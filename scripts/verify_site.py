# -*- coding: utf-8 -*-
from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
pages = [ROOT / "index.html", ROOT / "about.html", ROOT / "contact.html"]
pages += sorted((ROOT / "projects").glob("*.html"))
missing = []
counts = {}
for page in pages:
    html = page.read_text(encoding="utf-8")
    srcs = re.findall(r'(?:src|href)="(?:\.\./)?(portfolio_webp/[^"]+)"', html)
    for rel in srcs:
        if not (ROOT / rel).exists():
            missing.append((page.name, rel))
    counts[page.name] = html.count("<img")

print("pages", len(pages))
print("images", counts)
print("missing", len(missing))
for item in missing[:15]:
    print(" ", item)

for path in ["/", "/about.html", "/contact.html", "/projects/carpet.html", "/css/site.css", "/portfolio/carpet/poster.jpg"]:
    with urllib.request.urlopen("http://127.0.0.1:8765" + path, timeout=10) as response:
        print(path, response.status, response.headers.get("content-type"), "len", response.headers.get("content-length"))
