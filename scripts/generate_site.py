# -*- coding: utf-8 -*-
"""Generate static HTML portfolio pages from data/portfolio.json."""
from __future__ import annotations

import json
from itertools import zip_longest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "data" / "portfolio.json").read_text(encoding="utf-8"))
OUT = ROOT
PROJECTS_DIR = OUT / "projects"

KIND_LABEL = {
    "animation-film": "Animation",
    "costume-production": "Costume",
    "costume-props": "Props",
    "sketchbook": "Drawing",
}

COPY = {
    "carpet": {
        "year": "2025",
        "summary": "A winter courtyard somewhere in a sleeping district. A flying carpet, a boy, and the quiet life of neighbours seen from a balcony.",
        "text": "Production design for a short animated film: character line-ups, yard and apartment environments, colour stills, and a full storyboard. The world is built from snow, brick, laundry ropes, and one worn green carpet that refuses to stay on the floor.",
        "credits": [
            ("Role", "Production designer"),
            ("Format", "Animated short"),
            ("Year", "2025"),
            ("Director", "To be confirmed"),
            ("DoP / layout", "To be confirmed"),
        ],
    },
    "garden-of-the-future": {
        "year": "2024",
        "summary": "A clay-and-paper garden where greenhouse, barn, and cyberpunk sky share one horizon.",
        "text": "Sets and frames for a speculative garden: plasticine maquettes, sun studies, onion fields, and a panoramic sky. The design mixes pastoral objects with a slightly unwell future light.",
        "credits": [
            ("Role", "Production designer"),
            ("Format", "Animated short"),
            ("Year", "2024"),
            ("Director", "To be confirmed"),
        ],
    },
    "spark-of-life": {
        "year": "2024",
        "summary": "Costume plates for a stage piece about the first breath of a story — cloth, silhouette, and a single spark.",
        "text": "Final costume looks and print-ready plates. The palette stays close to skin, rust, and candlelight, with silhouettes that can be read from the back row.",
        "credits": [
            ("Role", "Costume / production designer"),
            ("Format", "Stage production"),
            ("Year", "2024"),
        ],
    },
    "eden": {
        "year": "2024",
        "summary": "Costume sketches for a closed garden: ritual, fruit, and the moment before the fall.",
        "text": "A series of costume boards that treat Eden as a wardrobe problem — how to dress innocence, knowledge, and the landscape that holds them.",
        "credits": [
            ("Role", "Costume designer"),
            ("Format", "Stage / film costumes"),
            ("Year", "2024"),
        ],
    },
    "reyneke-fox": {
        "year": "2023",
        "summary": "Costumes for the medieval trickster: fur, court cloth, and a fox who always leaves the scene richer.",
        "text": "Finished costume plates and preparatory drafts for Reyneke the Fox. Each look is built as a readable type — peasant, courtier, beast — then spoiled by one sly detail.",
        "credits": [
            ("Role", "Costume designer"),
            ("Format", "Stage production"),
            ("Year", "2023"),
            ("Source", "Reyneke Fuchs / folk epic"),
        ],
    },
    "prince-aquamarine": {
        "year": "2023",
        "summary": "A princely object world: aquamarine casket, staff, fabrics, and printed costume boards.",
        "text": "Props and materials research for a fairy-tale court. The aquamarine box and the staff are designed as characters of their own — cold stone, warm wood, and a little too much gold.",
        "credits": [
            ("Role", "Production designer, props"),
            ("Format", "Costume & object design"),
            ("Year", "2023"),
        ],
    },
    "ladies-happiness": {
        "year": "2023",
        "summary": "Department-store elegance: hats, gowns, and the theatre of shopping.",
        "text": "Costume sketches for a production after Zola's Au Bonheur des Dames. Silhouettes sit between shop-floor practicality and the dream the window sells.",
        "credits": [
            ("Role", "Costume designer"),
            ("Format", "Stage production"),
            ("Year", "2023"),
            ("Source", "Au Bonheur des Dames"),
        ],
    },
    "birds": {
        "year": "2022",
        "summary": "A flock of costume ideas: beaks, plumage, and people who forgot they were human.",
        "text": "Eleven costume plates for an ensemble of birds. The drawings keep anatomy honest enough to walk, strange enough to roost.",
        "credits": [
            ("Role", "Costume designer"),
            ("Format", "Stage production"),
            ("Year", "2022"),
        ],
    },
    "sketches": {
        "year": "2022–2026",
        "summary": "Life drawings, scans, and quick studies kept outside the productions.",
        "text": "A working sketchbook. Figures, faces, and notes that do not belong to a single title but feed all of them.",
        "credits": [
            ("Role", "Artist"),
            ("Format", "Sketchbook"),
            ("Year", "2022–2026"),
        ],
    },
}

LIMITS = {
    "storyboard": 8,
    "sketch": 10,
    "image": 8,
}


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def rel_from(page_dir: str, src: str) -> str:
    if page_dir == "root":
        return src
    return f"../{src}"


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


def pick_gallery(project: dict) -> list[dict]:
    grouped: dict[str, list] = {}
    for asset in project["assets"]:
        grouped.setdefault(asset["kind"], []).append(asset)

    order = [
        "poster",
        "character",
        "environment",
        "prop",
        "still",
        "film",
        "sketch",
        "storyboard",
        "image",
        "video",
    ]
    picked = []
    seen = set()
    for kind in order:
        items = grouped.get(kind, [])
        limit = LIMITS.get(kind)
        if kind == "poster":
            continue
        if kind == "storyboard":
            overview = [a for a in items if "overview" in a["src"]]
            frames = [a for a in items if a not in overview][: LIMITS["storyboard"]]
            items = overview + frames
        elif limit:
            items = items[:limit]
        for asset in items:
            if asset["src"] not in seen:
                picked.append(asset)
                seen.add(asset["src"])
    return picked


def work_table() -> str:
    cells = []
    for row in CATALOG["table"]:
        info = COPY[row["id"]]
        href = f"projects/{row['id']}.html"
        poster = row["poster"]
        cells.append(
            f"""<td>
          <a href="{href}">
            <img src="{poster}" alt="{esc(row['title'])}">
            <span class="cap">
              <span class="title">{esc(row['title'])}</span>
              <span class="meta">{esc(info['year'])} · {esc(KIND_LABEL.get(row['kind'], row['kind']))}</span>
            </span>
          </a>
        </td>"""
        )
    rows = []
    for group in chunks(cells, 3):
        tds = "".join(cell or "<td></td>" for cell in group)
        rows.append(f"<tr>{tds}</tr>")
    return '<table class="work">\n' + "\n".join(rows) + "\n    </table>"


def gallery_table(assets: list[dict], page_dir: str) -> str:
    cells = []
    for asset in assets:
        src = rel_from(page_dir, asset["src"])
        cap = esc(asset["caption"])
        if asset["kind"] == "video":
            inner = f'<video src="{src}" controls preload="metadata"></video><span class="cap">{cap}</span>'
        else:
            inner = f'<img src="{src}" alt="{cap}"><span class="cap">{cap}</span>'
        cells.append(f"<td>{inner}</td>")
    if not cells:
        return ""
    rows = []
    for group in chunks(cells, 2):
        tds = "".join(cell or "<td></td>" for cell in group)
        rows.append(f"<tr>{tds}</tr>")
    return '<table class="gallery">\n' + "\n".join(rows) + "\n      </table>"


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
        <p>Polina Inikova is a production designer based in Moscow. Her work moves between animated film and costume for the stage: character line-ups, environments, props, and the colour of a whole picture.</p>
        <p>She treats a set as a costume and a costume as architecture — silhouette first, then material, then the one object that makes the story specific. A carpet. A casket. A barn under a wrong sky.</p>
        <p>Selected work includes the animated shorts <em>The Carpet</em> and <em>Garden of the Future</em>, and costume cycles <em>Reyneke the Fox</em>, <em>Eden</em>, <em>Ladies' Happiness</em>, and <em>Birds</em>.</p>
      </div>
      <div class="contact-block">
        <table class="credits">
          <tr><th>Name</th><td>Inikova Polina</td></tr>
          <tr><th>Field</th><td>Production design</td></tr>
          <tr><th>Based in</th><td>Moscow</td></tr>
          <tr><th>Languages</th><td>Russian, English</td></tr>
          <tr><th>Email</th><td><a href="mailto:hello@inikova.works">hello@inikova.works</a></td></tr>
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
        <tr><th>Email</th><td><a href="mailto:hello@inikova.works">hello@inikova.works</a></td></tr>
        <tr><th>Telegram</th><td>@inikova</td></tr>
        <tr><th>Based in</th><td>Moscow, available for travel</td></tr>
      </table>
      <p class="bodycopy">Please write with a short note on the project, dates, and whether you need costumes, environments, props, or the whole visual world. Materials on this site are copyright of the author and may not be copied without permission.</p>
    </section>"""
    (OUT / "contact.html").write_text(
        page("Contact — Inikova Polina", body, "contact", ""),
        encoding="utf-8",
    )


def write_project(project: dict) -> None:
    info = COPY[project["id"]]
    poster = rel_from("projects", project["poster"]) if project["poster"] else ""
    credits_rows = "".join(
        f"<tr><th>{esc(k)}</th><td>{esc(v)}</td></tr>" for k, v in info["credits"]
    )
    pdf = ""
    if project.get("pdf"):
        pdf = f'<p><a class="pdf-link" href="{rel_from("projects", project["pdf"])}" target="_blank" rel="noopener">Open project PDF</a></p>'
    gallery = gallery_table(pick_gallery(project), "projects")
    hero = f'<figure class="hero"><img src="{poster}" alt="{esc(project["title"])}"></figure>' if poster else ""
    body = f"""<a class="back" href="../index.html">← Work</a>
    <h1 class="page-title">{esc(project["title"])}</h1>
    <p class="lede">{esc(info["summary"])}</p>
    <table class="credits">{credits_rows}</table>
    {hero}
    <p class="bodycopy">{esc(info["text"])}</p>
    {pdf}
    {gallery}"""
    path = PROJECTS_DIR / f"{project['id']}.html"
    path.write_text(
        page(f"{project['title']} — Inikova Polina", body, "work", "../"),
        encoding="utf-8",
    )


def main() -> None:
    PROJECTS_DIR.mkdir(exist_ok=True)
    write_index()
    write_about()
    write_contact()
    for project in CATALOG["projects"]:
        write_project(project)
    print(f"wrote index, about, contact, and {len(CATALOG['projects'])} project pages")


if __name__ == "__main__":
    main()
