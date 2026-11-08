#!/usr/bin/env python3
"""Build Marketcube's four static pages from the combined single-file view.

Pages: index.html (clients), investors.html, team.html, concept.html
(bold skin, client content). Shared CSS/JS; header nav links instead of
the audience switcher. Run: python3 build.py  (expects the combined
source kept in source.html)
"""
import re

html = open("source.html").read()
css = re.search(r"<style>(.*?)</style>", html, re.S).group(1)
script = re.search(r"<script>(.*?)</script>", html, re.S).group(1)

i_c = html.index('<div data-for="c">')
i_i = html.index('<div data-for="i"')
i_t = html.index('<div data-for="t"')
i_end = html.index("</main>")
client = html[i_c:i_i]
investors = html[i_i:i_t].replace('<div data-for="i" hidden>', '<div data-for="i">')
team = html[i_t:i_end].replace('<div data-for="t" hidden>', '<div data-for="t">')

# split script: keep the helper, drop the switcher machinery, keep the rest
head = script[: script.index("const views=")]
tail = script[script.index("const T={"):]
tail = tail.replace("setView('client');\n", "")
# the pre-launch checklist only exists on the team page; guard it
tail = tail.replace(
    "const ck=document.getElementById('ck');",
    "const ck=document.getElementById('ck');if(ck){")
tail = tail.replace("document.getElementById('bar').style.width=p+'%'}upd();",
                    "document.getElementById('bar').style.width=p+'%'}upd();}")
script = head + tail

PAGES = [
    ("index.html", client, "", "Clients"),
    ("investors.html", investors, "", "Investors and partners"),
    ("team.html", team, "", "Team"),
    ("concept.html", client, ' data-skin="bold"', "Visual concept"),
]

for fname, body, skin, active in PAGES:
    page = f"""<!DOCTYPE html>
<html lang="en"{skin}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Marketcube | Growth, engineered</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
<header><div class="w">
<div class="bar"><a class="logo" href="index.html"><svg width="26" height="26" viewBox="0 0 26 26" fill="none" stroke="var(--acc)" stroke-width="1.6"><path d="M13 2l9.5 5.5v11L13 24 3.5 18.5v-11z"/><path d="M13 13l9.5-5.5M13 13L3.5 7.5M13 13v11"/></svg>Marketcube</a><span style="font-size:12px;color:var(--mute);letter-spacing:.14em">ABUJA, NIGERIA</span></div>
</div></header>
<main id="top">
{body}
</main>
<footer><div class="w"><span>Marketcube. Growth, engineered.</span><span>Abuja, Nigeria</span></div></footer>
<script>{script}</script>
</body>
</html>"""
    open(fname, "w").write(page)
    print("built", fname)
