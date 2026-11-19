"""Generates the SVG assets used by README.md (assets/readme/*.svg).

Style: Apple-keynote darkness + restrained pixel art. No dependencies.
Run:  python scripts/build_readme_assets.py
"""
import base64
import random
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "assets" / "readme"
LOGOS = HERE / "logos"  # original project logos, embedded as data URIs

SANS = "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', 'Helvetica Neue', Inter, Arial, sans-serif"
MONO = "'SF Mono', ui-monospace, Menlo, 'Cascadia Code', Consolas, 'Liberation Mono', monospace"

BG = "#000000"
CARD = "#0b0b0e"
TEXT = "#f5f5f7"
TEXT2 = "#a1a1a6"
TEXT3 = "#6e6e73"
VIOLET = "#a78bfa"
BLUE = "#60a5fa"
PINK = "#f0abfc"
GREEN = "#4ade80"

# ---------------------------------------------------------------- pixel font (5x7, variable width)
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
    # rows beyond 7 are drawn above the cap height (the accent)
    "Í": ["..X", ".X.", "XXX", ".X.", ".X.", ".X.", ".X.", ".X.", "XXX"],
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
    " ": ["...", "...", "...", "...", "...", "...", "..."],
    ".": [".", ".", ".", ".", ".", ".", "X"],
    "-": ["...", "...", "...", "XXX", "...", "...", "..."],
}


def text_width(s, px):
    cols = sum(len(F[c][0]) for c in s) + max(len(s) - 1, 0)
    return cols * px


def pixel_text(s, x, y, px, fill, gap=None):
    """Return SVG rects drawing `s` with the pixel font, top-left at (x, y)."""
    gap = px * 0.14 if gap is None else gap
    out, cx = [], x
    for ch in s:
        g = F[ch]
        top = y - (len(g) - 7) * px
        for r, row in enumerate(g):
            for c, v in enumerate(row):
                if v == "X":
                    out.append(
                        f'<rect x="{cx + c * px:.1f}" y="{top + r * px:.1f}" '
                        f'width="{px - gap:.1f}" height="{px - gap:.1f}"/>'
                    )
        cx += (len(g[0]) + 1) * px
    return f'<g fill="{fill}">' + "".join(out) + "</g>"


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


def tile_base(x, y, size, gid):
    """App-icon style squircle (gradient + top shine + hairline)."""
    r = size * 0.24
    return (
        f'<defs><linearGradient id="{gid}t" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#312e81"/>'
        f'<stop offset=".55" stop-color="#6d28d9"/><stop offset="1" stop-color="#a21caf"/></linearGradient>'
        f'<linearGradient id="{gid}s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".2"/>'
        f'<stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>'
        f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{r:.0f}" fill="url(#{gid}t)"/>'
        f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{r:.0f}" fill="url(#{gid}s)"/>'
        f'<rect x="{x + .5}" y="{y + .5}" width="{size - 1}" height="{size - 1}" rx="{r:.0f}" fill="none" stroke="#fff" stroke-opacity=".25"/>'
    )


def monogram_tile(x, y, size, px, gid):
    """App-icon style squircle with the pixel 'DV' monogram."""
    r = size * 0.24
    mw, mh = text_width("DV", px), 7 * px
    mx, my = x + (size - mw) / 2, y + (size - mh) / 2
    return (
        f'<defs><linearGradient id="{gid}t" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#312e81"/>'
        f'<stop offset=".55" stop-color="#6d28d9"/><stop offset="1" stop-color="#a21caf"/></linearGradient>'
        f'<linearGradient id="{gid}s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".2"/>'
        f'<stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        f'<linearGradient id="{gid}m" gradientUnits="userSpaceOnUse" x1="{mx}" y1="{my}" x2="{mx + mw}" y2="{my + mh}">'
        f'<stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#ddd6fe"/></linearGradient></defs>'
        f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{r:.0f}" fill="url(#{gid}t)"/>'
        f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{r:.0f}" fill="url(#{gid}s)"/>'
        f'<rect x="{x + .5}" y="{y + .5}" width="{size - 1}" height="{size - 1}" rx="{r:.0f}" fill="none" stroke="#fff" stroke-opacity=".25"/>'
        f'<g opacity=".28">{pixel_text("DV", mx + px * 0.35, my + px * 0.35, px, "#000")}</g>'
        + pixel_text("DV", mx, my, px, f"url(#{gid}m)")
    )


# ---------------------------------------------------------------- hero
def hero():
    W, H = 1280, 560
    rnd = random.Random(7)
    defs = [
        f'<clipPath id="c"><rect width="{W}" height="{H}" rx="28"/></clipPath>',
        '<radialGradient id="g1"><stop offset="0" stop-color="#7c3aed" stop-opacity=".55"/><stop offset="1" stop-color="#7c3aed" stop-opacity="0"/></radialGradient>',
        '<radialGradient id="g2"><stop offset="0" stop-color="#2563eb" stop-opacity=".45"/><stop offset="1" stop-color="#2563eb" stop-opacity="0"/></radialGradient>',
        '<radialGradient id="g3"><stop offset="0" stop-color="#db2777" stop-opacity=".30"/><stop offset="1" stop-color="#db2777" stop-opacity="0"/></radialGradient>',
        '<pattern id="grid" width="16" height="16" patternUnits="userSpaceOnUse"><rect width="2" height="2" fill="#fff" opacity=".07"/></pattern>',
        '<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="28"/></filter>',
    ]
    px = 16
    x0 = 72
    w2 = text_width("VILLAR", px)
    defs.append(iri_gradient("iri", x0, x0 + w2))

    b = [f'<defs>{"".join(defs)}</defs>', '<g clip-path="url(#c)">', f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    # drifting glows
    for gid, cx, cy, r, dx, dy, dur in [
        ("g1", 980, 120, 520, -60, 40, 14),
        ("g2", 300, 600, 560, 80, -30, 18),
        ("g3", 1180, 540, 380, -40, -50, 16),
    ]:
        b.append(
            f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r * 0.7:.0f}" fill="url(#{gid})">'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;{dx} {dy};0 0" '
            f'dur="{dur}s" repeatCount="indefinite"/></ellipse>'
        )
    b.append(f'<rect width="{W}" height="{H}" fill="url(#grid)"/>')
    # a few quiet pixels
    for _ in range(18):
        x, y = rnd.randrange(0, W // 16) * 16, rnd.randrange(0, H // 16) * 16
        col = rnd.choice([TEXT, VIOLET, BLUE])
        b.append(
            f'<rect x="{x}" y="{y}" width="4" height="4" fill="{col}" opacity=".15">'
            f'<animate attributeName="opacity" values=".05;.45;.05" dur="{rnd.uniform(5, 9):.1f}s" '
            f'begin="{rnd.uniform(0, 4):.1f}s" repeatCount="indefinite"/></rect>'
        )
    b.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="28" fill="none" stroke="#ffffff" stroke-opacity=".08"/>')
    b.append("</g>")

    # pixel wordmark
    y1 = 84
    y2 = y1 + 7 * px + 26
    b.append(pixel_text("DAVID", x0, y1, px, "url(#iri)"))
    b.append(pixel_text("VILLAR", x0, y2, px, "url(#iri)"))
    b.append(
        f'<rect x="{x0 + w2 + px}" y="{y2}" width="{px * 2.4:.0f}" height="{7 * px - 2}" fill="{VIOLET}">'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/></rect>'
    )
    # headline
    ty = y2 + 7 * px + 72
    b.append(
        f'<text x="{x0}" y="{ty}" font-family="{SANS}" font-size="34" font-weight="600" letter-spacing="-.6" fill="{TEXT}">'
        f'Full‑stack developer.</text>'
        f'<text x="{x0}" y="{ty + 44}" font-family="{SANS}" font-size="34" font-weight="600" letter-spacing="-.6" fill="{TEXT3}">'
        f'Webs rápidas, diseño cuidado y código sólido.</text>'
    )
    # meta line
    meta = ["VIGO, ES", "GYLEVEN", "DURANDEV"]
    mx, my = x0, H - 44
    for i, m in enumerate(meta):
        b.append(f'<text x="{mx}" y="{my}" font-family="{MONO}" font-size="14" letter-spacing="1.5" fill="{TEXT3}">{m}</text>')
        mx += len(m) * 10 + 22
        if i < len(meta) - 1:
            b.append(f'<rect x="{mx - 15}" y="{my - 8}" width="5" height="5" fill="{VIOLET}"/>')

    # app-icon tile with the pixel avatar
    ts = 300
    tx, ty0 = 900, (H - ts) / 2
    sp = 16
    b.append(
        f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -6;0 0" dur="6s" repeatCount="indefinite"/>'
        f'<rect x="{tx + 30}" y="{ty0 + 60}" width="{ts - 60}" height="{ts - 40}" rx="60" fill="#a855f7" opacity=".5" filter="url(#blur)"/>'
        + tile_base(tx, ty0, ts, "ha")
        + sprite(AVATAR, AVATAR_PAL, tx + (ts - 16 * sp) / 2 - sp / 2, ty0 + (ts - 16 * sp) / 2 + 4, sp)
        + "</g>"
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
        b.append(sprite(icon, {"X": txt}, x, (h - len(icon) * 2.5) / 2, 2.5))
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
        f'<text x="{W / 2}" y="30" text-anchor="middle" font-family="{MONO}" font-size="15" letter-spacing="3" fill="#8b5cf6">'
        f'{num} — {escape(caption)}</text>'
    )
    b.append(pixel_text(title, x, 66, px, "url(#h)"))
    b.append(
        f'<rect x="{W / 2 - 220}" y="{H - 14}" width="440" height="1" fill="url(#hl)"/>'
        '<defs><linearGradient id="hl"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset=".5" stop-color="#8b5cf6" stop-opacity=".6"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>'
    )
    return svg(W, H, "".join(b), title)


# ---------------------------------------------------------------- terminal (neofetch + about)
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


NEOFETCH = [
    ("Role", "Full-stack developer"),
    ("Work", "Gyleven  ·  durandev (freelance)"),
    ("Location", "Vigo, Galicia, España"),
    ("Languages", "TypeScript · JavaScript · Python · Java · PHP"),
    ("Frontend", "React · Next.js · Vite · Tailwind · shadcn/ui"),
    ("Backend", "Node.js · Supabase · Firebase · Vercel"),
]

# (paragraph start?, text) — keep lines under ~92 chars
ABOUT = [
    (True, "Desarrollador full-stack en Gyleven. En paralelo, como durandev, diseño y desarrollo"),
    (False, "webs y tiendas online para negocios de Vigo y Galicia: rendimiento, SEO y mantenimiento."),
    (True, "Construyo y mantengo productos propios en producción, de la interfaz a la base de datos:"),
    (False, "¿Qué coche es?, Andén, Llavero y Tilo."),
    (True, "Día a día: TypeScript, React y Next.js, con Supabase o Firebase y despliegue en Vercel."),
    (True, "Cuido el rendimiento, el SEO técnico, la accesibilidad y la seguridad de lo que publico."),
]


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
        return "".join([
            f'<g>{fade_in(t0, 0.01)}',
            f'<text y="{y}" font-family="{MONO}" font-size="{fs}" xml:space="preserve">'
            f'<tspan x="{x0}" fill="{VIOLET}" font-weight="700">{p}</tspan><tspan fill="{BLUE}"> ~ </tspan><tspan fill="{TEXT}">% </tspan></text>',
            f'<clipPath id="{cid}"><rect x="{x0 + pre_w}" y="{y - 26}" width="{full:.1f}" height="36">'
            f'<animate attributeName="width" values="0;0;{steps}" keyTimes="0;{t0 / (t0 + t_type):.3f};'
            + ";".join(f"{(t0 + t_type * i / n) / (t0 + t_type):.3f}" for i in range(n + 1))
            + f'" dur="{t0 + t_type:.2f}s" calcMode="discrete" fill="freeze"/></rect></clipPath>',
            f'<text x="{x0 + pre_w}" y="{y}" font-family="{MONO}" font-size="{fs}" fill="{TEXT}" clip-path="url(#{cid})">{escape(cmd)}</text>',
            "</g>",
        ])

    # 1) neofetch
    b.append(prompt(y, "neofetch", 0.4, 0.7))
    t = 1.35
    y += lh + 14
    tile = 196
    b.append(f'<g>{fade_in(t)}' + monogram_tile(x0 + 4, y - 6, tile, 13, "nm") + "</g>")
    ix = x0 + tile + 64
    yy = y + 14
    head = [
        f'<tspan fill="{VIOLET}" font-weight="700">david</tspan><tspan fill="{TEXT}">@vigo</tspan>',
        f'<tspan fill="{TEXT3}">{"-" * 16}</tspan>',
    ]
    for k, v in NEOFETCH:
        pad = " " * (11 - len(k))
        head.append(
            f'<tspan fill="{VIOLET}" font-weight="700">{k}</tspan><tspan fill="{TEXT3}">:{pad}</tspan>'
            f'<tspan fill="{TEXT}">{escape(v)}</tspan>'
        )
    for i, line in enumerate(head):
        b.append(f'<text x="{ix}" y="{yy}" font-family="{MONO}" font-size="{fs}" xml:space="preserve">{fade_in(t + 0.06 * i)}{line}</text>')
        yy += lh
    cols = ["#1c1c21", "#ff5f57", GREEN, "#febc2e", BLUE, VIOLET, PINK, TEXT]
    tt = t + 0.06 * len(head)
    blocks = "".join(f'<rect x="{ix + i * 34}" y="{yy - 10}" width="30" height="16" fill="{c}"/>' for i, c in enumerate(cols))
    b.append(f"<g>{fade_in(tt)}{blocks}</g>")
    y = max(yy, y + tile) + lh + 26

    # 2) cat sobre-mi.md
    t2 = tt + 0.6
    b.append(prompt(y, "cat sobre-mi.md", t2, 0.9))
    t3 = t2 + 1.1
    y += lh + 6
    for i, (first, ln) in enumerate(ABOUT):
        if first and i:
            y += 10
        arrow = f'<tspan fill="{GREEN}">→ </tspan>' if first else '<tspan>  </tspan>'
        b.append(
            f'<text x="{x0}" y="{y}" font-family="{MONO}" font-size="{fs}" fill="{TEXT2}" xml:space="preserve">{fade_in(t3 + i * 0.12)}'
            f'{arrow}{escape(ln)}</text>'
        )
        y += lh
    y += 18
    # 3) idle prompt with cursor
    t4 = t3 + 0.12 * len(ABOUT) + 0.4
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
    "huella": (
        ["...XX..XX...", "...XX..XX...", "XX........XX", "XX........XX", "....XXXX....",
         "...XXXXXX...", "..XXXXXXXX..", "..XXXXXXXX..", "...XX..XX..."],
        {"X": "#fdba74"},
    ),
    "shield": (
        [".XXXXXXXXXX.", ".X........X.", ".X......C.X.", ".X.....C..X.", ".X.C..C...X.",
         ".X..CC....X.", "..X......X..", "...X....X...", "....XXXX...."],
        {"X": TEXT, "C": GREEN},
    ),
    "interstellar": (
        ["....OOOO....", "..OO....OO..", ".O........O.", ".O..KKKK..O.", "YYYYKKKKYYYY",
         "YYYYKKKKYYYY", ".O..KKKK..O.", ".O........O.", "..OO....OO..", "....OOOO...."],
        {"O": "#fb923c", "Y": "#fde68a", "K": "#000000"},
    ),
    "modular": (
        ["..X......X..", "XXXXXXXXXXXX", "XXXXXXXXXXXX", "X..........X", "X.AA.BB.AA.X",
         "X..........X", "X.BB.AA.BB.X", "X..........X", "X.AA.BB....X", "XXXXXXXXXXXX"],
        {"X": TEXT, "A": BLUE, "B": VIOLET},
    ),
}

TILE_GRAD = {
    "durandev": ("#1e1b4b", "#6d28d9"),
    "quecoche": ("#0f172a", "#2563eb"),
    "anden": ("#042f2e", "#0f766e"),
    "llavero": ("#18181b", "#52525b"),
    "tilo": ("#052e16", "#15803d"),
    "stackhub": ("#1f2937", "#4338ca"),
    "huella": ("#431407", "#c2410c"),
    "shield": ("#052e16", "#166534"),
    "interstellar": ("#0c0a09", "#44403c"),
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


def card(key, title, url_label, desc, chips, status, accent, logo=None, logo_mode="full"):
    W, H = 620, 350
    icon, pal = ICONS.get(key, (None, None))
    g0, g1 = TILE_GRAD[key]
    b = [
        '<defs>'
        f'<clipPath id="c"><rect width="{W}" height="{H}" rx="26"/></clipPath>'
        f'<radialGradient id="glow"><stop offset="0" stop-color="{accent}" stop-opacity=".26"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="t" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{g0}"/><stop offset="1" stop-color="{g1}"/></linearGradient>'
        '<linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".18"/><stop offset=".55" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        '<pattern id="grid" width="12" height="12" patternUnits="userSpaceOnUse"><rect width="2" height="2" fill="#fff" opacity=".05"/></pattern>'
        '</defs>',
        f'<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="{CARD}"/>',
        f'<rect width="{W}" height="{H}" fill="url(#grid)"/>',
        f'<ellipse cx="{W - 40}" cy="10" rx="300" ry="220" fill="url(#glow)"/></g>',
        f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="26" fill="none" stroke="#fff" stroke-opacity=".1" stroke-width="1.5"/>',
    ]
    # icon tile: the project's own logo when it has one, else a pixel icon
    tx, ty, ts = 34, 34, 92
    if logo:
        uri = data_uri(LOGOS / logo)
        if logo_mode == "full":  # square app icon: just round its corners
            art = (f'<clipPath id="lc"><rect x="{tx}" y="{ty}" width="{ts}" height="{ts}" rx="22"/></clipPath>'
                   f'<image href="{uri}" x="{tx}" y="{ty}" width="{ts}" height="{ts}" clip-path="url(#lc)" preserveAspectRatio="xMidYMid slice"/>')
        else:  # transparent mark: place it on the gradient tile
            pad = ts * 0.2
            art = (f'<rect x="{tx}" y="{ty}" width="{ts}" height="{ts}" rx="22" fill="url(#t)"/>'
                   f'<rect x="{tx}" y="{ty}" width="{ts}" height="{ts}" rx="22" fill="url(#s)"/>'
                   f'<image href="{uri}" x="{tx + pad}" y="{ty + pad}" width="{ts - 2 * pad}" height="{ts - 2 * pad}"/>')
        b.append(art + f'<rect x="{tx + .5}" y="{ty + .5}" width="{ts - 1}" height="{ts - 1}" rx="22" fill="none" stroke="#fff" stroke-opacity=".2"/>')
    else:
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
    dot = {"LIVE": GREEN, "API": BLUE, "TEAM": VIOLET}.get(status, TEXT2)
    b.append(
        f'<g transform="translate({W - 34 - sw} 40)"><rect width="{sw}" height="30" rx="15" fill="#fff" fill-opacity=".06" stroke="#fff" stroke-opacity=".12"/>'
        f'<rect x="15" y="11" width="8" height="8" fill="{dot}"/>'
        f'<text x="30" y="20" font-family="{MONO}" font-size="13" font-weight="600" letter-spacing="1.5" fill="{TEXT}">{status}</text></g>'
    )
    # title + url
    b.append(
        f'<text x="34" y="172" font-family="{SANS}" font-size="34" font-weight="700" letter-spacing="-.6" fill="{TEXT}">{escape(title)}</text>'
        f'<text x="34" y="202" font-family="{MONO}" font-size="15" fill="{accent}">{escape(url_label)} ↗</text>'
    )
    lines = wrap(desc, 54)
    assert len(lines) <= 2, f"{key}: description too long"
    for i, ln in enumerate(lines):
        b.append(f'<text x="34" y="{238 + i * 27}" font-family="{SANS}" font-size="20" fill="{TEXT2}">{escape(ln)}</text>')
    # chips
    cx = 34
    for c in chips:
        w = len(c) * 9 + 26
        assert cx + w <= W - 30, f"{key}: too many chips"
        b.append(
            f'<rect x="{cx}" y="292" width="{w:.0f}" height="32" rx="9" fill="#17171c" stroke="#2a2a31"/>'
            f'<text x="{cx + 13}" y="313" font-family="{MONO}" font-size="14.5" fill="#d4d4d8">{escape(c)}</text>'
        )
        cx += w + 8
    # transparent margin so neighbouring cards in the README don't touch
    m = CARD_MARGIN
    return svg(W + 2 * m, H + 2 * m, f'<g transform="translate({m} {m})">' + "".join(b) + "</g>", title)


CARD_MARGIN = 22


def data_uri(path):
    mime = {".png": "image/png", ".svg": "image/svg+xml"}[path.suffix]
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


PROJECTS = [
    dict(key="durandev", title="durandev", url_label="durandev.vercel.app",
         desc="Mi marca freelance: webs rápidas, tiendas online y SEO para negocios de Vigo y Galicia.",
         chips=["Next.js", "TypeScript", "Tailwind", "shadcn/ui", "Motion"], status="LIVE", accent=VIOLET,
         logo="durandev.png", logo_mode="mark"),
    dict(key="quecoche", title="¿Qué coche es?", url_label="quecochees.es",
         desc="Identifica cualquier coche por foto con IA: modelo, ficha técnica y precio de segunda mano.",
         chips=["Next.js", "TypeScript", "Gemini API", "Upstash", "Zod"], status="LIVE", accent=BLUE, logo="quecoche.png"),
    dict(key="anden", title="Andén", url_label="andentren.es",
         desc="Retrasos, avisos e incidencias de Renfe en directo con datos oficiales y mapa de trenes.",
         chips=["JavaScript", "Vercel Functions", "GTFS-Realtime", "Gemini"], status="LIVE", accent="#60a5fa", logo="anden.png"),
    dict(key="llavero", title="Llavero", url_label="app-llavero.vercel.app",
         desc="Gestor de contraseñas con cifrado en el navegador, códigos 2FA y extensión que autocompleta.",
         chips=["React", "TypeScript", "Firebase", "Vite", "Vitest"], status="LIVE", accent="#60a5fa", logo="llavero.svg"),
    dict(key="tilo", title="Tilo", url_label="app-tilo.vercel.app",
         desc="Presupuesto del hogar compartido: sueldos, gastos por categoría, ahorro e informe mensual.",
         chips=["React 19", "TypeScript", "Supabase", "TanStack Query"], status="LIVE", accent="#34d399", logo="tilo.png"),
    dict(key="stackhub", title="StackHub", url_label="stackhub-app.vercel.app",
         desc="Más de 150 recursos gratuitos para diseñadores y devs: iconos, fuentes, UI y componentes.",
         chips=["Next.js", "React", "Tailwind", "Framer Motion"], status="LIVE", accent="#facc15", logo="stackhub.png"),
    dict(key="huella", title="La Huella de Puri", url_label="lahuelladepuri.vercel.app",
         desc="Tienda y catálogo artesanal con panel de administración para gestionar productos.",
         chips=["Next.js", "React 19", "Supabase", "Tailwind"], status="LIVE", accent="#fdba74"),
    dict(key="shield", title="Security Verifier", url_label="github.com/davidvillard/drfbackendcheck",
         desc="API que analiza URLs, emails, teléfonos y SMS sospechosos con VirusTotal y Neutrino.",
         chips=["Python", "Django REST", "Docker", "Render"], status="API", accent=GREEN),
    dict(key="interstellar", title="Interstellar", url_label="interstellarfanpage.netlify.app",
         desc="Fan page de la película con login/registro, contenido exclusivo y base de datos.",
         chips=["Astro", "Auth.js", "Astro DB", "Tailwind", "Docker"], status="LIVE", accent="#fb923c"),
    dict(key="modular", title="Modular", url_label="github.com/sempereluismi/modular",
         desc="Gestión de horarios y módulos de un instituto. Proyecto en equipo con Luis, Andrea y Manuel.",
         chips=["React", "PHP", "Tailwind", "JavaScript"], status="TEAM", accent=BLUE),
]


# ---------------------------------------------------------------- tech specs (Apple spec-sheet)
SPECS = [
    ("DÍA A DÍA", True, [
        ("Lenguajes", "TypeScript · JavaScript · SQL", VIOLET),
        ("Frontend", "React · Next.js · Vite · Tailwind CSS · shadcn/ui · Motion", BLUE),
        ("Backend y datos", "Node.js · Supabase · Firebase · Vercel Functions · Upstash", PINK),
        ("Herramientas", "TanStack Query · Zod · Vitest · Gemini API", GREEN),
        ("Deploy", "Vercel · Git · GitHub", "#febc2e"),
    ]),
    ("TAMBIÉN SÉ", False, [
        ("Lenguajes", "Python · Java · PHP", TEXT3),
        ("Frameworks", "Django REST Framework · Express · Vue · Astro · Bootstrap", TEXT3),
        ("Datos y otros", "MySQL · MongoDB · Docker · WordPress · Netlify · Postman", TEXT3),
    ]),
]


def specs():
    W = 1280
    rh = 66
    gh = 64
    H = 24 + sum(gh + rh * len(rows) for _, _, rows in SPECS) + 24
    b = [
        f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="26" fill="{CARD}" stroke="#fff" stroke-opacity=".1" stroke-width="1.5"/>'
    ]
    y = 24
    for gi, (group, main, rows) in enumerate(SPECS):
        if gi:
            b.append(f'<rect x="48" y="{y}" width="{W - 96}" height="1" fill="#fff" fill-opacity=".14"/>')
        b.append(
            f'<text x="48" y="{y + 42}" font-family="{MONO}" font-size="14" letter-spacing="3" '
            f'fill="{VIOLET if main else TEXT3}">{group}</text>'
        )
        y += gh
        for i, (k, v, c) in enumerate(rows):
            cy = y + rh / 2
            b.append(sprite(["XX", "XX"], {"X": c}, 48, cy - 9, 5))
            b.append(f'<text x="76" y="{cy + 7}" font-family="{SANS}" font-size="19" font-weight="500" fill="{TEXT3}">{k}</text>')
            b.append(
                f'<text x="320" y="{cy + 8}" font-family="{SANS}" font-size="22" font-weight="600" letter-spacing="-.2" '
                f'fill="{TEXT if main else TEXT2}">{escape(v)}</text>'
            )
            if i < len(rows) - 1:
                b.append(f'<rect x="48" y="{y + rh}" width="{W - 96}" height="1" fill="#fff" fill-opacity=".07"/>')
            y += rh
    return svg(W, H, "".join(b), "Tech specs")


# ---------------------------------------------------------------- footer
def footer():
    W, H = 1280, 280
    b = [
        f'<defs><clipPath id="c"><rect width="{W}" height="{H}" rx="28"/></clipPath>'
        '<radialGradient id="g"><stop offset="0" stop-color="#7c3aed" stop-opacity=".45"/><stop offset="1" stop-color="#7c3aed" stop-opacity="0"/></radialGradient>'
        '<pattern id="grid" width="16" height="16" patternUnits="userSpaceOnUse"><rect width="2" height="2" fill="#fff" opacity=".07"/></pattern></defs>',
        f'<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="{BG}"/>',
        f'<ellipse cx="{W / 2}" cy="{H + 40}" rx="620" ry="240" fill="url(#g)"/>',
        f'<rect width="{W}" height="{H}" fill="url(#grid)"/>',
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="28" fill="none" stroke="#fff" stroke-opacity=".08"/></g>',
    ]
    b.append(
        f'<text x="{W / 2}" y="58" text-anchor="middle" font-family="{MONO}" font-size="15" letter-spacing="3" fill="{VIOLET}">'
        f'05 — contacto</text>'
    )
    px = 12
    t1 = "HABLEMOS"
    w1 = text_width(t1, px)
    b.append(f'<defs>{iri_gradient("f", (W - w1) / 2, (W + w1) / 2)}</defs>')
    b.append(pixel_text(t1, (W - w1) / 2, 82, px, "url(#f)"))
    b.append(
        f'<text x="{W / 2}" y="212" text-anchor="middle" font-family="{SANS}" font-size="24" font-weight="600" '
        f'letter-spacing="-.3" fill="{TEXT2}">¿Tienes un proyecto en mente? Escríbeme en durandev.vercel.app</text>'
    )
    b.append(
        f'<text x="{W / 2}" y="246" text-anchor="middle" font-family="{MONO}" font-size="14" letter-spacing="1.5" fill="{TEXT3}">'
        f'VIGO, ES  ·  @durandev_</text>'
    )
    return svg(W, H, "".join(b), "Hablemos — durandev.vercel.app")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    files = {
        "hero.svg": hero(),
        "terminal.svg": terminal(),
        "specs.svg": specs(),
        "footer.svg": footer(),
        "header-sobre-mi.svg": header("01", "SOBRE MÍ", "whoami"),
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
    for stale in set(p.name for p in OUT.glob("*.svg")) - set(files):
        (OUT / stale).unlink()
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
    print(f"wrote {len(files)} files to {OUT}")


if __name__ == "__main__":
    main()
