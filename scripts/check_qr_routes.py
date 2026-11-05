#!/usr/bin/env python3
"""Ensure every registered printed-QR URL still resolves to its original card page."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "qr-routes.json"


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    base_url = data["base_url"]
    base = urlsplit(base_url)
    if not base.scheme or not base.netloc or not base.path.endswith("/"):
        print(f"Invalid base_url in {MANIFEST}", file=sys.stderr)
        return 1

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

    discovered: set[str] = set()
    for page in ROOT.rglob("index.html"):
        if ".git" in page.parts:
            continue
        source = page.read_text(encoding="utf-8")
        if re.search(r"\bid=[\"']qrcode[\"']", source, re.I):
            discovered.add(base_url + page.relative_to(ROOT).as_posix())

    for url in sorted(discovered - registered):
        failures.append(f"QR page missing from manifest: {url}")
    for url in sorted(registered - discovered):
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
