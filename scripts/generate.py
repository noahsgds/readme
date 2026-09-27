"""Génère les visuels SVG du profil GitHub (thème Nord / VS Code du portfolio).

    python scripts/generate.py            # visuels statiques -> assets/
    python scripts/generate.py --stats    # stats live via l'API GitHub -> dist/

Aucune dépendance externe : uniquement la bibliothèque standard.
"""

import datetime as dt
import json
import math
import os
import sys
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).parent))
import profile_data as P  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# Palette Nord reprise de themes.css du portfolio
BG_DEEP = "#1e222a"
BG_TITLE = "#252932"
BG = "#2E3440"
BG_2 = "#3B4252"
BG_3 = "#434C5E"
MUTED = "#616E88"
TEXT = "#ECEFF4"
TEXT_2 = "#D8DEE9"
ACCENT = "#88C0D0"
NAME = "#BF616A"
BLUE = "#81A1C1"
GREEN = "#A3BE8C"
YELLOW = "#EBCB8B"
ORANGE = "#D08770"
PURPLE = "#B48EAD"

SANS = "'Segoe UI', Ubuntu, -apple-system, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', Consolas, Menlo, 'Courier New', monospace"
MEDAL = {1: "🥇", 2: "🥈", 3: "🥉"}
RANK_LABEL = {1: "1ère place", 2: "2ème place", 3: "3ème place"}
RANK_COLOR = {1: YELLOW, 2: "#C0C5CE", 3: ORANGE}


def e(text):
    return escape(str(text), {'"': "&quot;"})


def svg(width, height, body, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{e(title)}">'
        f"<title>{e(title)}</title>{body}</svg>\n"
    )


def text_width(text, size, mono=False):
    """Largeur approximative d'un texte (pas de mesure de police dans un SVG statique)."""
    if mono:
        return len(text) * size * 0.6
    wide = sum(1 for c in text if c.isupper() or c in "mwMW%@#")
    return (len(text) - wide) * size * 0.52 + wide * size * 0.68


def wrap(text, size, max_width):
    lines, line = [], ""
    for word in text.split():
        candidate = f"{line} {word}".strip()
        if text_width(candidate, size) > max_width and line:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines


def pill(x, y, label, color, size=11, fill_opacity=0.14):
    w = text_width(label, size) + 16
    return (
        f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{size + 9}" rx="{(size + 9) / 2}" '
        f'fill="{color}" fill-opacity="{fill_opacity}" stroke="{color}" stroke-opacity="0.45"/>'
        f'<text x="{x + w / 2:.0f}" y="{y + size + 3}" text-anchor="middle" font-family="{SANS}" '
        f'font-size="{size}" font-weight="600" fill="{color}">{e(label)}</text>'
    ), w


def window_chrome(width, height, filename, tabs=None):
    """Cadre de fenêtre VS Code : barre de titre, onglets, fond d'éditeur."""
    parts = [
        f'<rect width="{width}" height="{height}" rx="12" fill="{BG}"/>',
        f'<path d="M12 0h{width - 24}a12 12 0 0 1 12 12v24H0V12A12 12 0 0 1 12 0z" fill="{BG_TITLE}"/>',
        f'<circle cx="22" cy="18" r="6" fill="#BF616A"/>',
        f'<circle cx="42" cy="18" r="6" fill="#EBCB8B"/>',
        f'<circle cx="62" cy="18" r="6" fill="#A3BE8C"/>',
        f'<text x="{width / 2}" y="22" text-anchor="middle" font-family="{SANS}" font-size="12" '
        f'fill="{MUTED}">{e(filename)} — noah-segonds</text>',
    ]
    if tabs:
        parts.append(f'<rect y="36" width="{width}" height="32" fill="{BG_TITLE}"/>')
        x = 0
        for i, (label, color) in enumerate(tabs):
            w = text_width(label, 12, mono=True) + 44
            active = i == 0
            parts.append(
                f'<rect x="{x}" y="36" width="{w:.0f}" height="32" fill="{BG if active else BG_TITLE}"/>'
            )
            if active:
                parts.append(f'<rect x="{x}" y="36" width="{w:.0f}" height="2" fill="{ACCENT}"/>')
            parts.append(f'<circle cx="{x + 16}" cy="52" r="4" fill="{color}"/>')
            parts.append(
                f'<text x="{x + 28}" y="56" font-family="{MONO}" font-size="12" '
                f'fill="{TEXT if active else MUTED}">{e(label)}</text>'
            )
            x += w
    parts.append(f'<rect width="{width}" height="{height}" rx="12" fill="none" stroke="{BG_2}"/>')
    return "".join(parts)


# --------------------------------------------------------------------------- header
def header():
    W, H = 880, 330
    tabs = [("README.md", ACCENT), ("about.html", ORANGE), ("projects.js", YELLOW),
            ("experience.ts", BLUE), ("skills.json", GREEN)]
    body = [window_chrome(W, H, "README.md", tabs)]
    body.append(
        "<style>"
        "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}"
        ".cur{animation:blink 1s step-end infinite}"
        "@keyframes rise{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}"
        ".r1{animation:rise .6s ease-out}.r2{animation:rise .9s ease-out}"
        ".r3{animation:rise 1.2s ease-out}.r4{animation:rise 1.5s ease-out}"
        "@keyframes glow{0%,100%{opacity:.35}50%{opacity:.7}}.glow{animation:glow 4s ease-in-out infinite}"
                        "</style>"
    )
    # numéros de ligne
    for i in range(1, 10):
        body.append(
            f'<text x="34" y="{84 + i * 22}" text-anchor="end" font-family="{MONO}" '
            f'font-size="12" fill="{BG_3}">{i}</text>'
        )
    body.append(
        f'<text class="r1" x="54" y="106" font-family="{MONO}" font-size="13" fill="{MUTED}">'
        f"// hello world !! Welcome to my GitHub</text>"
    )
    body.append(
        f'<text class="r1" x="54" y="136" font-family="{MONO}" font-size="16" fill="{ACCENT}">'
        f"&gt; Hello, I'm</text>"
    )
    body.append(
        f'<text class="r2" x="52" y="194" font-family="{SANS}" font-size="56" font-weight="800" '
        f'letter-spacing="-1"><tspan fill="{TEXT}">{e(P.NAME_FIRST)} </tspan>'
        f'<tspan fill="{NAME}">{e(P.NAME_LAST)}</tspan></text>'
    )

    # rôles tapés au clavier, en boucle (SMIL)
    n = len(P.ROLES)
    per = 3.2
    total = per * n
    y = 238
    body.append(
        f'<text class="r3" x="54" y="{y}" font-family="{MONO}" font-size="18" fill="{PURPLE}">const</text>'
        f'<text class="r3" x="120" y="{y}" font-family="{MONO}" font-size="18" fill="{TEXT_2}">role =</text>'
    )
    x0 = 200
    for i, role in enumerate(P.ROLES):
        label = f'"{role}"'
        w = text_width(label, 18, mono=True)
        start, end = i / n, (i + 1) / n
        seg = end - start
        kt = [0, start, start + seg * 0.35, start + seg * 0.85, end, 1]
        kt = sorted(set(round(k, 4) for k in kt))
        # largeur du masque : 0 -> w (frappe) -> w (pause) -> 0 (effacement)
        vals = {0: 0, round(start, 4): 0, round(start + seg * 0.35, 4): w,
                round(start + seg * 0.85, 4): w, round(end, 4): 0, 1: 0}
        values = ";".join(f"{vals[k]:.0f}" for k in kt)
        key_times = ";".join(str(k) for k in kt)
        body.append(
            f'<clipPath id="role{i}"><rect x="{x0}" y="{y - 20}" height="28" width="0">'
            f'<animate attributeName="width" dur="{total}s" repeatCount="indefinite" '
            f'values="{values}" keyTimes="{key_times}" calcMode="linear"/></rect></clipPath>'
            f'<text clip-path="url(#role{i})" x="{x0}" y="{y}" font-family="{MONO}" font-size="18" '
            f'fill="{GREEN}">{e(label)}</text>'
        )
        # curseur qui suit la frappe
        body.append(
            f'<rect class="cur" x="{x0}" y="{y - 16}" width="9" height="20" fill="{ACCENT}" opacity="0">'
            f'<animate attributeName="x" dur="{total}s" repeatCount="indefinite" '
            f'values="{";".join(f"{x0 + vals[k] + 2:.0f}" for k in kt)}" keyTimes="{key_times}"/>'
            f'<animate attributeName="opacity" dur="{total}s" repeatCount="indefinite" calcMode="discrete" '
            f'values="0;1;0" keyTimes="0;{round(start, 4)};{round(end, 4)}"/></rect>'
        )

    body.append(
        f'<text class="r4" x="54" y="276" font-family="{MONO}" font-size="13" fill="{MUTED}">'
        f"/* MSc Business Analytics @ Eugenia School · Major de promo 🏆 */</text>"
    )

    # décor à droite : orbites de technos
    body.append(f'<circle class="glow" cx="735" cy="185" r="92" fill="{ACCENT}" fill-opacity="0.06"/>')
    body.append(f'<circle cx="735" cy="185" r="88" fill="none" stroke="{BG_2}" stroke-dasharray="4 6"/>')
    body.append(f'<circle cx="735" cy="185" r="56" fill="none" stroke="{BG_2}" stroke-dasharray="3 5"/>')
    body.append(
        f'<text x="735" y="194" text-anchor="middle" font-family="{MONO}" font-size="26" '
        f'font-weight="700" fill="{ACCENT}">&lt;NS/&gt;</text>'
    )
    outer = [("Python", "#3776AB"), ("SQL", "#336791"), ("Power BI", "#F2C811"), ("Dust", "#E5E9F0")]
    inner = [("n8n", "#EA4B71"), ("Make", "#6D00CC"), ("Databricks", "#FF3621")]
    for items, r, dur, direction in ((outer, 88, 28, 1), (inner, 56, 18, -1)):
        sweep = 1 if direction > 0 else 0
        path = (f"M{735 + r},185 A{r},{r} 0 1,{sweep} {735 - r},185 "
                f"A{r},{r} 0 1,{sweep} {735 + r},185")
        for k, (label, color) in enumerate(items):
            w = text_width(label, 10) + 14
            offset = -dur * k / len(items)
            body.append(
                f'<g><rect x="{-w / 2:.1f}" y="-10" width="{w:.0f}" height="20" rx="10" '
                f'fill="{BG_TITLE}" stroke="{color}"/>'
                f'<text y="4" text-anchor="middle" font-family="{SANS}" font-size="10" '
                f'font-weight="700" fill="{TEXT_2}">{e(label)}</text>'
                f'<animateMotion dur="{dur}s" begin="{offset:.2f}s" repeatCount="indefinite" '
                f'path="{path}"/></g>'
            )

    # barre de statut
    body.append(f'<path d="M0 {H - 26}h{W}v14a12 12 0 0 1-12 12H12A12 12 0 0 1 0 {H - 12}z" fill="{BG_2}"/>')
    body.append(f'<rect y="{H - 26}" width="92" height="26" fill="#5E81AC"/>')
    body.append(
        f'<text x="12" y="{H - 9}" font-family="{MONO}" font-size="11" fill="{TEXT}">⎇ main ✓</text>'
        f'<text x="106" y="{H - 9}" font-family="{MONO}" font-size="11" fill="{TEXT_2}">'
        f"● Data Analyst @ Decathlon   ◆ Eugenia School   ✉ {e(P.EMAIL)}</text>"
        f'<text x="{W - 14}" y="{H - 9}" text-anchor="end" font-family="{MONO}" font-size="11" '
        f'fill="{TEXT_2}">UTF-8  TypeScript  Nord</text>'
    )
    return svg(W, H, "".join(body), "Noah Segonds — Data Analyst, Business Analyst, Chef de Projet IA")


# --------------------------------------------------------------------------- chiffres clés
def highlights():
    W, H = 880, 110
    n = len(P.HIGHLIGHTS)
    gap = 12
    cw = (W - gap * (n - 1)) / n
    body = [
        "<style>@keyframes pop{0%{opacity:0;transform:translateY(10px) scale(.96)}"
        "100%{opacity:1;transform:none}}.t{animation:pop .7s ease-out}</style>"
    ]
    for i, (value, label, color) in enumerate(P.HIGHLIGHTS):
        x = i * (cw + gap)
        body.append(
            f'<g class="t" style="animation-duration:{0.6 + i * 0.2:.1f}s">'
            f'<rect x="{x:.1f}" y="1" width="{cw:.1f}" height="{H - 2}" rx="12" fill="{BG}" stroke="{BG_2}"/>'
            f'<rect x="{x:.1f}" y="1" width="{cw:.1f}" height="3" rx="1.5" fill="{color}"/>'
            f'<text x="{x + cw / 2:.1f}" y="58" text-anchor="middle" font-family="{SANS}" '
            f'font-size="34" font-weight="800" fill="{color}">{e(value)}</text>'
            f'<text x="{x + cw / 2:.1f}" y="86" text-anchor="middle" font-family="{SANS}" '
            f'font-size="12" fill="{TEXT_2}">{e(label)}</text></g>'
        )
    return svg(W, H, "".join(body), "Chiffres clés")


# --------------------------------------------------------------------------- cartes hackathon
def hackathon_card(h):
    W, H = 430, 230
    c1, c2 = h["cover"]
    body = [
        f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>'
        f'<clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath></defs>',
        "<style>@keyframes in{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}"
        ".a{animation:in .7s ease-out}.b{animation:in 1s ease-out}"
        "@keyframes shine{0%{transform:translateX(-200px)}60%,100%{transform:translateX(560px)}}"
        ".s{animation:shine 5s ease-in-out infinite}</style>",
        f'<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="{BG}"/>',
        f'<rect width="{W}" height="64" fill="url(#g)"/>',
        f'<rect class="s" x="0" y="0" width="60" height="64" fill="#fff" fill-opacity="0.12" '
        f'transform="skewX(-20)"/>',
        f'<text x="18" y="44" font-size="28">{h["icon"]}</text>',
    ]
    medal_label = f'{MEDAL[h["rank"]]} {RANK_LABEL[h["rank"]]}'
    mw = text_width(medal_label, 12) + 24
    body.append(
        f'<rect x="{W - mw - 14:.0f}" y="18" width="{mw:.0f}" height="28" rx="14" fill="{BG_DEEP}" '
        f'fill-opacity="0.55"/>'
        f'<text x="{W - 14 - mw / 2:.0f}" y="37" text-anchor="middle" font-family="{SANS}" '
        f'font-size="12" font-weight="700" fill="{RANK_COLOR[h["rank"]]}">{e(medal_label)}</text>'
    )
    body.append(
        f'<text x="62" y="30" font-family="{MONO}" font-size="10" fill="#fff" fill-opacity="0.85" '
        f'letter-spacing="1">{e(" · ".join(h["categories"]))}</text>'
        f'<text x="62" y="47" font-family="{MONO}" font-size="11" fill="#fff" fill-opacity="0.95">'
        f"Chef de Projet</text>"
    )
    body.append(
        f'<g class="a"><text x="18" y="90" font-family="{SANS}" font-size="16" font-weight="700" '
        f'fill="{TEXT}">{e(h["title"])}</text>'
        f'<text x="18" y="108" font-family="{MONO}" font-size="11" fill="{MUTED}">'
        f'// {e(h["period"])}</text></g>'
    )
    body.append('<g class="b">')
    for k, line in enumerate(wrap(h["desc"], 12.5, W - 36)[:4]):
        body.append(
            f'<text x="18" y="{130 + k * 17}" font-family="{SANS}" font-size="12.5" '
            f'fill="{TEXT_2}">{e(line)}</text>'
        )
    body.append("</g>")
    x = 18
    for tag in h["tags"]:
        p, w = pill(x, H - 32, tag, c1, size=10)
        if x + w > W - 18:
            break
        body.append(p)
        x += w + 6
    if h["url"]:
        body.append(
            f'<text x="{W - 16}" y="{H - 17}" text-anchor="end" font-family="{MONO}" font-size="11" '
            f'fill="{ACCENT}">open ↗</text>'
        )
    body.append(f'</g><rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" '
                f'stroke="{BG_2}"/>')
    return svg(W, H, "".join(body), f'{h["title"]} — {RANK_LABEL[h["rank"]]}')


def trophies():
    W, H = 880, 64
    gold = sum(1 for h in P.HACKATHONS if h["rank"] == 1)
    silver = sum(1 for h in P.HACKATHONS if h["rank"] == 2)
    bronze = sum(1 for h in P.HACKATHONS if h["rank"] == 3)
    body = [
        "<style>@keyframes b{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}"
        ".m{animation:b 2.4s ease-in-out infinite}</style>",
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="{BG}" stroke="{BG_2}"/>',
        f'<text x="22" y="38" font-family="{MONO}" font-size="14" fill="{MUTED}">'
        f'<tspan fill="{PURPLE}">const</tspan> <tspan fill="{TEXT_2}">palmares</tspan> = </text>',
    ]
    x = 230
    for i, (emoji, count, label, color) in enumerate(
        ((MEDAL[1], gold, "victoires", YELLOW), (MEDAL[2], silver, "2ème place", "#C0C5CE"),
         (MEDAL[3], bronze, "3èmes places", ORANGE))
    ):
        body.append(
            f'<g class="m" style="animation-delay:{i * 0.3}s"><text x="{x}" y="42" font-size="26">{emoji}</text></g>'
            f'<text x="{x + 38}" y="41" font-family="{SANS}" font-size="24" font-weight="800" '
            f'fill="{color}">{count}</text>'
            f'<text x="{x + 60}" y="40" font-family="{SANS}" font-size="13" fill="{TEXT_2}">{e(label)}</text>'
        )
        x += 200
    return svg(W, H, "".join(body), f"Palmarès : {gold} victoires, {silver} deuxième, {bronze} troisièmes")


# --------------------------------------------------------------------------- expérience
def experience():
    W = 880
    row = 104
    H = 76 + row * len(P.EXPERIENCES)
    body = [
        "<style>@keyframes in{from{opacity:0;transform:translateX(14px)}to{opacity:1;transform:none}}"
        ".r{animation:in .7s ease-out}"
        "@keyframes pulse{0%{r:7;opacity:.9}100%{r:18;opacity:0}}.p{animation:pulse 1.6s ease-out infinite}"
        "@keyframes draw{from{stroke-dashoffset:1000}to{stroke-dashoffset:0}}"
        ".l{stroke-dasharray:1000;animation:draw 2.5s ease-out}</style>",
        window_chrome(W, H, "experience.ts"),
        f'<text x="24" y="60" font-family="{MONO}" font-size="12" fill="{MUTED}">'
        f'<tspan fill="{PURPLE}">interface</tspan> <tspan fill="{YELLOW}">Career</tspan> '
        f'<tspan fill="{PURPLE}">extends</tspan> <tspan fill="{YELLOW}">Timeline</tspan> {{}}</text>',
        f'<line class="l" x1="40" y1="82" x2="40" y2="{H - 30}" stroke="{BG_3}" stroke-width="2"/>',
    ]
    for i, exp in enumerate(P.EXPERIENCES):
        y = 88 + i * row
        body.append(f'<g class="r" style="animation-duration:{0.6 + i * 0.25:.2f}s">')
        if exp["current"]:
            body.append(f'<circle class="p" cx="40" cy="{y + 8}" r="7" fill="{exp["color"]}"/>')
        body.append(
            f'<circle cx="40" cy="{y + 8}" r="7" fill="{BG}" stroke="{exp["color"]}" stroke-width="3"/>'
            f'<text x="66" y="{y + 12}" font-family="{MONO}" font-size="11" fill="{MUTED}">'
            f'{e(exp["period"])}</text>'
            f'<text x="66" y="{y + 34}" font-family="{SANS}" font-size="16" font-weight="700" '
            f'fill="{TEXT}">{e(exp["title"])}</text>'
            f'<text x="66" y="{y + 54}" font-family="{SANS}" font-size="13" font-weight="700" '
            f'fill="{exp["color"]}">@ {e(exp["company"])}</text>'
        )
        tw = text_width("@ " + exp["company"], 13) + 76
        p, _ = pill(tw, y + 42, exp["type"], exp["color"], size=10)
        body.append(p)
        body.append(
            f'<text x="66" y="{y + 76}" font-family="{SANS}" font-size="12.5" fill="{TEXT_2}">'
            f'{e(exp["line"])}</text>'
        )
        x = W - 20
        for tag in reversed(exp["tags"][:4]):
            w = text_width(tag, 10) + 16
            x -= w
            p, _ = pill(x, y + 2, tag, BLUE, size=10)
            body.append(p)
            x -= 6
        if exp["current"]:
            body.append(
                f'<text x="{text_width(exp["title"], 16) + 76:.0f}" y="{y + 33}" font-family="{MONO}" '
                f'font-size="10" fill="{GREEN}">● EN COURS</text>'
            )
        body.append("</g>")
    return svg(W, H, "".join(body), "Parcours professionnel")


# --------------------------------------------------------------------------- compétences
def skills():
    W = 880
    col_w = 400
    colors = [GREEN, YELLOW, ORANGE, BLUE, PURPLE, ACCENT]
    cols = [P.SKILLS[:3], P.SKILLS[3:]]
    heights = [sum(38 + 30 * len(s) for _, s in col) for col in cols]
    H = 90 + max(heights)
    body = ["<style>@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
            ".bar{transform-box:fill-box;transform-origin:left;animation:grow 1.4s cubic-bezier(.2,.8,.2,1)}</style>",
            window_chrome(W, H, "skills.json"),
            f'<text x="24" y="60" font-family="{MONO}" font-size="12" fill="{MUTED}">'
            f'{{ <tspan fill="{ACCENT}">"status"</tspan>: <tspan fill="{GREEN}">"always_learning"</tspan>, '
            f'<tspan fill="{ACCENT}">"passion"</tspan>: <tspan fill="{GREEN}">"immeasurable"</tspan> }}</text>']
    delay = 0.0
    for c, col in enumerate(cols):
        x0 = 28 + c * (col_w + 36)
        y = 96
        for title, items in col:
            body.append(
                f'<text x="{x0}" y="{y}" font-family="{MONO}" font-size="11" font-weight="700" '
                f'letter-spacing="1.5" fill="{MUTED}">{e(title)}</text>'
            )
            y += 22
            for k, (name, pct) in enumerate(items):
                color = colors[k % len(colors)]
                bar_x, bar_w = x0 + 150, col_w - 150 - 44
                fill_w = bar_w * pct / 100
                body.append(
                    f'<text x="{x0}" y="{y + 4}" font-family="{SANS}" font-size="12.5" fill="{TEXT_2}">'
                    f'{e(name)}</text>'
                    f'<rect x="{bar_x}" y="{y - 4}" width="{bar_w}" height="8" rx="4" fill="{BG_2}"/>'
                    f'<rect class="bar" style="animation-duration:{1 + delay:.2f}s" x="{bar_x}" y="{y - 4}" width="{fill_w:.1f}" height="8" rx="4" fill="{color}"/>'
                    f'<text x="{x0 + col_w}" y="{y + 4}" text-anchor="end" font-family="{MONO}" '
                    f'font-size="11" fill="{color}">{pct}%</text>'
                )
                delay += 0.06
                y += 30
            y += 16
    return svg(W, H, "".join(body), "Compétences")


# --------------------------------------------------------------------------- stats live
QUERY = """
query($login: String!) {
  user(login: $login) {
    createdAt
    followers { totalCount }
    repositories(ownerAffiliations: OWNER, first: 100, privacy: PUBLIC) {
      totalCount
      nodes {
        isFork
        stargazerCount
        languages(first: 8, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def fetch_stats(token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": P.LOGIN}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "profile-readme-generator"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if "errors" in payload:
        raise RuntimeError(payload["errors"])
    return payload["data"]["user"]


def compute(user):
    cc = user["contributionsCollection"]
    days = [d for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    days.sort(key=lambda d: d["date"])
    best = cur = 0
    for d in days:
        cur = cur + 1 if d["contributionCount"] > 0 else 0
        best = max(best, cur)
    current = 0
    for i, d in enumerate(reversed(days)):
        if d["contributionCount"] > 0:
            current += 1
        elif i == 0:
            continue  # aujourd'hui peut encore être vide
        else:
            break
    langs = {}
    stars = 0
    for repo in user["repositories"]["nodes"]:
        stars += repo["stargazerCount"]
        if repo["isFork"]:
            continue
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            size, color = langs.get(name, (0, edge["node"]["color"] or MUTED))
            langs[name] = (size + edge["size"], color)
    total = sum(s for s, _ in langs.values()) or 1
    top = sorted(((n, s / total * 100, c) for n, (s, c) in langs.items()), key=lambda t: -t[1])[:6]
    return {
        "contributions": cc["contributionCalendar"]["totalContributions"],
        "commits": cc["totalCommitContributions"] + cc["restrictedContributionsCount"],
        "prs": cc["totalPullRequestContributions"],
        "repos": user["repositories"]["totalCount"],
        "stars": stars,
        "followers": user["followers"]["totalCount"],
        "streak": current,
        "best_streak": best,
        "langs": top,
    }


def stats_card(s):
    W, H = 880, 230
    body = [
        "<style>@keyframes in{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}"
        ".r{animation:in .6s ease-out}</style>",
        window_chrome(W, H, "github_stats.py"),
        f'<text x="24" y="62" font-family="{MONO}" font-size="12" fill="{MUTED}">'
        f"# live · mis à jour le {dt.date.today().strftime('%d/%m/%Y')}</text>",
    ]
    metrics = [
        ("🔥", "Streak actuel", f'{s["streak"]} j', ORANGE),
        ("🏅", "Meilleur streak", f'{s["best_streak"]} j', YELLOW),
        ("📈", "Contributions (1 an)", s["contributions"], GREEN),
        ("💾", "Commits (1 an)", s["commits"], ACCENT),
        ("🔀", "Pull requests", s["prs"], PURPLE),
        ("📦", "Repos publics", s["repos"], BLUE),
    ]
    for i, (icon, label, value, color) in enumerate(metrics):
        col, row = i % 2, i // 2
        x, y = 28 + col * 215, 98 + row * 42
        body.append(
            f'<g class="r" style="animation-duration:{0.5 + i * 0.15:.2f}s">'
            f'<text x="{x}" y="{y}" font-size="15">{icon}</text>'
            f'<text x="{x + 26}" y="{y - 1}" font-family="{SANS}" font-size="12" fill="{TEXT_2}">{e(label)}</text>'
            f'<text x="{x + 26}" y="{y + 18}" font-family="{SANS}" font-size="17" font-weight="800" '
            f'fill="{color}">{e(value)}</text></g>'
        )
    # langages
    lx, lw = 480, 372
    body.append(
        f'<text x="{lx}" y="92" font-family="{MONO}" font-size="11" font-weight="700" letter-spacing="1.5" '
        f'fill="{MUTED}">TOP LANGAGES</text>'
    )
    x = lx
    body.append(f'<clipPath id="bar"><rect x="{lx}" y="104" width="{lw}" height="10" rx="5"/></clipPath>'
                f'<g clip-path="url(#bar)">')
    for name, pct, color in s["langs"]:
        w = lw * pct / 100
        body.append(f'<rect x="{x:.1f}" y="104" width="{w + 0.5:.1f}" height="10" fill="{color}"/>')
        x += w
    body.append("</g>")
    for i, (name, pct, color) in enumerate(s["langs"]):
        col, row = i % 2, i // 2
        x, y = lx + col * 190, 140 + row * 24
        body.append(
            f'<circle cx="{x + 5}" cy="{y - 4}" r="5" fill="{color}"/>'
            f'<text x="{x + 16}" y="{y}" font-family="{SANS}" font-size="12.5" fill="{TEXT_2}">{e(name)}</text>'
            f'<text x="{x + 175}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="11" '
            f'fill="{MUTED}">{pct:.1f}%</text>'
        )
    return svg(W, H, "".join(body), "Statistiques GitHub")


# --------------------------------------------------------------------------- main
def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print("écrit", path.relative_to(ROOT))


def main():
    if "--stats" in sys.argv:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            sys.exit("GITHUB_TOKEN manquant")
        write(ROOT / "dist" / "stats.svg", stats_card(compute(fetch_stats(token))))
        return
    assets = ROOT / "assets"
    write(assets / "header.svg", header())
    write(assets / "highlights.svg", highlights())
    write(assets / "trophies.svg", trophies())
    write(assets / "experience.svg", experience())
    write(assets / "skills.svg", skills())
    for i, h in enumerate(P.HACKATHONS, 1):
        write(assets / "hackathons" / f"{i:02d}.svg", hackathon_card(h))


if __name__ == "__main__":
    main()
