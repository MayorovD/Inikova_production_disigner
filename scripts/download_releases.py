# -*- coding: utf-8 -*-
"""Download all release assets into portfolio/<release-tag>/ keeping original names."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
TOKEN = ""  # filled at runtime for authenticated downloads of private assets
RELEASES = json.loads((ROOT / "data" / "releases-manifest.json").read_text(encoding="utf-8"))
DST = ROOT / "portfolio"

URLS = []


def collect_urls(releases):
    for rel in releases:
        for asset in rel["assets"]:
            URLS.append(asset["url"])


def download(path: Path, url: str) -> None:
    req = Request(url, headers={"User-Agent": "kilo-portfolio-fetcher", "Authorization": f"Bearer {TOKEN}"})
    with urlopen(req, timeout=120) as src, open(path, "wb") as out:
        while True:
            chunk = src.read(1 << 20)
            if not chunk:
                break
            out.write(chunk)


def main() -> None:
    DST.mkdir(exist_ok=True)
    collect_urls(RELEASES)
    total = 0
    for rel in RELEASES:
        tag_dir = DST / rel["tag"]
        tag_dir.mkdir(exist_ok=True)
        for asset in rel["assets"]:
            name = asset["name"]
            path = tag_dir / name
            if path.exists() and path.stat().st_size == asset["size"]:
                print(f"skip (exists) {rel['tag']}/{name}")
                continue
            download(path, asset["url"])
            total += 1
            print(f"ok {rel['tag']}/{name} {asset['size']/1024/1024:.1f} MB")
    print(f"DONE. downloaded {total} new files")


if __name__ == "__main__":
    main()