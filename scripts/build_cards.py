#!/usr/bin/env python3
"""Generate the static menus and card pages from the site's JSON data."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from string import Template
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
CARDS_FILE = ROOT / "data" / "cards.json"
SECTIONS_FILE = ROOT / "data" / "sections.json"
CARD_TEMPLATE = Template((ROOT / "templates" / "card.html").read_text(encoding="utf-8"))
MENU_TEMPLATE = Template((ROOT / "templates" / "menu.html").read_text(encoding="utf-8"))


def relative_asset(asset: Path, page: Path) -> str:
    return Path(os.path.relpath(asset, page.parent)).as_posix()


def render_card(card: dict) -> str:
    page = ROOT / card["path"]
    return CARD_TEMPLATE.substitute(
        lang=card.get("lang", "ru"),
        viewport=card["viewport"],
        title_html=card["title_html"],
        stylesheet=relative_asset(ROOT / "styles.css", page),
        body_class=card["body_class"],
        content_html=card["content_html"],
        qr_html=card["qr_html"],
        qrcode_script=relative_asset(ROOT / "qrcode.min.js", page),
        qr_script=relative_asset(ROOT / "qr.js", page),
    )


def render_menu_script(items: list[tuple[str, str]]) -> str:
    pairs = ",\n".join(
        f"  [{json.dumps(path, ensure_ascii=False)}, {json.dumps(title, ensure_ascii=False)}]"
        for path, title in items
    )
    return (
        "// Пункты меню: [папка, название]\n"
        f"const folders = [\n{pairs}\n];\n\n"
        'const menu = document.getElementById("menu");\n\n'
        "folders.forEach(([folder, displayName]) => {\n"
        '  const link = document.createElement("a");\n'
        '  link.href = `${folder}/index.html`;\n'
        '  link.className = "item";\n'
        "  link.textContent = displayName;\n"
        "  menu.appendChild(link);\n"
        "});\n"
    )


def render_menu_page(page_path: Path, title_html: str, heading_html: str,
                     lang: str, viewport: str, body_class: str) -> str:
    return MENU_TEMPLATE.substitute(
        lang=lang,
        viewport=viewport,
        title_html=title_html,
        stylesheet=relative_asset(ROOT / "styles.css", page_path),
        body_class=body_class,
        heading_html=heading_html,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="check generated files without writing")
    args = parser.parse_args()

    cards_data = json.loads(CARDS_FILE.read_text(encoding="utf-8"))
    sections_data = json.loads(SECTIONS_FILE.read_text(encoding="utf-8"))
    if cards_data.get("schema_version") != 2 or sections_data.get("schema_version") != 1:
        print("Unsupported JSON data schema version", file=sys.stderr)
        return 1

    failures: list[str] = []
    expected_paths: dict[str, str] = {}
    card_paths: set[str] = set()
    cards_by_section: dict[str, list[dict]] = {}
    for card in cards_data["cards"]:
        relative = Path(card["path"])
        if relative.is_absolute() or ".." in relative.parts or relative.suffix.lower() != ".html":
            failures.append(f"Unsafe or invalid card path: {card['path']}")
            continue
        if card["path"] in card_paths:
            failures.append(f"Duplicate card path: {card['path']}")
            continue
        card_paths.add(card["path"])
        if relative.parts[:1] != (card["section_path"],) or len(relative.parts) != 3:
            failures.append(f"Path/section mismatch: {card['path']}")
            continue
        if relative.parts[1] != card["slug"] or relative.name != "index.html":
            failures.append(f"Path/slug mismatch: {card['path']}")
            continue
        if re.search(r"\bid=[\"']qrcode[\"']", card["content_html"], re.I):
            failures.append(f"QR container must remain in template field for {card['path']}")
            continue
        cards_by_section.setdefault(card["section_path"], []).append(card)
        expected_paths[card["path"]] = render_card(card)

    manifest = json.loads((ROOT / "qr-routes.json").read_text(encoding="utf-8"))
    base = urlsplit(manifest["base_url"])
    registered_paths = {
        urlsplit(route["url"]).path[len(base.path):]
        for route in manifest["routes"]
        if urlsplit(route["url"]).path.startswith(base.path)
    }
    if registered_paths != card_paths:
        missing = sorted(registered_paths - card_paths)
        unregistered = sorted(card_paths - registered_paths)
        failures.append(f"Card data and QR manifest differ; missing={missing}, unregistered={unregistered}")

    sections = sections_data["sections"]
    section_paths = [section["path"] for section in sections]
    if len(section_paths) != len(set(section_paths)):
        failures.append("Duplicate section path in sections.json")
    if set(cards_by_section) != set(section_paths):
        failures.append("Section data and card data do not describe the same section paths")

    expected_paths["index.html"] = render_menu_page(
        ROOT / "index.html", sections_data["home_title_html"],
        sections_data["home_heading_html"], sections_data.get("lang", "ru"),
        sections_data["viewport"], sections_data["home_body_class"])
    expected_paths["script.js"] = render_menu_script(
        [(section["path"], section["menu_title"]) for section in sections])

    for section in sections:
        section_path = section["path"]
        section_index = Path(section_path) / "index.html"
        expected_paths[section_index.as_posix()] = render_menu_page(
            ROOT / section_index, section["title_html"], section["heading_html"],
            section.get("lang", "ru"), section["viewport"], section["body_class"])
        expected_paths[f"{section_path}/script.js"] = render_menu_script(
            [(card["slug"], card["menu_title"]) for card in cards_by_section.get(section_path, [])])

    for relative, expected in expected_paths.items():
        output = ROOT / relative
        if args.check:
            if not output.is_file() or output.read_text(encoding="utf-8") != expected:
                failures.append(f"Generated file is out of date: {relative}")
        else:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(expected, encoding="utf-8")

    if failures:
        for item in failures:
            print(item, file=sys.stderr)
        return 1

    action = "checked" if args.check else "rendered"
    print(f"{len(expected_paths)} generated files {action} from JSON data and templates.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
