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
        {link("about.html", "Обо мне", "about")}
        {link("contact.html", "Контакты", "contact")}
      </nav>
    </header>"""


def footer(prefix: str) -> str:
    return f"""<footer class="site">
    <div class="wrap">
      <span>© Полина Иникова, 2026. Все права защищены.</span>
      <a href="{prefix}contact.html">hello@inikova.works</a>
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


def poster_for(release: dict) -> str:
    tag = release["tag"]
    for a in release["assets"]:
        if a["name"].lower().startswith("default"):
            return f"portfolio/{tag}/{a['name']}"
    # fall back to first non-pdf image if no default cover exists
    for a in release["assets"]:
        if not a["name"].lower().endswith(".pdf"):
            return f"portfolio/{tag}/{a['name']}"
    return f"portfolio/{tag}/1.jpg"


def ordered():  # curated display order
    order = [
        "Carpet",
        "The-Garden-of-the-Future",
        "Spark-of-Life",
        "Eden",
        "Reineke-Fuchs",
        "Le-Prince-des-Aigues-Marines",
        "The-Ladies-Delight",
        "The-Birds",
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
        <span class="work-meta">{esc(year)} · {esc(field)}</span>
        <p class="work-summary">{esc(summary)}</p>
      </div>
    </a>""")
    return "\n".join(out)


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
      <div>
        <h1>Обо мне</h1>
        <p>Полина Иникова — художник-постановщик из Москвы. Её работа лежит между анимационным кино и костюмом для сцены: линейки персонажей, пространства, предметы и цвет всей картины целиком.</p>
        <p>Она относится к пространству как к костюму, а к костюму — как к архитектуре: сначала силуэт, затем материал, и только потом тот единственный предмет, что делает историю особенной.</p>
        <p>Среди избранных работ — анимационные короткометражки «Ковёр» и «Сад будущего», а также циклы костюмов: «Рейнеке-лис», «Эдем», «Дамское счастье», «Птицы».</p>
      </div>
      <div class="contact-block">
        <table class="credits">
          <tr><th>Имя</th><td>Иникова Полина</td></tr>
          <tr><th>Профессия</th><td>Художник-постановщик</td></tr>
          <tr><th>Город</th><td>Москва</td></tr>
          <tr><th>Языки</th><td>русский, английский</td></tr>
        </table>
      </div>
    </div>"""
    (OUT / "about.html").write_text(
        page("Обо мне — Иникова Полина", body, "about", ""),
        encoding="utf-8",
    )


def write_contact() -> None:
    body = """<section>
      <h1 class="page-title">Контакты</h1>
      <p class="lede">Для сотрудничества, преподавания и вопросов по производственному дизайну.</p>
      <table class="credits">
        <tr><th>Почта</th><td>hello@inikova.works</td></tr>
        <tr><th>Телеграм</th><td>@inikova</td></tr>
        <tr><th>Город</th><td>Москва, возможны выезды</td></tr>
      </table>
      <p class="bodycopy">Пишите кратко о проекте, сроках и о том, нужны ли вам костюмы, пространства, предметы или весь визуальный мир. Материалы на сайте являются авторскими и не могут быть скопированы без разрешения.</p>
    </section>"""
    (OUT / "contact.html").write_text(
        page("Контакты — Иникова Полина", body, "contact", ""),
        encoding="utf-8",
    )


def write_project(rel: dict) -> None:
    tag = rel["tag"]
    if tag not in TAG_MAP:
        return
    slug, title, year, field, summary = TAG_MAP[tag]

    def rel_img(src: str) -> str:
        return rel_from("projects", src)

    gallery = gallery_html(rel)

    credits = (
        f'<tr><th>Название</th><td>{esc(rel["title"])}</td></tr>'
        f'<tr><th>Год</th><td>{esc(year)}</td></tr>'
        f'<tr><th>Область работы</th><td>{esc(field)}</td></tr>'
        f'<tr><th>Описание</th><td>{esc(rel["description"])}</td></tr>'
    )

    body = f"""<a class="back" href="../index.html">← Назад к проектам</a>
    <h1 class="page-title">{esc(title)}</h1>
    <p class="lede">{esc(summary)}</p>
    <table class="credits">{credits}</table>
    {gallery}"""
    path = PROJECTS_DIR / f"{slug}.html"
    path.write_text(
        page(f"{title} — Иникова Полина", body, "work", "../"),
        encoding="utf-8",
    )


def gallery_html(rel: dict) -> str:
    tag = rel["tag"]
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
        src = f"../portfolio/{tag}/{a['name']}"
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
            f'<a class="cell"><img src="{i["src"]}" alt="{i["cap"]}"><span class="cap">{i["cap"]}</span></a>'
            for i in items
        )
        return f'<div class="col">{cells}</div>'

    def row_html(row_num, bucket):
        main = sorted(bucket["main"], key=lambda x: x["rank"])
        left = col_html(bucket["l"], "stack")
        right = col_html(bucket["r"], "stack")
        main_cells = "".join(
            f'<a class="cell"><img src="{i["src"]}" alt="{i["cap"]}"><span class="cap">{i["cap"]}</span></a>'
            for i in main
        )
        main_zone = f'<div class="main-zone">{main_cells}</div>' if main_cells else ""
        parts = [left, main_zone, right]
        body = "".join(p for p in parts if p)
        return f'<div class="row" data-row="{row_num}">{body}</div>'

    rows_html = "\n".join(row_html(n, rows[n]) for n in sorted(rows))
    return f'<div class="rows">\n{rows_html}\n      </div>'


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