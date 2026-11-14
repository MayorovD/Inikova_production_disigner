# -*- coding: utf-8 -*-
"""Rename portfolio assets to English web-safe names and write a JSON catalog."""
from __future__ import annotations

import json
import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "портфолио"
DST = ROOT / "portfolio"
DATA_DIR = ROOT / "data"

TRANSLIT = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "e",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "h",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "sch",
    "ъ": "",
    "ы": "y",
    "ь": "",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}

WORD_MAP = {
    "афиша": "poster",
    "афиши": "posters",
    "эскиз": "sketch",
    "эскизы": "sketches",
    "набросок": "draft",
    "наброски": "sketches",
    "финал": "final",
    "финалп": "final-print",
    "готово": "final",
    "печать": "print",
    "копия": "copy",
    "персонажи": "characters",
    "раскадровка": "storyboard",
    "аниматик": "animatic",
    "тизер": "teaser",
    "кадр": "frame",
    "предметы": "props",
    "материал": "material",
    "посох": "staff",
    "полный": "full",
    "шкатулка": "casket",
    "аквамарин": "aquamarine",
    "бабушка": "grandmother",
    "крупно": "closeup",
    "дед": "grandfather",
    "линейка": "lineup",
    "мальчик": "boy",
    "соседка": "neighbor",
    "двор": "yard",
    "день": "day",
    "итог": "final",
    "панорама": "panorama",
    "дом": "house",
    "пластилиновый": "clay",
    "заглавие": "title",
    "сад": "garden",
    "будущего": "of-the-future",
    "ковер": "carpet",
    "птицы": "birds",
    "эдем": "eden",
    "принц": "prince",
    "дамское": "ladies",
    "счастье": "happiness",
    "рейнеке": "reyneke",
    "лис": "fox",
    "искра": "spark",
    "жизни": "of-life",
}

DIR_MAP = {
    "Дамское счастье": "ladies-happiness",
    "Принц Аквамарин": "prince-aquamarine",
    "Птицы": "birds",
    "Рейнеке-лис": "reyneke-fox",
    "Эдем": "eden",
    "искра жизни": "spark-of-life",
    "ковер": "carpet",
    "наброски": "sketches",
    "сад будущего": "garden-of-the-future",
    "эскизы": "sketches",
    "персонажи": "characters",
    "раскадровка": "storyboard",
}

FILE_OVERRIDES = {
    "заглавие.jpg": "title.jpg",
    "заглавие.psd": "title.psd",
    "Дамское счастье.pdf": "ladies-happiness.pdf",
    "афиша.png": "poster.png",
    "эскиз_2.png": "sketch-02.png",
    "эскиз_3.png": "sketch-03.png",
    "эскиз_5.png": "sketch-05.png",
    "эскиз_6.png": "sketch-06.png",
    "эскиз_7.png": "sketch-07.png",
    "Принц Аквамарин.pdf": "prince-aquamarine.pdf",
    "Шкатулка_аквамарин.jpg": "casket-aquamarine.jpg",
    "шкатулка2.jpg": "casket-02.jpg",
    "материал2.jpg": "material-02.jpg",
    "материал3.jpg": "material-03.jpg",
    "материал4.jpg": "material-04.jpg",
    "посох.jpg": "staff.jpg",
    "посох_полный.jpg": "staff-full.jpg",
    "предметы.jpg": "props-01.jpg",
    "предметы2.jpg": "props-02.jpg",
    "1.jpg": "sketch-01.jpg",
    "2.jpg": "sketch-02.jpg",
    "афиша.jpg": "poster.jpg",
    "набросок_эскиз3.jpg": "draft-sketch-03.jpg",
    "набросок_эскиз3_1.jpg": "draft-sketch-03-alt.jpg",
    "набросок_эскиз_1.jpg": "draft-sketch-01.jpg",
    "набросок_эскиз_1_1.jpg": "draft-sketch-01-alt.jpg",
    "набросок_эскиз_2.jpg": "draft-sketch-02.jpg",
    "набросок_эскиз_2_1.jpg": "draft-sketch-02-alt.jpg",
    "эскиз1_ПЕЧАТЬ копия.jpg": "sketch-01-print.jpg",
    "эскиз3_печать копия.jpg": "sketch-03-print.jpg",
    "птицы.pdf": "birds.pdf",
    "э1.jpg": "sketch-01.jpg",
    "э2.jpg": "sketch-02.jpg",
    "э3.jpg": "sketch-03.jpg",
    "э4.jpg": "sketch-04.jpg",
    "э5.jpg": "sketch-05.jpg",
    "э6.jpg": "sketch-06.jpg",
    "э9.jpg": "sketch-09.jpg",
    "э10.jpg": "sketch-10.jpg",
    "э11.jpg": "sketch-11.jpg",
    "Рейнеке-лис.pdf": "reyneke-fox.pdf",
    "набросок_эскиз_4.jpg": "draft-sketch-04.jpg",
    "набросок_эскиз_4_!.jpg": "draft-sketch-04-alt.jpg",
    "набросок_эскиз_6.jpg": "draft-sketch-06.jpg",
    "набросок_эскиз_7.jpg": "draft-sketch-07.jpg",
    "эскиз_1_ГОТОВО.jpg": "sketch-01-final.jpg",
    "эскиз_2_ГОТОВО.jpg": "sketch-02-final.jpg",
    "эскиз_3_ГОТОВО.jpg": "sketch-03-final.jpg",
    "эскиз_4_ГОТОВО.jpg": "sketch-04-final.jpg",
    "эскиз_5_ГОТОВО.jpg": "sketch-05-final.jpg",
    "эскиз_6_ГОТОВО.jpg": "sketch-06-final.jpg",
    "эскиз_7_ГОТОВО.jpg": "sketch-07-final.jpg",
    "эскиз_8_ГОТОВО.jpg": "sketch-08-final.jpg",
    "Эдем.pdf": "eden.pdf",
    "Эскиз-3.jpg": "sketch-03.jpg",
    "Эскиз1.jpg": "sketch-01.jpg",
    "Эскиз4.jpg": "sketch-04.jpg",
    "Эскиз5.jpg": "sketch-05.jpg",
    "Эскиз6.jpg": "sketch-06.jpg",
    "Эскиз8.jpg": "sketch-08.jpg",
    "искра жизни.pdf": "spark-of-life.pdf",
    "1_финалП.jpg": "final-01-print.jpg",
    "2_финал.jpg": "final-02.jpg",
    "3_финал.jpg": "final-03.jpg",
    "4_финал.jpg": "final-04.jpg",
    "ковер.pdf": "carpet.pdf",
    "аниматик_финал.mp4": "animatic-final.mp4",
    "тизер2.mp4": "teaser-02.mp4",
    "афиша1.jpg": "poster.jpg",
    "раскадровка_.jpg": "storyboard-overview.jpg",
    "Э_Двор_день_Итог.jpg": "environment-yard-day-final.jpg",
    "Э_Дом_соседки_Итог.jpg": "environment-neighbor-house-final.jpg",
    "Э_Панорама_двор_Итог.jpg": "environment-yard-panorama-final.jpg",
    "pel.jpg": "still-pel.jpg",
    "Бабушка_крупно1.jpg": "grandmother-closeup.jpg",
    "Дед.jpg": "grandfather.jpg",
    "Линейка1.jpg": "lineup-01.jpg",
    "Линейка2.jpg": "lineup-02.jpg",
    "Мальчик1.jpg": "boy-01.jpg",
    "Мальчик2.jpg": "boy-02.jpg",
    "Мальчик3.jpg": "boy-03.jpg",
    "Соседка.jpg": "neighbor.jpg",
    "бабушка.jpg": "grandmother.jpg",
    "бабушка1.jpg": "grandmother-02.jpg",
    "сад будущего.pdf": "garden-of-the-future.pdf",
    "АФИШИ_наброски.jpg": "poster-drafts.jpg",
    "пластилиновый эскиз.jpg": "clay-sketch.jpg",
    "кадр_4.jpg": "frame-04.jpg",
    "кадр_5.jpg": "frame-05.jpg",
    "кадр_9.jpg": "frame-09.jpg",
    "panorama_kiberpank.jpg": "panorama-cyberpunk.jpg",
    "J59f7zog914.jpg": "concept-sky.jpg",
    "luk.jpg": "onion.jpg",
    "podem.jpg": "ascent.jpg",
    "end.jpg": "ending.jpg",
    "saray.jpg": "barn.jpg",
    "sun.jpg": "sun.jpg",
}

STILL_NUMBERS = {"16.jpg", "27.jpg", "35.jpg", "36.jpg", "38.jpg", "52.jpg", "56.jpg", "82.jpg"}

PROJECTS = [
    {
        "id": "carpet",
        "title": "The Carpet",
        "titleRu": "Ковер",
        "kind": "animation-film",
        "role": "production designer",
    },
    {
        "id": "garden-of-the-future",
        "title": "Garden of the Future",
        "titleRu": "Сад будущего",
        "kind": "animation-film",
        "role": "production designer",
    },
    {
        "id": "spark-of-life",
        "title": "Spark of Life",
        "titleRu": "Искра жизни",
        "kind": "costume-production",
        "role": "production designer",
    },
    {
        "id": "eden",
        "title": "Eden",
        "titleRu": "Эдем",
        "kind": "costume-production",
        "role": "production designer",
    },
    {
        "id": "reyneke-fox",
        "title": "Reyneke the Fox",
        "titleRu": "Рейнеке-лис",
        "kind": "costume-production",
        "role": "production designer",
    },
    {
        "id": "prince-aquamarine",
        "title": "Prince Aquamarine",
        "titleRu": "Принц Аквамарин",
        "kind": "costume-props",
        "role": "production designer",
    },
    {
        "id": "ladies-happiness",
        "title": "Ladies' Happiness",
        "titleRu": "Дамское счастье",
        "kind": "costume-production",
        "role": "production designer",
    },
    {
        "id": "birds",
        "title": "Birds",
        "titleRu": "Птицы",
        "kind": "costume-production",
        "role": "production designer",
    },
    {
        "id": "sketches",
        "title": "Sketches",
        "titleRu": "Наброски",
        "kind": "sketchbook",
        "role": "artist",
    },
]


def slugify_token(token: str) -> str:
    t = token.lower().strip()
    if t in WORD_MAP:
        return WORD_MAP[t]
    out = []
    for ch in t:
        if ch in TRANSLIT:
            out.append(TRANSLIT[ch])
        else:
            out.append(ch)
    return "".join(out)


def slugify_name(name: str) -> str:
    stem, ext = os.path.splitext(name)
    stem = stem.replace("ё", "е")
    parts = re.split(r"[_\s\-]+", stem)
    slugged = [slugify_token(p) for p in parts if p]
    joined = "-".join(slugged)
    joined = re.sub(r"[^a-z0-9.-]+", "-", joined.lower())
    joined = re.sub(r"-{2,}", "-", joined).strip("-.")
    ext = ext.lower()
    if not joined:
        joined = "file"
    return joined + ext


def pad_storyboard(name: str) -> str:
    stem, ext = os.path.splitext(name)
    stem = stem.replace(",", ".").replace(" ", "")
    if stem.endswith("-"):
        stem = stem[:-1] + "-alt"
    m = re.fullmatch(r"(\d+)(?:\.(\d+))?(?:-alt)?", stem)
    if not m:
        return slugify_name(name)
    num = int(m.group(1))
    frac = m.group(2)
    alt = stem.endswith("-alt")
    out = f"{num:03d}"
    if frac:
        out += f"-{frac}"
    if alt:
        out += "-alt"
    return out + ext.lower()


def unique_name(directory: Path, name: str) -> str:
    candidate = directory / name
    if not candidate.exists():
        return name
    stem, ext = os.path.splitext(name)
    i = 2
    while True:
        alt = f"{stem}-{i}{ext}"
        if not (directory / alt).exists():
            return alt
        i += 1


def copy_tree() -> dict[str, str]:
    if not SRC.exists():
        raise SystemExit(f"Source folder not found: {SRC}")
    if DST.exists():
        shutil.rmtree(DST)
    mapping: dict[str, str] = {}
    for dirpath, dirnames, filenames in os.walk(SRC):
        rel = Path(dirpath).relative_to(SRC)
        new_parts = [DIR_MAP.get(part, slugify_name(part)) for part in rel.parts]
        dest_dir = DST.joinpath(*new_parts) if new_parts else DST
        dest_dir.mkdir(parents=True, exist_ok=True)
        for filename in filenames:
            src_file = Path(dirpath) / filename
            parts = Path(dirpath).parts
            if "раскадровка" in parts:
                new_name = pad_storyboard(filename)
            elif filename in STILL_NUMBERS and "ковер" in parts and "персонажи" not in parts:
                new_name = f"still-{int(os.path.splitext(filename)[0]):02d}.jpg"
            elif "наброски" in parts and re.fullmatch(r"\d+\.(jpg|jpeg|png)", filename, re.I):
                new_name = filename  # sequential names applied after copy
            elif filename.lower().startswith("скан_"):
                new_name = slugify_name(filename.replace("Скан_", "scan-").replace("скан_", "scan-"))
                new_name = new_name.replace("(", "").replace(")", "")
                new_name = re.sub(r"-{2,}", "-", new_name)
            elif filename in FILE_OVERRIDES:
                new_name = FILE_OVERRIDES[filename]
            else:
                new_name = slugify_name(filename)
            new_name = unique_name(dest_dir, new_name)
            dest_file = dest_dir / new_name
            shutil.copy2(src_file, dest_file)
            mapping[str(src_file.relative_to(ROOT)).replace("\\", "/")] = str(dest_file.relative_to(ROOT)).replace("\\", "/")
    sketches_dir = DST / "sketches"
    if sketches_dir.exists():
        numbered = sorted(
            [p for p in sketches_dir.iterdir() if p.is_file() and re.fullmatch(r"\d+\.(jpg|jpeg|png)", p.name, re.I)],
            key=lambda p: p.name,
        )
        for i, path in enumerate(numbered, start=1):
            new_path = sketches_dir / f"sketch-{i:02d}{path.suffix.lower()}"
            path.rename(new_path)
            old_rel = str(path.relative_to(ROOT)).replace("\\", "/")
            new_rel = str(new_path.relative_to(ROOT)).replace("\\", "/")
            for src, dst in list(mapping.items()):
                if dst == old_rel:
                    mapping[src] = new_rel
    return mapping


def kind_for(path: str) -> str:
    lower = path.lower()
    name = Path(path).name.lower()
    if name.endswith(".pdf"):
        return "pdf"
    if name.endswith(".mp4"):
        return "video"
    if name.endswith(".psd"):
        return "source"
    if "poster" in name:
        return "poster"
    if "/characters/" in lower:
        return "character"
    if "/storyboard/" in lower or "storyboard" in name:
        return "storyboard"
    if name.startswith("environment-"):
        return "environment"
    if name.startswith("still-"):
        return "still"
    if name.startswith("frame-") or name.startswith("teaser") or "animatic" in name:
        return "film"
    if "draft" in name or "/sketches/" in lower or name.startswith("sketch-") or "clay" in name:
        return "sketch"
    if "prop" in name or "casket" in name or "staff" in name or "material" in name:
        return "prop"
    return "image"


def caption_for(path: str) -> str:
    stem = Path(path).stem.replace("-", " ")
    return stem[:1].upper() + stem[1:] if stem else ""


def build_catalog() -> dict:
    web_ext = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".mp4", ".pdf"}
    projects = []
    for meta in PROJECTS:
        folder = DST / meta["id"]
        assets = []
        poster = None
        pdf = None
        videos = []
        if folder.exists():
            for file in sorted(folder.rglob("*")):
                if not file.is_file():
                    continue
                if file.suffix.lower() not in web_ext:
                    continue
                rel = str(file.relative_to(ROOT)).replace("\\", "/")
                k = kind_for(rel)
                item = {
                    "src": rel,
                    "kind": k,
                    "caption": caption_for(rel),
                }
                if k == "poster":
                    name = file.name.lower()
                    if name in {"poster.jpg", "poster.jpeg", "poster.png", "poster.webp"}:
                        poster = rel
                    elif poster is None:
                        poster = rel
                if k == "pdf" and pdf is None:
                    pdf = rel
                if k == "video":
                    videos.append(rel)
                assets.append(item)
        if poster is None:
            images = [a["src"] for a in assets if a["kind"] not in {"pdf", "video", "source"}]
            poster = images[0] if images else None
        projects.append(
            {
                **meta,
                "folder": str((DST / meta["id"]).relative_to(ROOT)).replace("\\", "/"),
                "poster": poster,
                "pdf": pdf,
                "videos": videos,
                "assets": assets,
            }
        )
    title = DST / "title.jpg"
    table = [
        {
            "id": p["id"],
            "poster": p["poster"],
            "title": p["title"],
            "titleRu": p["titleRu"],
            "kind": p["kind"],
            "role": p["role"],
            "pdf": p["pdf"],
            "videos": len(p["videos"]),
            "assets": len(p["assets"]),
            "folder": p["folder"],
        }
        for p in projects
    ]
    return {
        "site": {
            "title": "Inikova — production designer",
            "cover": str(title.relative_to(ROOT)).replace("\\", "/") if title.exists() else None,
        },
        "table": table,
        "projects": projects,
    }


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    if SRC.exists():
        mapping = copy_tree()
        (DATA_DIR / "rename-map.json").write_text(
            json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"copied {len(mapping)} files")
        if DST.exists():
            shutil.rmtree(SRC)
            print(f"removed original folder {SRC.name}")
    catalog = build_catalog()
    (DATA_DIR / "portfolio.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"projects {len(catalog['projects'])}")
    print(f"wrote {DATA_DIR / 'portfolio.json'}")


if __name__ == "__main__":
    main()
