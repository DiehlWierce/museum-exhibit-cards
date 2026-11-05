#!/usr/bin/env python3
"""Check printed-QR page URLs; optionally register newly added card pages."""
from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "qr-routes.json"


class TitleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_title = False
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "title":
            self.in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.parts.append(data)

    @property
    def title(self) -> str:
        return " ".join(" ".join(self.parts).split())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--register-new",
        action="store_true",
        help="append discovered QR pages to qr-routes.json without removing old entries",
    )
    args = parser.parse_args()

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    base_url = data["base_url"]
    base = urlsplit(base_url)
    if not base.scheme or not base.netloc or not base.path.endswith("/"):
        print(f"Invalid base_url in {MANIFEST}", file=sys.stderr)
        return 1

    discovered: dict[str, Path] = {}
    for page in ROOT.rglob("index.html"):
        if ".git" in page.parts:
            continue
        source = page.read_text(encoding="utf-8")
        if re.search(r"\bid=[\"']qrcode[\"']", source, re.I):
            discovered[base_url + page.relative_to(ROOT).as_posix()] = page

    existing_urls = {item["url"] for item in data["routes"]}
    new_urls = sorted(set(discovered) - existing_urls)
    if args.register_new and new_urls:
        for url in new_urls:
            page = discovered[url]
            title_parser = TitleParser()
            title_parser.feed(page.read_text(encoding="utf-8"))
            data["routes"].append({"url": url, "title": title_parser.title or page.parent.name})
        MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Registered {len(new_urls)} new QR route(s); existing entries were kept.")

    registered: set[str] = set()
    failures: list[str] = []
    for item in data["routes"]:
        url = item["url"]
        if not url.startswith(base_url):
            failures.append(f"URL outside configured site base: {url}")
            continue
        if url in registered:
            failures.append(f"Duplicate registered URL: {url}")
            continue
        registered.add(url)
        relative = urlsplit(url).path[len(base.path):]
        page = ROOT / relative
        if not page.is_file():
            failures.append(f"Missing page for {url} (expected {page.relative_to(ROOT)})")
            continue
        source = page.read_text(encoding="utf-8")
        if not re.search(r"\bid=[\"']qrcode[\"']", source, re.I):
            failures.append(f"QR container missing from {page.relative_to(ROOT)}")

    for url in sorted(set(discovered) - registered):
        failures.append(f"QR page missing from manifest: {url}")
    for url in sorted(registered - set(discovered)):
        failures.append(f"Manifest route no longer contains a QR page: {url}")

    if failures:
        print("QR route check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"QR route check passed: {len(registered)} stable card URLs resolve to their original pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
