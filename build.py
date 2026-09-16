#!/usr/bin/env python3
"""Regenerate the works grid in Core/index.html from Core/works.json.

Only the cards between <div class="grid"> and its closing tag are rewritten;
the head, logo and bio stay hand-edited in the HTML.

To mark a work, set its "status" in works.json to "reserved" or "sold"
(or null to clear it), then run:  python3 build.py
"""
import json
import re
from pathlib import Path

from PIL import Image

CORE = Path(__file__).parent / "Core"
NB = " "
WIDE_RATIO = 1.4  # wider than this spans both columns (the diptych)


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def card(work, statuses):
    src = f"assets/works/{Path(work['image']).stem}.jpg"
    w, h = Image.open(CORE / src).size
    title = esc(work["title"] + (f" ({work['note']})" if work["note"] else ""))
    details = esc(f"{work['size']}, {work['medium']}").replace(" см", NB + "см")
    price = f"{work['price']:,}".replace(",", NB) + NB + "₽"
    wide = " work--wide" if w / h > WIDE_RATIO else ""

    status = ""
    if work.get("status"):
        key = work["status"]
        if key not in statuses:
            raise SystemExit(f"work {work['id']}: unknown status {key!r}")
        status = (f'\n            <span class="work__status work__status--{key}">'
                  f"{statuses[key]}</span>")

    return f"""        <figure class="work{wide}">
          <img src="{src}" alt="{title}" width="{w}" height="{h}" loading="lazy" decoding="async">
          <figcaption>
            <span class="work__title">{title}</span>
            <span class="work__details">{details}</span>
            <span class="work__price">{price}</span>{status}
          </figcaption>
        </figure>"""


def main():
    data = json.loads((CORE / "works.json").read_text())
    cards = "\n".join(card(w, data["statuses"]) for w in data["works"])

    page = CORE / "index.html"
    html = page.read_text()
    html, n = re.subn(r'(<div class="grid">\n).*?(\n      </div>\n  </main>)',
                      lambda m: m.group(1) + cards + m.group(2), html, flags=re.S)
    if n != 1:
        raise SystemExit("grid block not found in Core/index.html")
    page.write_text(html)

    marked = [f"{w['title']}: {w['status']}" for w in data["works"] if w.get("status")]
    print(f"{len(data['works'])} cards written" + (f"; {', '.join(marked)}" if marked else ""))


if __name__ == "__main__":
    main()
