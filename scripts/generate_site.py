# -*- coding: utf-8 -*-
"""Generate a Russian static portfolio from data/releases-manifest.json.

Projects keep their release folders portfolio/<release-tag>/. The first page
shows a vertical list of horizontal posters (default.jpg, or 1.jpg for Carpet).
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "data" / "releases-manifest.json").read_text(encoding="utf-8"))
OUT = ROOT
PROJECTS_DIR = OUT / "projects"

# release tag -> (slug, short Russian title, year label, field label, one-line summary)
TAG_MAP = {
    "Carpet": ("carpet", "Ковёр", "2026", "Анимационный фильм", "История о непослушном ковре и одиноком дедушке — Свердловская киностудия."),
    "The-Garden-of-the-Future": ("garden-of-the-future", "Сад будущего", "2021", "Анимационный фильм", "Мальчик с помощью волшебной птицы попадает в миры — версии его собственного сада."),
    "Spark-of-Life": ("spark-of-life", "Искра жизни", "1952", "Костюмы, спектакль", "Люди цепляются за последнее, что у них осталось, — за искру жизни."),
    "Eden": ("eden", "Эдем", "1958", "Костюмы, спектакль", "Экипаж землян терпит крушение на неизученной планете, где живут двутелы."),
    "Reineke-Fuchs": ("reyneke-fox", "Рейнеке-лис", "1794", "Костюмы, спектакль", "Под масками зверей — феодальное общество и хитрый лис Рейнеке."),
    "Le-Prince-des-Aigues-Marines": ("prince-aquamarine", "Принц Аквамарин", "1722", "Костюмы и предметы", "Проклятый принц проходит испытания, чтобы разрушить чары и найти возлюбленную."),
    "The-Ladies-Delight": ("ladies-happiness", "Дамское счастье", "1883", "Костюмы, спектакль", "Витрины и кружева универмага-гиганта, где одни богатеют, а другие разоряются."),
    "The-Birds": ("birds", "Птицы", "414 до н. э.", "Костюмы, спектакль", "Афиняне с птицами основывают между небом и землёй Тучекукушкин град."),
}

# explicit row layout per slug: each entry is a list of filenames for that row.
# Rows render as full-width .main-zone (no automatic r/l columns).
CUSTOM_ROWS = {
    "carpet": [
        ["1.jpg"],
        ["2.jpg"],
        ["3.jpg"],
        ["3_r1.jpg", "3_r2.jpg"],
        ["4_2.jpg"],
        ["5_r1.jpg"],
        ["5.jpg"],
        ["6.jpg"],
        # "VIDEO"  <- placeholder for pilot (video not added yet)
        ["7_1.jpg", "7_2.jpg"],
        ["8_1.jpg", "8_2.jpg"],
        ["9_1.jpg", "9_2.jpg"],
    ],
    "garden-of-the-future": [
        ["1.jpg"],
        ["2.jpg"],
        ["3.jpg"],
        {"main": ["4_1.jpg", "4_2.jpg"], "fit": True},
        ["5.jpg"],
        ["6_1.jpg", "6_2.jpg", "6_3.jpg"],
    ],
    "prince-aquamarine": [
        {"main": ["1.jpg"], "r": ["1_r1.jpg", "1_r2.jpg"]},
        ["2_1.jpg", "2_2.jpg"],
        ["3.jpg"],
        ["4_1.jpg", "4_2.jpg"],
        {"main": ["5.jpg"], "l": ["5_l1.jpg", "5_l2.jpg"]},
    ],
    "birds": [
        ["1.jpg"],
        ["3.jpg"],
        ["2_1.jpg"],
        ["2_2.jpg"],
        ["2_3.jpg"],
        ["4_1.jpg"],
        ["4_2.jpg"],
        ["4_3.jpg"],
    ],
}


def esc(text) -> str:
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
      <a class="brand" href="{prefix}index.html">Иникова Полина
        <small>Художник-постановщик</small>
      </a>
      <nav>
        {link("index.html", "Проекты", "work")}
        {link("sketches.html", "Скетчи", "sketches")}
        {link("about.html", "Обо мне", "about")}
      </nav>
    </header>"""


def footer(prefix: str) -> str:
    return f"""<footer class="site">
    <div class="wrap">
      <span>© Полина Иникова, 2026. Все права защищены.</span>
<a href="mailto:polinainikova02@gmail.com">polinainikova02@gmail.com</a>
    </div>
  </footer>
  <script src="{prefix}js/site.js"></script>"""


def page(title: str, body: str, active: str, prefix: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="ru">
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


def webp_name(name: str) -> str:
    if name.lower().endswith(".webp"):
        return name
    stem = name[: name.rfind(".")]
    return f"{stem}.webp"


def poster_for(release: dict) -> str:
    tag = release["tag"]
    for a in release["assets"]:
        if a["name"].lower().startswith("default"):
            return f"portfolio_webp/{tag}/{webp_name(a['name'])}"
    # fall back to first non-pdf image if no default cover exists
    for a in release["assets"]:
        if not a["name"].lower().endswith(".pdf"):
            return f"portfolio_webp/{tag}/{webp_name(a['name'])}"
    return f"portfolio_webp/{tag}/1.webp"


def ordered():  # curated display order
    order = [
        "The-Birds",
        "Carpet",
        "Reineke-Fuchs",
        "The-Ladies-Delight",
        "Eden",
        "The-Garden-of-the-Future",
        "Le-Prince-des-Aigues-Marines",
        "Spark-of-Life",
    ]
    by_tag = {r["tag"]: r for r in MANIFEST}
    return [by_tag[t] for t in order if t in by_tag]


def project_rows() -> str:
    out = []
    for rel in ordered():
        tag = rel["tag"]
        slug, title, year, field, summary = TAG_MAP[tag]
        href = f"projects/{slug}.html"
        poster = poster_for(rel)
        out.append(f"""<a class="work-item" href="{href}">
      <img src="{poster}" alt="{esc(title)}">
      <div class="work-caption">
        <span class="work-title">{esc(title)}</span>
      </div>
    </a>""")
    return "\n".join(out)


def sketches_rel() -> dict:
    for r in MANIFEST:
        if r["tag"] == "Sketches":
            return r
    raise RuntimeError("Sketches release not present in manifest")


def write_index() -> None:
    body = f"""<section class="projects">
      <h1 class="page-title">Проекты</h1>
      {project_rows()}
    </section>"""
    (OUT / "index.html").write_text(
        page("Иникова Полина — художник-постановщик", body, "work", ""),
        encoding="utf-8",
    )


def write_about() -> None:
    body = """<div class="about-grid">
      <div class="about-photo">
        <img src="images/about.webp" alt="Портрет Полины">
      </div>
      <div class="about-text">
        <h1>Обо мне</h1>
        <p>Меня зовут Полина, я 2D-художник и аниматор. Люблю создавать разнообразные миры — от фонов и пропсов до персонажей и раскадровок — и работать в разных стилях, находя для каждого проекта свой визуальный язык.</p>
        <p>В 2026 году я завершила работу над анимационным короткометражным фильмом «Ковёр» на Свердловской киностудии, где выступила и в качестве режиссёра, и художника-постановщика. Также работала художником по фонам над другими короткометражными фильмами.</p>
        <p>В 2022 году получила среднее специальное образование в колледже ВГИК. Сейчас завершаю обучение в университете ВГИК по специальности «художник анимации и компьютерной графики».</p>
        <p>Свободно владею следующим программным обеспечением:</p>
        <ul class="software-list">
          <li>Adobe Photoshop</li>
          <li>Adobe Illustrator</li>
          <li>Adobe After Effects</li>
          <li>Adobe Premiere Pro</li>
          <li>Blender 3D</li>
          <li>Toon Boom Harmony</li>
        </ul>
        <p>Открыта к интересным проектам.</p>
        <div class="about-contact">
          <h2>Контакты</h2>
          <p><a href="mailto:polinainikova02@gmail.com">polinainikova02@gmail.com</a></p>
          <p>Телеграм: <a href="https://t.me/poli_ini" rel="noopener">@poli_ini</a></p>
          <p>ВКонтакте: <a href="https://vk.ru/club213014018" rel="noopener">«Иней на поляне»</a></p>
        </div>
      </div>
    </div>"""
    (OUT / "about.html").write_text(
        page("Обо мне — Иникова Полина", body, "about", ""),
        encoding="utf-8",
    )


def write_project(rel: dict) -> None:
    tag = rel["tag"]
    if tag not in TAG_MAP:
        return
    slug, title, year, field, summary = TAG_MAP[tag]

    def rel_img(src: str) -> str:
        return rel_from("projects", src)

    gallery = gallery_html(rel, slug, "../")

    body = f"""<a class="back" href="../index.html">← Назад к проектам</a>
    <h1 class="page-title">{esc(title)}</h1>
    <p class="lede">{esc(rel["description"])}</p>
    {gallery}"""
    path = PROJECTS_DIR / f"{slug}.html"
    path.write_text(
        page(f"{title} — Иникова Полина", body, "work", "../"),
        encoding="utf-8",
    )


def gallery_html(rel: dict, slug: str, prefix: str = "") -> str:
    tag = rel["tag"]

    def existing(argv):
        return f'{prefix}portfolio_webp/{tag}/{webp_name(argv)}'

    # explicit per-project layout
    if slug in CUSTOM_ROWS:
        def img_cell(n):
            return f'<a class="cell"><img src="{existing(n)}" alt="{esc(n)}"></a>'

        def col_html(names, side):
            if not names:
                return ""
            cells = "".join(img_cell(n) for n in names)
            return f'<div class="col" data-side="{side}">{cells}</div>'

        def render_row(entry):
            if isinstance(entry, dict):
                main = entry.get("main", [])
                left = col_html(entry.get("l", []), "l")
                right = col_html(entry.get("r", []), "r")
                fit = f' data-fit="hw"' if entry.get("fit") else ""
                mz = (
                    f'<div class="main-zone"{fit}>'
                    + "".join(img_cell(n) for n in main)
                    + "</div>"
                )
                parts = [left, mz, right]
                inner = "".join(p for p in parts if p)
                return f'<div class="row">{inner}</div>'
            # list: all in main-zone
            mz = "".join(f'<div class="main-zone">{img_cell(n)}</div>' for n in entry)
            return f'<div class="row">{mz}</div>'

        rows_html = "\n".join(render_row(entry) for entry in CUSTOM_ROWS[slug])
        return f'<div class="rows">\n{rows_html}\n      </div>'

    # parse assets by row number
    import re
    row_re = re.compile(r"^(\d+)(?:_(\d+))?(?:_([rl])(\d+))?$")
    rows: dict[int, dict] = {}

    for a in rel["assets"]:
        name = a["name"].lower()
        if name.startswith("default") or name.endswith(".pdf"):
            continue
        stem = name[:-4] if name.endswith(".jpg") else name.replace(".", "")
        m = row_re.match(stem)
        if not m:
            continue
        row_num = int(m.group(1))
        pos = m.group(2)
        side = m.group(3)
        seq = m.group(4)
        bucket = rows.setdefault(
            row_num, {"main": [], "l": [], "r": []}
        )
        src = f"{prefix}portfolio_webp/{tag}/{webp_name(a['name'])}"
        if side:
            bucket[side].append({"seq": int(seq), "src": src, "cap": esc(a["name"])})
        else:
            rank = 0 if pos is None else int(pos)
            bucket["main"].append({"rank": rank, "src": src, "cap": esc(a["name"])})

    if not rows:
        return ""

    def col_html(items, orient):
        if not items:
            return ""
        items = sorted(items, key=lambda x: x["seq"] if orient == "stack" else x["rank"])
        cells = "".join(
            f'<a class="cell"><img src="{i["src"]}" alt="{i["cap"]}"></a>'
            for i in items
        )
        return f'<div class="col">{cells}</div>'

    def row_html(row_num, bucket):
        main = sorted(bucket["main"], key=lambda x: x["rank"])
        left = col_html(bucket["l"], "stack")
        right = col_html(bucket["r"], "stack")
        main_cells = "".join(
            f'<a class="cell"><img src="{i["src"]}" alt="{i["cap"]}"></a>'
            for i in main
        )
        main_zone = f'<div class="main-zone">{main_cells}</div>' if main_cells else ""
        parts = [left, main_zone, right]
        body = "".join(p for p in parts if p)
        return f'<div class="row" data-row="{row_num}">{body}</div>'

    rows_html = "\n".join(row_html(n, rows[n]) for n in sorted(rows))
    return f'<div class="rows">\n{rows_html}\n      </div>'


def write_sketches() -> None:
    rel = sketches_rel()
    lede = f'<p class="lede">{esc(rel["description"])}</p>\n    ' if rel.get("description") else ""
    body = f"""<a class="back" href="index.html">← К проектам</a>
    <h1 class="page-title">Скетчи</h1>
    {lede}<div class="sketches-gal">
      {gallery_html(rel, "sketches")}
    </div>"""
    (OUT / "sketches.html").write_text(
        page("Скетчи — Иникова Полина", body, "sketches", ""),
        encoding="utf-8",
    )


def main() -> None:
    PROJECTS_DIR.mkdir(exist_ok=True)
    write_index()
    write_about()
    write_sketches()
    for rel in MANIFEST:
        write_project(rel)
    print(f"wrote index, about, sketches, and {len(MANIFEST)} project pages")


if __name__ == "__main__":
    main()