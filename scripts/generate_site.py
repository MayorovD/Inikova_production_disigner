# -*- coding: utf-8 -*-
"""Generate static HTML portfolio from data/releases-manifest.json, using
release folders under portfolio/<release-tag>/ with original asset filenames."""
from __future__ import annotations

import json
from itertools import zip_longest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "data" / "releases-manifest.json").read_text(encoding="utf-8"))
OUT = ROOT
PROJECTS_DIR = OUT / "projects"

# release tag -> (site slug, English title, year, kind label)
TAG_MAP = {
    "Carpet": ("carpet", "The Carpet", "2026", "Animation film"),
    "The-Garden-of-the-Future": ("garden-of-the-future", "Garden of the Future", "2021", "Animation film"),
    "Spark-of-Life": ("spark-of-life", "Spark of Life", "1952", "Costume / stage"),
    "Eden": ("eden", "Eden", "1958", "Costume / stage"),
    "Reineke-Fuchs": ("reyneke-fox", "Reyneke the Fox", "1794", "Costume / stage"),
    "Le-Prince-des-Aigues-Marines": ("prince-aquamarine", "Prince Aquamarine", "1722", "Costume / props"),
    "The-Ladies-Delight": ("ladies-happiness", "Ladies' Happiness", "1883", "Costume / stage"),
    "The-Birds": ("birds", "Birds", "414 BC", "Costume / stage"),
}

SUMMARY = {
    "carpet": "A flying carpet, a boy, and the quiet life of a winter courtyard.",
    "garden-of-the-future": "A clay-and-paper garden where greenhouse, barn, and cyberpunk sky share a horizon.",
    "spark-of-life": "Costume plates for a stage piece about the first breath of a story.",
    "eden": "Costume sketches for a closed garden: ritual, fruit, and the moment before the fall.",
    "reyneke-fox": "Costumes for the medieval trickster: fur, court cloth, and a fox who always wins.",
    "prince-aquamarine": "A princely object world: aquamarine casket, staff, fabrics, and printed boards.",
    "ladies-happiness": "Department-store elegance: hats, gowns, and the theatre of shopping.",
    "birds": "A flock of costume ideas: beaks, plumage, and people who forgot they were human.",
}

LIMITS = {"storyboard": 8, "sketch": 10, "image": 8}


def esc(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def rel_from(page_dir: str, src: str) -> str:
    return src if page_dir == "root" else f"../{src}"


def header(active: str, prefix: str) -> str:
    def link(href: str, label: str, key: str) -> str:
        current = ' aria-current="page"' if active == key else ""
        return f'<a href="{prefix}{href}"{current}>{label}</a>'

    return f"""<header class="site">
      <a class="brand" href="{prefix}index.html">Inikova Polina
        <small>Production designer</small>
      </a>
      <nav>
        {link("index.html", "Work", "work")}
        {link("about.html", "About", "about")}
        {link("contact.html", "Contact", "contact")}
      </nav>
    </header>"""


def footer(prefix: str) -> str:
    return f"""<footer class="site">
    <div class="wrap">
      <span>© Polina Inikova, 2026. All rights reserved.</span>
      <a href="{prefix}contact.html">hello@inikova.works</a>
    </div>
  </footer>
  <script src="{prefix}js/site.js"></script>"""


def page(title: str, body: str, active: str, prefix: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <link rel="stylesheet" href="{prefix}css/site.css">
</head>
<body>
  <div class="wrap">
    {header(active, prefix)}
    {body}
  </div>
  {footer(prefix)}
</body>
</html>
"""


def chunks(items: list, n: int):
    args = [iter(items)] * n
    return zip_longest(*args)


def poster_for(release: dict) -> str | None:
    for a in release["assets"]:
        if a["name"].lower().startswith("default"):
            return f"portfolio/{release['tag']}/{a['name']}"
    # fall back to first non-pdf image if no default cover exists
    for a in release["assets"]:
        if not a["name"].lower().endswith(".pdf"):
            return f"portfolio/{release['tag']}/{a['name']}"
    return None


def work_table() -> str:
    cells = []
    for rel in MANIFEST:
        tag = rel["tag"]
        if tag not in TAG_MAP:
            continue
        slug, title, year, kind = TAG_MAP[tag]
        href = f"projects/{slug}.html"
        poster = poster_for(rel) or ""
        cells.append(
            f"""<td>
          <a href="{href}">
            <img src="{poster}" alt="{esc(title)}">
            <span class="cap">
              <span class="title">{esc(title)}</span>
              <span class="meta">{esc(year)} · {esc(kind)}</span>
            </span>
          </a>
        </td>"""
        )
    rows = []
    for group in chunks(cells, 3):
        tds = "".join(cell or "<td></td>" for cell in group)
        rows.append(f"<tr>{tds}</tr>")
    return '<table class="work">\n' + "".join(rows) + "\n    </table>"


def pick_gallery(rel: dict) -> list[dict]:
    out = []
    for a in rel["assets"]:
        if a["name"].lower().startswith("default"):
            continue
        if a["name"].lower().endswith(".pdf"):
            continue
        src = f"portfolio/{rel['tag']}/{a['name']}"
        cap = a["name"]
        out.append({"src": src, "name": a["name"]})
    return out


def gallery_table(assets: list[dict], page_dir: str) -> str:
    cells = []
    for asset in assets:
        src = rel_from(page_dir, asset["src"])
        cap = esc(asset["name"])
        cells.append(f'<td><img src="{src}" alt="{cap}"><span class="cap">{cap}</span></td>')
    if not cells:
        return ""
    rows = []
    for group in chunks(cells, 2):
        tds = "".join(cell or "<td></td>" for cell in group)
        rows.append(f"<tr>{tds}</tr>")
    return '<table class="gallery">\n' + "".join(rows) + "\n      </table>"


def write_index() -> None:
    body = f"""<section class="intro">
      <p>Hello. I am a production designer working in animation, costume, and props. I build small complete worlds — courtyards, gardens, courts, and the clothes that live inside them.</p>
    </section>
    {work_table()}"""
    (OUT / "index.html").write_text(
        page("Inikova Polina — Production designer", body, "work", ""),
        encoding="utf-8",
    )


def write_about() -> None:
    body = """<div class="about-grid">
      <div>
        <h1>About</h1>
        <p>Polina Inikova is a production designer based in Moscow. Her work moves between animated film and costume for the stage.</p>
        <p>She treats a set as a costume and a costume as architecture — silhouette first, then material, then the one object that makes the story specific.</p>
      </div>
      <div class="contact-block">
        <table class="credits">
          <tr><th>Name</th><td>Inikova Polina</td></tr>
          <tr><th>Field</th><td>Production design</td></tr>
          <tr><th>Based in</th><td>Moscow</td></tr>
          <tr><th>Languages</th><td>Russian, English</td></tr>
        </table>
      </div>
    </div>"""
    (OUT / "about.html").write_text(
        page("About — Inikova Polina", body, "about", ""),
        encoding="utf-8",
    )


def write_contact() -> None:
    body = """<section>
      <h1 class="page-title">Get in touch</h1>
      <p class="lede">For collaborations, teaching, and production design inquiries.</p>
      <table class="credits">
        <tr><th>Email</th><td>hello@inikova.works</td></tr>
        <tr><th>Telegram</th><td>@inikova</td></tr>
        <tr><th>Based in</th><td>Moscow, available for travel</td></tr>
      </table>
    </section>"""
    (OUT / "contact.html").write_text(
        page("Contact — Inikova Polina", body, "contact", ""),
        encoding="utf-8",
    )


def write_project(rel: dict) -> None:
    tag = rel["tag"]
    if tag not in TAG_MAP:
        return
    slug, title, year, kind = TAG_MAP[tag]
    poster = rel_from("projects", poster_for(rel)) if poster_for(rel) else ""
    summary = SUMMARY.get(slug, "")

    gallery = gallery_table(pick_gallery(rel), "projects")
    hero = f'<figure class="hero"><img src="{poster}" alt="{esc(title)}"></figure>' if poster else ""
    body = f"""<a class="back" href="../index.html">← Work</a>
    <h1 class="page-title">{esc(title)}</h1>
    <p class="lede">{esc(summary)}</p>
    <table class="credits">
      <tr><th>Title</th><td>{esc(rel['title'])}</td></tr>
      <tr><th>Year</th><td>{esc(year)}</td></tr>
      <tr><th>Field</th><td>{esc(kind)}</td></tr>
      <tr><th>Description</th><td>{esc(rel['description'])}</td></tr>
    </table>
    {hero}
    {gallery}"""
    path = PROJECTS_DIR / f"{slug}.html"
    path.write_text(
        page(f"{title} — Inikova Polina", body, "work", "../"),
        encoding="utf-8",
    )


def main() -> None:
    PROJECTS_DIR.mkdir(exist_ok=True)
    write_index()
    write_about()
    write_contact()
    for rel in MANIFEST:
        write_project(rel)
    print(f"wrote index, about, contact, and {len(MANIFEST)} project pages")


if __name__ == "__main__":
    main()