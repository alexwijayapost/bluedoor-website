#!/usr/bin/env python3
"""Build the website files from source/.

Usage: python3 build-site.py            builds preview/  (hidden from search engines, for checking changes)
       python3 build-site.py --live     builds live/     (the public site; only after the owner approves)
Reads source/index.html (the single source of truth for design and copy) and writes
index.html, favicon.svg, .htaccess, assets/three.module.min.js, bench/*.jpg, audio/*.mp3
"""
import pathlib, re, shutil, sys

here = pathlib.Path(__file__).resolve().parent
concept = here / "source"
three = here / "tools" / "three.module.min.js"
live = "--live" in sys.argv
dist = here / ("live" if live else "preview")
if dist.exists():
    shutil.rmtree(dist)
(dist / "assets").mkdir(parents=True)

s = (concept / "index.html").read_text(encoding="utf-8")

def once(a, b):
    global s
    assert s.count(a) == 1, (a[:70], s.count(a))
    s = s.replace(a, b)

# three.js from our own server instead of a CDN
once("https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.min.js", "./assets/three.module.min.js")
shutil.copy(three, dist / "assets" / "three.module.min.js")

# the concept chip is not part of the real site
s, n = re.subn(r'<div class="chip">', '<div class="chip" hidden>', s)
assert n == 1

# no contact form on the site: the contact section has only the WhatsApp and Email us buttons.

# full document head
m = re.search(r'\n(?=<(?:div|header|main|section|a|canvas|svg|button)\b)', s)
head_part, body_part = s[:m.start()], s[m.start():]
head_part = re.sub(r'<title>.*?</title>\n?', '', head_part)
head_part = head_part.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
title = "The Blue Door | Consulting agency for growing businesses"
desc = ("The Blue Door is a consulting agency for small and medium businesses. Marketing, operations and admin, "
        "powered by AI and delivered by people. Business problems in. Solutions out.")
robots = '' if live else '<meta name="robots" content="noindex,nofollow">\n'
head = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}<meta name="theme-color" content="#273462">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://bluedoor.id/">
<style>body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
"""
(dist / "index.html").write_text(head + head_part + "\n</head>\n<body>\n" + body_part + "\n</body>\n</html>\n", encoding="utf-8")

# other files
shutil.copy(concept / "favicon.svg", dist / "favicon.svg")
for rel in sorted(set(re.findall(r'(?:src|poster)="((?:bench|behind-door|img|audio)/[^"]+)"', s))):
    if not (concept / rel).exists():
        print("  WARNING: missing", rel, "(the site works without it, that media is simply absent)")
        continue
    (dist / rel).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(concept / rel, dist / rel)
ht = "Options -Indexes\n<IfModule mod_headers.c>\n"
if not live:
    ht += '  Header set X-Robots-Tag "noindex, nofollow"\n'
ht += ('  <FilesMatch "\\.(js|jpg|jpeg|png|svg|webp|woff2|mp4|mp3)$">\n    Header set Cache-Control "public, max-age=86400"\n  </FilesMatch>\n'
       "</IfModule>\n")
(dist / ".htaccess").write_text(ht)
print("PREVIEW build" if not live else "LIVE build")
for f in sorted(dist.rglob("*")):
    if f.is_file(): print(" ", f.relative_to(dist), f.stat().st_size)
