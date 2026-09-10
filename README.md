# Андрей Новицкий — site

Static site, no build step. Every path is relative, so it runs at a domain root
or a subpath on any host unchanged.

## Pages

- `Core/` — CORE bistro × A149: artist bio and the works catalogue with prices.

The repo root redirects to `Core/`.

## Deploy

GitHub Pages, serving `main` from the repo root. Every push to `main` rebuilds
in under a minute.

## Data

`Core/works.json` / `works.csv` is the catalogue, pulled from the CORE bistro
Google Sheet. The sheet export, full-resolution originals (`Core/Works/`) and the
pasted label cards (`Core/Labels/`) stay local — see `.gitignore`. The page uses
900px copies in `Core/assets/works/`.
