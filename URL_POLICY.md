# QR URL policy

Every URL in `qr-routes.json` is treated as a permanent public address because printed QR codes may already point to it.

- Keep the repository owner and repository name stable while the site is hosted at `diehlwierce.github.io/museum-exhibit-cards`.
- Do not move, rename, or change the letter case of a registered card's directory or `index.html` path.
- Content, layout, and shared code may be refactored as long as the registered URL continues to serve the same card.
- Before an intentional URL migration, provide a tested redirect for every old address and keep its old path reachable.
- Run `python3 scripts/check_qr_routes.py` after changes to card pages or routing.
