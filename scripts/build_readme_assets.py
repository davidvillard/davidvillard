"""Generates the SVG assets used by README.md (assets/readme/*.svg).

Style: Apple-keynote darkness + 8-bit pixel art. No dependencies.
Run:  python scripts/build_readme_assets.py
"""
import random
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "readme"

SANS = "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', 'Helvetica Neue', Inter, Arial, sans-serif"
MONO = "'SF Mono', ui-monospace, Menlo, 'Cascadia Code', Consolas, 'Liberation Mono', monospace"

BG = "#000000"
CARD = "#0b0b0e"
LINE = "#1d1d22"
TEXT = "#f5f5f7"
TEXT2 = "#a1a1a6"
TEXT3 = "#6e6e73"
VIOLET = "#a78bfa"
BLUE = "#60a5fa"
PINK = "#f0abfc"
GREEN = "#4ade80"

# ---------------------------------------------------------------- pixel font
F = {
    "A": [".XXX.", "X...X", "X...X", "XXXXX", "X...X", "X...X", "X...X"],
    "B": ["XXXX.", "X...X", "X...X", "XXXX.", "X...X", "X...X", "XXXX."],
    "C": [".XXX.", "X...X", "X....", "X....", "X....", "X...X", ".XXX."],
    "D": ["XXXX.", "X...X", "X...X", "X...X", "X...X", "X...X", "XXXX."],
    "E": ["XXXXX", "X....", "X....", "XXXX.", "X....", "X....", "XXXXX"],
    "F": ["XXXXX", "X....", "X....", "XXXX.", "X....", "X....", "X...."],
    "G": [".XXX.", "X...X", "X....", "X.XXX", "X...X", "X...X", ".XXXX"],
    "H": ["X...X", "X...X", "X...X", "XXXXX", "X...X", "X...X", "X...X"],
    "I": ["XXX", ".X.", ".X.", ".X.", ".X.", ".X.", "XXX"],
    "J": ["..XXX", "...X.", "...X.", "...X.", "X..X.", "X..X.", ".XX.."],
    "K": ["X...X", "X..X.", "X.X..", "XX...", "X.X..", "X..X.", "X...X"],
    "L": ["X....", "X....", "X....", "X....", "X....", "X....", "XXXXX"],
    "M": ["X...X", "XX.XX", "X.X.X", "X.X.X", "X...X", "X...X", "X...X"],
    "N": ["X...X", "XX..X", "X.X.X", "X..XX", "X...X", "X...X", "X...X"],
    "O": [".XXX.", "X...X", "X...X", "X...X", "X...X", "X...X", ".XXX."],
    "P": ["XXXX.", "X...X", "X...X", "XXXX.", "X....", "X....", "X...."],
    "Q": [".XXX.", "X...X", "X...X", "X...X", "X.X.X", "X..X.", ".XX.X"],
    "R": ["XXXX.", "X...X", "X...X", "XXXX.", "X.X..", "X..X.", "X...X"],
    "S": [".XXXX", "X....", "X....", ".XXX.", "....X", "....X", "XXXX."],
    "T": ["XXXXX", "..X..", "..X..", "..X..", "..X..", "..X..", "..X.."],
    "U": ["X...X", "X...X", "X...X", "X...X", "X...X", "X...X", ".XXX."],
    "V": ["X...X", "X...X", "X...X", "X...X", "X...X", ".X.X.", "..X.."],
    "W": ["X...X", "X...X", "X...X", "X.X.X", "X.X.X", "X.X.X", ".X.X."],
    "X": ["X...X", "X...X", ".X.X.", "..X..", ".X.X.", "X...X", "X...X"],
    "Y": ["X...X", "X...X", ".X.X.", "..X..", "..X..", "..X..", "..X.."],
    "Z": ["XXXXX", "....X", "...X.", "..X..", ".X...", "X....", "XXXXX"],
    "0": [".XXX.", "X...X", "X..XX", "X.X.X", "XX..X", "X...X", ".XXX."],
    "1": ["..X..", ".XX..", "..X..", "..X..", "..X..", "..X..", ".XXX."],
    "2": [".XXX.", "X...X", "....X", "...X.", "..X..", ".X...", "XXXXX"],
    "3": ["XXXXX", "...X.", "..X..", "...X.", "....X", "X...X", ".XXX."],
    "4": ["...X.", "..XX.", ".X.X.", "X..X.", "XXXXX", "...X.", "...X."],
    "5": ["XXXXX", "X....", "XXXX.", "....X", "....X", "X...X", ".XXX."],
    "6": ["..XX.", ".X...", "X....", "XXXX.", "X...X", "X...X", ".XXX."],
    "7": ["XXXXX", "....X", "...X.", "..X..", ".X...", ".X...", ".X..."],
    "8": [".XXX.", "X...X", "X...X", ".XXX.", "X...X", "X...X", ".XXX."],
    "9": [".XXX.", "X...X", "X...X", ".XXXX", "....X", "...X.", ".XX.."],
    " ": ["...", "...", "...", "...", "...", "...", "..."],
    ".": [".", ".", ".", ".", ".", ".", "X"],
    "-": ["...", "...", "...", "XXX", "...", "...", "..."],
    "_": [".....", ".....", ".....", ".....", ".....", ".....", "XXXXX"],
    ">": ["X...", ".X..", "..X.", "...X", "..X.", ".X..", "X..."],
    "/": ["....X", "....X", "...X.", "..X..", ".X...", "X....", "X...."],
    "!": ["X", "X", "X", "X", "X", ".", "X"],
    "?": [".XXX.", "X...X", "....X", "...X.", "..X..", ".....", "..X.."],
    ":": [".", "X", ".", ".", ".", "X", "."],
    "+": [".....", "..X..", "..X..", "XXXXX", "..X..", "..X..", "....."],
    "#": [".X.X.", "XXXXX", ".X.X.", ".X.X.", ".X.X.", "XXXXX", ".X.X."],
    "*": [".......", ".XX.XX.", "XXXXXXX", "XXXXXXX", ".XXXXX.", "..XXX..", "...X..."],  # heart
    "|": ["XXXXX"] * 7,  # block cursor
}


def text_width(s, px):
    cols = sum(len(F[c][0]) for c in s) + max(len(s) - 1, 0)
    return cols * px


def pixel_text(s, x, y, px, fill, gap=None, extra=""):
    """Return SVG rects drawing `s` with the pixel font, top-left at (x, y)."""
    gap = px * 0.14 if gap is None else gap
    out, cx = [], x
    for ch in s:
        g = F[ch]
        for r, row in enumerate(g):
            for c, v in enumerate(row):
                if v == "X":
                    out.append(
                        f'<rect x="{cx + c * px:.1f}" y="{y + r * px:.1f}" '
                        f'width="{px - gap:.1f}" height="{px - gap:.1f}"/>'
                    )
        cx += (len(g[0]) + 1) * px
    return f'<g fill="{fill}"{extra}>' + "".join(out) + "</g>"


def sprite(rows, palette, x, y, px, gap=0):
    out = []
    for r, row in enumerate(rows):
        for c, v in enumerate(row):
            if v in palette:
                out.append(
                    f'<rect x="{x + c * px:.1f}" y="{y + r * px:.1f}" width="{px - gap:.1f}" '
                    f'height="{px - gap:.1f}" fill="{palette[v]}"/>'
                )
    return "".join(out)


def fade_in(t, d=0.18):
    """Opacity animation starting at 0 and fading in at t seconds.
    If SMIL is unsupported the element just stays visible."""
    end = t + d
    return (
        f'<animate attributeName="opacity" values="0;0;1" keyTimes="0;{t / end:.4f};1" '
        f'dur="{end:.2f}s" fill="freeze"/>'
    )


def svg(w, h, body, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-label="{escape(title)}"><title>{escape(title)}</title>{body}</svg>\n'
    )


def iri_gradient(gid, x1, x2, stops=(TEXT, "#e9d5ff", "#c4b5fd", "#93c5fd", PINK)):
    n = len(stops) - 1
    s = "".join(f'<stop offset="{i / n:.2f}" stop-color="{c}"/>' for i, c in enumerate(stops))
    return f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x1}" y1="0" x2="{x2}" y2="0">{s}</linearGradient>'


# ---------------------------------------------------------------- avatar sprite (me, with the cap)
AVATAR = [
    "................",
    ".....KKKKKK.....",
    "...KKKKKKKKKK...",
    "..KKkkKKKKKKKK..",
    "..KkkKKKKKKKKK..",
    "..KKKKKKKKKKKKKKK",
    "..HHSSSSSSSSHH..",
    "..HSSSSSSSSSSH..",
    "..SSEWSSSSSSSS..",
    ".sSSEESSSSEESSs.",
    "..SPSSSSSSSSPS..",
    "..SSSSMSSSMSSS..",
    "...SSSSMMMSSSS..",
    "....sSSSSSSs....",
    "..TTTTTsTTTTTT..",
    ".TTTTTTTTTTTTTT.",
]
AVATAR_PAL = {
    "K": "#111114", "k": "#3a3a40", "H": "#3b2418", "S": "#f2c38f", "s": "#d99a63",
    "E": "#111114", "W": "#ffffff", "P": "#f29a8a", "M": "#7a2e2e", "T": "#8b5cf6",
}


# ---------------------------------------------------------------- hero
def hero():
    W, H = 1280, 600
    rnd = random.Random(7)
    defs = [
        f'<clipPath id="c"><rect width="{W}" height="{H}" rx="28"/></clipPath>',
        '<radialGradient id="g1"><stop offset="0" stop-color="#7c3aed" stop-opacity=".55"/><stop offset="1" stop-color="#7c3aed" stop-opacity="0"/></radialGradient>',
        '<radialGradient id="g2"><stop offset="0" stop-color="#2563eb" stop-opacity=".45"/><stop offset="1" stop-color="#2563eb" stop-opacity="0"/></radialGradient>',
        '<radialGradient id="g3"><stop offset="0" stop-color="#db2777" stop-opacity=".30"/><stop offset="1" stop-color="#db2777" stop-opacity="0"/></radialGradient>',
        '<pattern id="grid" width="16" height="16" patternUnits="userSpaceOnUse"><rect width="2" height="2" fill="#fff" opacity=".07"/></pattern>',
        '<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="28"/></filter>',
        '<linearGradient id="tile" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#312e81"/><stop offset=".55" stop-color="#6d28d9"/><stop offset="1" stop-color="#c026d3"/></linearGradient>',
        '<linearGradient id="shine" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>',
    ]
    px = 16
    x0 = 72
    w2 = text_width("VILLAR", px)
    defs.append(iri_gradient("iri", x0, x0 + w2))

    b = [f'<defs>{"".join(defs)}</defs>', '<g clip-path="url(#c)">', f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    # drifting glows
    for gid, cx, cy, r, dx, dy, dur in [
        ("g1", 980, 120, 520, -60, 40, 14),
        ("g2", 300, 620, 560, 80, -30, 18),
        ("g3", 1180, 560, 380, -40, -50, 16),
    ]:
        b.append(
            f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r * 0.7:.0f}" fill="url(#{gid})">'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;{dx} {dy};0 0" '
            f'dur="{dur}s" repeatCount="indefinite"/></ellipse>'
        )
    b.append(f'<rect width="{W}" height="{H}" fill="url(#grid)"/>')
    # twinkling pixels
    for _ in range(46):
        x, y = rnd.randrange(0, W // 16) * 16, rnd.randrange(0, H // 16) * 16
        s = rnd.choice([4, 4, 6, 8])
        col = rnd.choice([TEXT, VIOLET, BLUE, PINK])
        dur = rnd.uniform(2.5, 6)
        b.append(
            f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{col}" opacity=".25">'
            f'<animate attributeName="opacity" values=".05;.85;.05" dur="{dur:.1f}s" '
            f'begin="{rnd.uniform(0, 4):.1f}s" repeatCount="indefinite"/></rect>'
        )
    b.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="28" fill="none" stroke="#ffffff" stroke-opacity=".08"/>')
    b.append("</g>")

    # status pill
    pill_txt = "Disponible para proyectos freelance"
    pw = 46 + len(pill_txt) * 8.3
    b.append(
        f'<g transform="translate({x0} 52)"><rect width="{pw:.0f}" height="38" rx="19" fill="#fff" fill-opacity=".06" '
        f'stroke="#fff" stroke-opacity=".12"/>'
        f'<circle cx="21" cy="19" r="5" fill="{GREEN}"><animate attributeName="opacity" values="1;.35;1" dur="2s" repeatCount="indefinite"/></circle>'
        f'<circle cx="21" cy="19" r="5" fill="none" stroke="{GREEN}"><animate attributeName="r" values="5;12" dur="2s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values=".8;0" dur="2s" repeatCount="indefinite"/></circle>'
        f'<text x="36" y="24.5" font-family="{SANS}" font-size="15" font-weight="500" fill="{TEXT}">{pill_txt}</text></g>'
    )
    # pixel wordmark
    y1, y2 = 128, 128 + 7 * px + 26
    b.append(pixel_text("DAVID", x0, y1, px, "url(#iri)"))
    b.append(pixel_text("VILLAR", x0, y2, px, "url(#iri)"))
    cx = x0 + w2 + px
    b.append(
        f'<rect x="{cx}" y="{y2}" width="{px * 2.4:.0f}" height="{7 * px - 2}" fill="{VIOLET}">'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/></rect>'
    )
    # headline
    ty = y2 + 7 * px + 70
    b.append(
        f'<text x="{x0}" y="{ty}" font-family="{SANS}" font-size="34" font-weight="600" letter-spacing="-.6" fill="{TEXT}">'
        f'Full‑stack developer.</text>'
        f'<text x="{x0}" y="{ty + 44}" font-family="{SANS}" font-size="34" font-weight="600" letter-spacing="-.6" fill="{TEXT3}">'
        f'Webs rápidas, diseño cuidado y píxeles.</text>'
    )
    # footer meta
    meta = ["VIGO, ES", "GYLEVEN", "DURANDEV", "SINCE 2021"]
    mx = x0
    my = H - 46
    parts = []
    for i, m in enumerate(meta):
        parts.append(f'<text x="{mx}" y="{my}" font-family="{MONO}" font-size="14" letter-spacing="1.5" fill="{TEXT3}">{m}</text>')
        mx += len(m) * 10 + 22
        if i < len(meta) - 1:
            parts.append(f'<rect x="{mx - 15}" y="{my - 8}" width="5" height="5" fill="{VIOLET}"/>')
    b.extend(parts)

    # app-icon tile with the pixel avatar
    tx, ty0, ts = 880, 118, 320
    sp = 17
    b.append(
        f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -8;0 0" dur="4s" repeatCount="indefinite"/>'
        f'<rect x="{tx + 30}" y="{ty0 + 60}" width="{ts - 60}" height="{ts - 40}" rx="60" fill="#a855f7" opacity=".55" filter="url(#blur)"/>'
        f'<rect x="{tx}" y="{ty0}" width="{ts}" height="{ts}" rx="76" fill="url(#tile)"/>'
        f'<rect x="{tx}" y="{ty0}" width="{ts}" height="{ts}" rx="76" fill="url(#shine)"/>'
        f'<rect x="{tx + .5}" y="{ty0 + .5}" width="{ts - 1}" height="{ts - 1}" rx="76" fill="none" stroke="#fff" stroke-opacity=".25"/>'
        + sprite(AVATAR, AVATAR_PAL, tx + (ts - 16 * sp) / 2 - sp / 2, ty0 + (ts - 16 * sp) / 2 + 6, sp)
        + "</g>"
    )
    b.append(
        f'<text x="{tx + ts / 2}" y="{ty0 + ts + 58}" text-anchor="middle" font-family="{MONO}" font-size="14" '
        f'letter-spacing="1.5" fill="{TEXT3}">PLAYER 1 · LVL 99 DEV</text>'
    )
    return svg(W, H, "".join(b), "David Villar Durán — Full-stack developer")


# ---------------------------------------------------------------- buttons
def button(label, primary, icon=None):
    h = 56
    tw = len(label) * 9.6
    iw = 26 if icon else 0
    w = int(tw + iw + 56)
    fill, txt, stroke = (TEXT, "#000", "#d2d2d7") if primary else ("#16161a", TEXT, "#2c2c33")
    b = [f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="27" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>']
    x = 28
    if icon:
        b.append(sprite(icon, {"X": txt, "A": VIOLET}, x, (h - len(icon) * 2.5) / 2, 2.5))
        x += iw
    b.append(
        f'<text x="{x}" y="{h / 2 + 6}" font-family="{SANS}" font-size="17" font-weight="600" fill="{txt}">{escape(label)}</text>'
    )
    return svg(w, h, "".join(b), label)


ICON_ARROW = ["..XXXX", "....XX", "...X.X", "..X..X", ".X....", "X....."]
ICON_GLOBE = [".XXXX.", "X.XX.X", "XXXXXX", "X.XX.X", "X.XX.X", ".XXXX."]
ICON_CAM = [".XXXX.", "X....X", "X.XX.X", "X.XX.X", "X....X", ".XXXX."]
ICON_NOTE = ["...XXX", "...X.X", "...X..", ".XXX..", "XXXX..", ".XX..."]


# ---------------------------------------------------------------- section headers
def header(num, title, caption):
    W, H = 1280, 150
    px = 9
    tw = text_width(title, px)
    x = (W - tw) / 2
    b = [f'<defs>{iri_gradient("h", x, x + tw, ("#7c3aed", "#8b5cf6", "#3b82f6", "#c026d3"))}</defs>']
    b.append(
        f'<text x="{W / 2}" y="34" text-anchor="middle" font-family="{MONO}" font-size="15" letter-spacing="3" fill="#8b5cf6">'
        f'{num} — {escape(caption)}</text>'
    )
    b.append(pixel_text(title, x, 56, px, "url(#h)"))
    b.append(
        f'<rect x="{W / 2 - 220}" y="{H - 14}" width="440" height="1" fill="url(#hl)"/>'
        '<defs><linearGradient id="hl"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset=".5" stop-color="#8b5cf6" stop-opacity=".6"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>'
    )
    return svg(W, H, "".join(b), title)


# ---------------------------------------------------------------- terminal (neofetch)
def terminal_frame(W, H):
    b = [
        f'<defs><clipPath id="c"><rect width="{W}" height="{H}" rx="22"/></clipPath>'
        '<linearGradient id="bar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2a30"/><stop offset="1" stop-color="#1f1f24"/></linearGradient></defs>',
        f'<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="{CARD}"/>',
        f'<rect width="{W}" height="52" fill="url(#bar)"/><rect y="52" width="{W}" height="1" fill="#000"/>',
    ]
    for i, col in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        b.append(f'<circle cx="{30 + i * 24}" cy="26" r="7" fill="{col}"/>')
    b.append(
        f'<text x="{W / 2}" y="31" text-anchor="middle" font-family="{SANS}" font-size="15" font-weight="600" fill="{TEXT2}">'
        f'david — zsh — 120×32</text>'
    )
    b.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="22" fill="none" stroke="#fff" stroke-opacity=".1"/></g>')
    return "".join(b)


def terminal():
    W = 1280
    lh = 34
    fs = 20
    cw = fs * 0.6  # approx monospace advance
    b = []
    x0 = 44
    y = 100
    clip_id = [0]

    def prompt(y, cmd, t0, t_type):
        clip_id[0] += 1
        cid = f"t{clip_id[0]}"
        p = "david@vigo"
        pre_w = (len(p) + 5) * cw
        n = len(cmd)
        full = n * cw + 4
        steps = ";".join(f"{i * cw:.1f}" for i in range(n + 1))
        kt = ";".join(f"{i / n:.3f}" for i in range(n + 1))
        g = [
            f'<g opacity="1">{fade_in(t0, 0.01)}',
            f'<text y="{y}" font-family="{MONO}" font-size="{fs}" xml:space="preserve">'
            f'<tspan x="{x0}" fill="{VIOLET}" font-weight="700">{p}</tspan><tspan fill="{BLUE}"> ~ </tspan><tspan fill="{TEXT}">% </tspan></text>',
            f'<clipPath id="{cid}"><rect x="{x0 + pre_w}" y="{y - 26}" width="{full:.1f}" height="36">'
            f'<animate attributeName="width" values="0;0;{steps}" keyTimes="0;{t0 / (t0 + t_type):.3f};'
            + ";".join(f"{(t0 + t_type * i / n) / (t0 + t_type):.3f}" for i in range(n + 1))
            + f'" dur="{t0 + t_type:.2f}s" calcMode="discrete" fill="freeze"/></rect></clipPath>',
            f'<text x="{x0 + pre_w}" y="{y}" font-family="{MONO}" font-size="{fs}" fill="{TEXT}" clip-path="url(#{cid})">{escape(cmd)}</text>',
            "</g>",
        ]
        return "".join(g)

    # 1) neofetch
    b.append(prompt(y, "neofetch", 0.4, 0.7))
    t = 1.35
    y += lh + 14
    # avatar block
    ap = 13
    b.append(f'<g>{fade_in(t)}' + sprite(AVATAR, AVATAR_PAL, x0 + 6, y - 10, ap) + "</g>")
    info = [
        ("david", "@vigo", None),
        ("-" * 16, None, None),
        ("Role", "Full-stack developer", None),
        ("Work", "Gyleven  ·  durandev (freelance)", None),
        ("Location", "Vigo, Galicia, España", None),
        ("Languages", "TypeScript · JavaScript · PHP · Python · Java", None),
        ("Frontend", "React · Next.js · Astro · Vue · Tailwind", None),
        ("Backend", "Node · Express · Django REST · Supabase", None),
        ("Interests", "Ciberseguridad · UI design · Pixel art", None),
        ("Uptime", "en GitHub desde 2021", None),
    ]
    ix = x0 + 16 * ap + 56
    yy = y + 4
    for i, (k, v, _) in enumerate(info):
        tt = t + 0.06 * i
        if i == 0:
            line = (f'<tspan fill="{VIOLET}" font-weight="700">{k}</tspan><tspan fill="{TEXT}">{v}</tspan>')
        elif i == 1:
            line = f'<tspan fill="{TEXT3}">{k}</tspan>'
        else:
            pad = " " * (11 - len(k))
            line = (f'<tspan fill="{VIOLET}" font-weight="700">{k}</tspan><tspan fill="{TEXT3}">:{pad}</tspan>'
                    f'<tspan fill="{TEXT}">{escape(v)}</tspan>')
        b.append(f'<text x="{ix}" y="{yy}" font-family="{MONO}" font-size="{fs}" xml:space="preserve">{fade_in(tt)}{line}</text>')
        yy += lh
    # color blocks
    cols = ["#111114", "#ff5f57", GREEN, "#febc2e", BLUE, VIOLET, PINK, TEXT]
    tt = t + 0.06 * len(info)
    blocks = "".join(f'<rect x="{ix + i * 34}" y="{yy - 10}" width="30" height="18" fill="{c}"/>' for i, c in enumerate(cols))
    b.append(f"<g>{fade_in(tt)}{blocks}</g>")
    y = yy + lh + 26

    # 2) cat sobre-mi.txt
    t2 = tt + 0.6
    cmd = "cat sobre-mi.txt"
    b.append(prompt(y, cmd, t2, 0.9))
    t3 = t2 + 1.1
    lines = [
        "Me encanta construir producto de punta a punta: del pixel al servidor.",
        "Como durandev hago webs rápidas y tiendas online para negocios de Galicia.",
        "Obsesionado con el detalle, la performance y la seguridad web.",
    ]
    y += lh + 4
    for i, ln in enumerate(lines):
        b.append(
            f'<text x="{x0}" y="{y}" font-family="{MONO}" font-size="{fs}" fill="{TEXT2}" xml:space="preserve">{fade_in(t3 + i * 0.15)}'
            f'<tspan fill="{GREEN}">→ </tspan>{escape(ln)}</text>'
        )
        y += lh
    y += 18
    # 3) idle prompt with cursor
    t4 = t3 + 0.7
    p_w = (len("david@vigo") + 5) * cw
    b.append(
        f'<g>{fade_in(t4, 0.01)}<text x="{x0}" y="{y}" font-family="{MONO}" font-size="{fs}" xml:space="preserve">'
        f'<tspan fill="{VIOLET}" font-weight="700">david@vigo</tspan><tspan fill="{BLUE}"> ~ </tspan><tspan fill="{TEXT}">% </tspan></text>'
        f'<rect x="{x0 + p_w:.1f}" y="{y - 19}" width="12" height="24" fill="{TEXT}">'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/></rect></g>'
    )
    H = int(y + 46)
    return svg(W, H, terminal_frame(W, H) + "".join(b), "neofetch — David Villar Durán")


# ---------------------------------------------------------------- project cards
ICONS = {
    "durandev": (
        ["XXXXXXXXXXXX", "XRXYXGX....X", "XXXXXXXXXXXX", "X..........X", "X.A........X",
         "X..A.......X", "X.A..AAA...X", "X..........X", "XXXXXXXXXXXX"],
        {"X": TEXT, "A": VIOLET, "R": "#ff5f57", "Y": "#febc2e", "G": "#28c840"},
    ),
    "stackhub": (
        ["..XXXXXXXX..", "..XXXXXXXX..", "............", ".AAAAAAAAAA.", ".AAAAAAAAAA.",
         "............", "BBBBBBBBBBBB", "BBBBBBBBBBBB"],
        {"X": TEXT, "A": "#c4b5fd", "B": VIOLET},
    ),
    "huella": (
        ["...XX..XX...", "...XX..XX...", "XX........XX", "XX........XX", "....XXXX....",
         "...XXXXXX...", "..XXXXXXXX..", "..XXXXXXXX..", "...XX..XX..."],
        {"X": "#fdba74"},
    ),
    "interstellar": (
        ["....OOOO....", "..OO....OO..", ".O........O.", ".O..KKKK..O.", "YYYYKKKKYYYY",
         "YYYYKKKKYYYY", ".O..KKKK..O.", ".O........O.", "..OO....OO..", "....OOOO...."],
        {"O": "#fb923c", "Y": "#fde68a", "K": "#000000"},
    ),
    "shield": (
        [".XXXXXXXXXX.", ".X........X.", ".X......C.X.", ".X.....C..X.", ".X.C..C...X.",
         ".X..CC....X.", "..X......X..", "...X....X...", "....XXXX...."],
        {"X": TEXT, "C": GREEN},
    ),
    "modular": (
        ["..X......X..", "XXXXXXXXXXXX", "XXXXXXXXXXXX", "X..........X", "X.AA.BB.AA.X",
         "X..........X", "X.BB.AA.BB.X", "X..........X", "X.AA.BB....X", "XXXXXXXXXXXX"],
        {"X": TEXT, "A": BLUE, "B": VIOLET},
    ),
}

TILE_GRAD = {
    "durandev": ("#1e1b4b", "#6d28d9"),
    "stackhub": ("#1f2937", "#4338ca"),
    "huella": ("#431407", "#c2410c"),
    "interstellar": ("#0c0a09", "#44403c"),
    "shield": ("#052e16", "#15803d"),
    "modular": ("#0c4a6e", "#1d4ed8"),
}


def wrap(s, n):
    words, lines, cur = s.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > n and cur:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    lines.append(cur)
    return lines


def card(key, title, url_label, desc, chips, status, accent):
    W, H = 620, 350
    icon, pal = ICONS[key]
    g0, g1 = TILE_GRAD[key]
    b = [
        '<defs>'
        f'<clipPath id="c"><rect width="{W}" height="{H}" rx="26"/></clipPath>'
        f'<radialGradient id="glow"><stop offset="0" stop-color="{accent}" stop-opacity=".28"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="t" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{g0}"/><stop offset="1" stop-color="{g1}"/></linearGradient>'
        '<linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".18"/><stop offset=".55" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        '<pattern id="grid" width="12" height="12" patternUnits="userSpaceOnUse"><rect width="2" height="2" fill="#fff" opacity=".05"/></pattern>'
        '</defs>',
        f'<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="{CARD}"/>',
        f'<rect width="{W}" height="{H}" fill="url(#grid)"/>',
        f'<ellipse cx="{W - 40}" cy="10" rx="300" ry="220" fill="url(#glow)"/></g>',
        f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="26" fill="none" stroke="#fff" stroke-opacity=".1" stroke-width="1.5"/>',
    ]
    # icon tile
    tx, ty, ts = 34, 34, 92
    ip = 6
    iw, ih = len(icon[0]) * ip, len(icon) * ip
    b.append(
        f'<rect x="{tx}" y="{ty}" width="{ts}" height="{ts}" rx="22" fill="url(#t)"/>'
        f'<rect x="{tx}" y="{ty}" width="{ts}" height="{ts}" rx="22" fill="url(#s)"/>'
        f'<rect x="{tx + .5}" y="{ty + .5}" width="{ts - 1}" height="{ts - 1}" rx="22" fill="none" stroke="#fff" stroke-opacity=".2"/>'
        + sprite(icon, pal, tx + (ts - iw) / 2, ty + (ts - ih) / 2, ip)
    )
    # status chip
    sw = len(status) * 9 + 40
    dot = {"LIVE": GREEN, "API": BLUE, "TEAM": VIOLET, "WIP": "#febc2e"}.get(status, TEXT2)
    anim = '<animate attributeName="opacity" values="1;.3;1" dur="1.8s" repeatCount="indefinite"/>' if status == "LIVE" else ""
    b.append(
        f'<g transform="translate({W - 34 - sw} 40)"><rect width="{sw}" height="30" rx="15" fill="#fff" fill-opacity=".06" stroke="#fff" stroke-opacity=".12"/>'
        f'<rect x="15" y="11" width="8" height="8" fill="{dot}">{anim}</rect>'
        f'<text x="30" y="20" font-family="{MONO}" font-size="13" font-weight="600" letter-spacing="1.5" fill="{TEXT}">{status}</text></g>'
    )
    # title + url
    b.append(
        f'<text x="34" y="172" font-family="{SANS}" font-size="34" font-weight="700" letter-spacing="-.6" fill="{TEXT}">{escape(title)}</text>'
        f'<text x="34" y="202" font-family="{MONO}" font-size="15" fill="{accent}">{escape(url_label)} ↗</text>'
    )
    for i, ln in enumerate(wrap(desc, 54)[:2]):
        b.append(f'<text x="34" y="{238 + i * 27}" font-family="{SANS}" font-size="20" fill="{TEXT2}">{escape(ln)}</text>')
    # chips
    cx = 34
    for c in chips:
        w = len(c) * 9 + 26
        if cx + w > W - 30:
            break
        b.append(
            f'<rect x="{cx}" y="292" width="{w:.0f}" height="32" rx="9" fill="#17171c" stroke="#2a2a31"/>'
            f'<text x="{cx + 13}" y="313" font-family="{MONO}" font-size="14.5" fill="#d4d4d8">{escape(c)}</text>'
        )
        cx += w + 8
    return svg(W, H, "".join(b), title)


PROJECTS = [
    dict(key="durandev", title="durandev", url_label="durandev.vercel.app",
         desc="Mi marca freelance: webs rápidas, tiendas online y SEO para negocios de Vigo y Galicia.",
         chips=["Next.js", "TypeScript", "Tailwind", "shadcn/ui", "Motion"], status="LIVE", accent=VIOLET),
    dict(key="stackhub", title="StackHub", url_label="stackhub-app.vercel.app",
         desc="Más de 150 recursos gratuitos para diseñadores y devs: iconos, fuentes, UI y componentes.",
         chips=["Next.js", "React", "Tailwind", "Framer Motion"], status="LIVE", accent="#818cf8"),
    dict(key="huella", title="La Huella de Puri", url_label="lahuelladepuri.vercel.app",
         desc="Tienda y catálogo artesanal con panel de administración para gestionar productos.",
         chips=["Next.js", "React 19", "Supabase", "Tailwind"], status="LIVE", accent="#fdba74"),
    dict(key="interstellar", title="Interstellar", url_label="interstellarfanpage.netlify.app",
         desc="Fan page de la película con login/registro, contenido exclusivo y base de datos.",
         chips=["Astro", "Auth.js", "Astro DB", "Tailwind", "Docker"], status="LIVE", accent="#fb923c"),
    dict(key="shield", title="Security Verifier", url_label="github.com/davidvillard/drfbackendcheck",
         desc="API que analiza URLs, emails, teléfonos y SMS sospechosos con VirusTotal y Neutrino.",
         chips=["Python", "Django REST", "Docker", "Render"], status="API", accent=GREEN),
    dict(key="modular", title="Modular", url_label="github.com/sempereluismi/modular",
         desc="Gestión de horarios y módulos de un instituto. Proyecto en equipo con Luis, Andrea y Manuel.",
         chips=["React", "PHP", "Tailwind", "JavaScript"], status="TEAM", accent=BLUE),
]


# ---------------------------------------------------------------- tech specs (Apple spec-sheet)
SPECS = [
    ("Lenguajes", "TypeScript · JavaScript · PHP · Python · Java · SQL", VIOLET),
    ("Frontend", "React · Next.js · Astro · Vue · Tailwind CSS · shadcn/ui", BLUE),
    ("Backend", "Node.js · Express · Django REST Framework · PHP", PINK),
    ("Datos", "Supabase · MySQL · MongoDB · Astro DB", GREEN),
    ("DevOps", "Git · Docker · Vercel · Netlify · Render · Postman", "#febc2e"),
    ("CMS y tools", "WordPress · VS Code · Obsidian", "#fb923c"),
]


def specs():
    W = 1280
    rh = 72
    H = 40 + rh * len(SPECS) + 30
    b = [
        f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="26" fill="{CARD}" stroke="#fff" stroke-opacity=".1" stroke-width="1.5"/>'
    ]
    y = 40
    for i, (k, v, c) in enumerate(SPECS):
        cy = y + rh / 2
        b.append(sprite(["XX", "XX"], {"X": c}, 48, cy - 9, 5))
        b.append(f'<text x="76" y="{cy + 7}" font-family="{SANS}" font-size="19" font-weight="500" fill="{TEXT3}">{k}</text>')
        b.append(f'<text x="300" y="{cy + 8}" font-family="{SANS}" font-size="22" font-weight="600" letter-spacing="-.2" fill="{TEXT}">{escape(v)}</text>')
        if i < len(SPECS) - 1:
            b.append(f'<rect x="48" y="{y + rh}" width="{W - 96}" height="1" fill="#fff" fill-opacity=".08"/>')
        y += rh
    return svg(W, H, "".join(b), "Tech specs")


# ---------------------------------------------------------------- footer
def footer():
    W, H = 1280, 300
    rnd = random.Random(3)
    b = [
        '<defs><clipPath id="c"><rect width="1280" height="300" rx="28"/></clipPath>'
        '<radialGradient id="g"><stop offset="0" stop-color="#7c3aed" stop-opacity=".45"/><stop offset="1" stop-color="#7c3aed" stop-opacity="0"/></radialGradient>'
        '<pattern id="grid" width="16" height="16" patternUnits="userSpaceOnUse"><rect width="2" height="2" fill="#fff" opacity=".07"/></pattern></defs>',
        f'<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="{BG}"/>',
        f'<ellipse cx="{W / 2}" cy="{H + 40}" rx="620" ry="260" fill="url(#g)"/>',
        f'<rect width="{W}" height="{H}" fill="url(#grid)"/>',
    ]
    for _ in range(24):
        x, y = rnd.randrange(0, W // 16) * 16, rnd.randrange(0, H // 16) * 16
        b.append(
            f'<rect x="{x}" y="{y}" width="4" height="4" fill="{rnd.choice([TEXT, VIOLET, BLUE])}" opacity=".2">'
            f'<animate attributeName="opacity" values=".05;.8;.05" dur="{rnd.uniform(2.5, 5):.1f}s" begin="{rnd.uniform(0, 3):.1f}s" repeatCount="indefinite"/></rect>'
        )
    b.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="28" fill="none" stroke="#fff" stroke-opacity=".08"/></g>')
    # lives / score row
    b.append(f'<text x="48" y="54" font-family="{MONO}" font-size="14" letter-spacing="2" fill="{TEXT3}">1UP</text>')
    for i in range(3):
        b.append(sprite(F["*"], {"X": "#ff5f57"}, 96 + i * 30, 40, 3))
    b.append(f'<text x="{W - 48}" y="54" text-anchor="end" font-family="{MONO}" font-size="14" letter-spacing="2" fill="{TEXT3}">HI-SCORE 002021</text>')
    # PRESS START
    px = 12
    t1 = "PRESS START"
    w1 = text_width(t1, px)
    b.append(f'<defs>{iri_gradient("f", (W - w1) / 2, (W + w1) / 2)}</defs>')
    b.append(
        '<g><animate attributeName="opacity" values="1;1;.15;.15" keyTimes="0;.55;.55;1" dur="1.4s" repeatCount="indefinite"/>'
        + pixel_text(t1, (W - w1) / 2, 96, px, "url(#f)")
        + "</g>"
    )
    px2 = 5
    t2 = "TO BUILD SOMETHING TOGETHER"
    w2 = text_width(t2, px2)
    b.append(pixel_text(t2, (W - w2) / 2, 208, px2, TEXT2))
    b.append(
        f'<text x="{W / 2}" y="{H - 30}" text-anchor="middle" font-family="{MONO}" font-size="14" letter-spacing="1.5" fill="{TEXT3}">'
        f'hecho con café, píxeles y ⌘ desde Vigo</text>'
    )
    return svg(W, H, "".join(b), "Press start to build something together")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    files = {
        "hero.svg": hero(),
        "terminal.svg": terminal(),
        "specs.svg": specs(),
        "footer.svg": footer(),
        "header-whoami.svg": header("01", "WHOAMI", "sobre mí"),
        "header-proyectos.svg": header("02", "PROYECTOS", "selected work"),
        "header-stack.svg": header("03", "STACK", "tech specs"),
        "header-actividad.svg": header("04", "ACTIVIDAD", "commits & lenguajes"),
        "btn-durandev.svg": button("durandev.vercel.app", True, ICON_GLOBE),
        "btn-portfolio.svg": button("Portfolio", False, ICON_ARROW),
        "btn-instagram.svg": button("Instagram", False, ICON_CAM),
        "btn-tiktok.svg": button("TikTok", False, ICON_NOTE),
    }
    for p in PROJECTS:
        files[f"card-{p['key']}.svg"] = card(**p)
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
    print(f"wrote {len(files)} files to {OUT}")


if __name__ == "__main__":
    main()
