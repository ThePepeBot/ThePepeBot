"""
PepeBot README asset kit.

Every animated SVG in assets/readme/ is generated from this folder so the
visual system stays consistent. GitHub renders SVGs through <img>, which means:
  - no JavaScript, no external fonts, no external images
  - CSS @keyframes inside <style> and SMIL (<animate*>) both work
  - raster images must be embedded as data: URIs
Run:  python3 scripts/readme-assets/build.py
"""
import base64
import io
import math
import os
from functools import lru_cache

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "assets", "readme")
LOGO = os.path.join(ROOT, "assets", "brand", "pepebot-logo.png")

# ------------------------------------------------------------------ palette
P = {
    "void": "#030504",       # the black behind everything
    "deck": "#0a0e0b",       # panel steel
    "deck2": "#111812",      # raised steel
    "seam": "#1d2a1c",       # panel seams / grid
    "hull": "#6e8c3a",       # PepeBot green metal
    "hull_hi": "#9dbb52",    # lit edge of the hull
    "hull_lo": "#34471d",    # hull in shadow
    "rust": "#7c3a1a",       # corrosion
    "rust_hi": "#b0582a",
    "eye": "#ff2d17",        # robot eye red
    "eye_hot": "#ffb199",
    "phos": "#b8ff4f",       # phosphor readout green
    "phos_dim": "#4d6b25",
    "amber": "#ffae1a",      # warnings / SIM markers
    "sol": "#14f195",        # solana accent (use sparingly)
    "sol2": "#9945ff",       # solana accent (use sparingly)
    "text": "#c9d6bf",
    "mute": "#6c7a66",
}
MONO = "'JetBrains Mono','SFMono-Regular','Cascadia Mono',Consolas,'Liberation Mono',Menlo,monospace"

# eye centres/radius as a fraction of the square logo (measured from the art)
EYES = [(0.297, 0.133), (0.696, 0.133)]
EYE_R = 0.088


@lru_cache(None)
def logo_uri(size: int, quality: int = 80) -> str:
    from PIL import Image
    im = Image.open(LOGO).convert("RGBA").resize((size, size), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=quality, method=6)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()


# ------------------------------------------------------------ 5x7 LED font
_F = {
    "A": [" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    "B": ["#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "],
    "C": [" ### ", "#   #", "#    ", "#    ", "#    ", "#   #", " ### "],
    "D": ["#### ", "#   #", "#   #", "#   #", "#   #", "#   #", "#### "],
    "E": ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"],
    "F": ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "],
    "G": [" ### ", "#   #", "#    ", "# ###", "#   #", "#   #", " ####"],
    "H": ["#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    "I": [" ### ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "],
    "J": ["  ###", "   # ", "   # ", "   # ", "   # ", "#  # ", " ##  "],
    "K": ["#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"],
    "L": ["#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"],
    "M": ["#   #", "## ##", "# # #", "# # #", "#   #", "#   #", "#   #"],
    "N": ["#   #", "#   #", "##  #", "# # #", "#  ##", "#   #", "#   #"],
    "O": [" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    "P": ["#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "],
    "Q": [" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"],
    "R": ["#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"],
    "S": [" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "],
    "T": ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "],
    "U": ["#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    "V": ["#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "],
    "W": ["#   #", "#   #", "#   #", "# # #", "# # #", "# # #", " # # "],
    "X": ["#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"],
    "Y": ["#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "],
    "Z": ["#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"],
    "0": [" ### ", "#   #", "#  ##", "# # #", "##  #", "#   #", " ### "],
    "1": ["  #  ", " ##  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "],
    "2": [" ### ", "#   #", "    #", "   # ", "  #  ", " #   ", "#####"],
    "3": ["#####", "   # ", "  #  ", "   # ", "    #", "#   #", " ### "],
    "4": ["   # ", "  ## ", " # # ", "#  # ", "#####", "   # ", "   # "],
    "5": ["#####", "#    ", "#### ", "    #", "    #", "#   #", " ### "],
    "6": ["  ## ", " #   ", "#    ", "#### ", "#   #", "#   #", " ### "],
    "7": ["#####", "    #", "   # ", "  #  ", " #   ", " #   ", " #   "],
    "8": [" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "],
    "9": [" ### ", "#   #", "#   #", " ####", "    #", "   # ", " ##  "],
    ".": ["     "] * 5 + [" ##  ", " ##  "],
    ",": ["     "] * 5 + ["  #  ", " #   "],
    "/": ["    #", "    #", "   # ", "  #  ", " #   ", "#    ", "#    "],
    "-": ["     ", "     ", "     ", "#####", "     ", "     ", "     "],
    ":": ["     ", " ##  ", " ##  ", "     ", " ##  ", " ##  ", "     "],
    "!": ["  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "     ", "  #  "],
    "?": [" ### ", "#   #", "    #", "   # ", "  #  ", "     ", "  #  "],
    ">": ["#    ", " #   ", "  #  ", "   # ", "  #  ", " #   ", "#    "],
    "<": ["    #", "   # ", "  #  ", " #   ", "  #  ", "   # ", "    #"],
    "[": [" ### ", " #   ", " #   ", " #   ", " #   ", " #   ", " ### "],
    "]": [" ### ", "   # ", "   # ", "   # ", "   # ", "   # ", " ### "],
    "(": ["   # ", "  #  ", " #   ", " #   ", " #   ", "  #  ", "   # "],
    ")": [" #   ", "  #  ", "   # ", "   # ", "   # ", "  #  ", " #   "],
    "+": ["     ", "  #  ", "  #  ", "#####", "  #  ", "  #  ", "     "],
    "=": ["     ", "     ", "#####", "     ", "#####", "     ", "     "],
    "%": ["##   ", "##  #", "   # ", "  #  ", " #   ", "#  ##", "   ##"],
    "_": ["     "] * 6 + ["#####"],
    "#": [" # # ", " # # ", "#####", " # # ", "#####", " # # ", " # # "],
    "'": ["  #  ", "  #  "] + ["     "] * 5,
    " ": ["     "] * 7,
}


def matrix(text: str, x: float, y: float, pitch: float, dot: float = None, gap_cols: int = 1):
    """Return (path_d, width) for text drawn as a 5x7 dot matrix.
    Each lit pixel is a small square; `pitch` is centre-to-centre spacing."""
    dot = dot if dot is not None else pitch * 0.72
    d = []
    cx = x
    for ch in text.upper():
        g = _F.get(ch, _F["?"])
        for r, row in enumerate(g):
            for c, px in enumerate(row):
                if px == "#":
                    px_x = cx + c * pitch
                    px_y = y + r * pitch
                    d.append(f"M{px_x:.1f} {px_y:.1f}h{dot:.1f}v{dot:.1f}h-{dot:.1f}z")
        cx += (5 + gap_cols) * pitch
    width = cx - x - gap_cols * pitch
    return "".join(d), width


def matrix_width(text, pitch, gap_cols=1):
    n = len(text)
    return n * (5 + gap_cols) * pitch - gap_cols * pitch


# ---------------------------------------------------------------- helpers
def svg(w, h, body, css="", defs="", title="PepeBot", extra_attr=""):
    reduce = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{title}" {extra_attr}>'
        f"<title>{title}</title>"
        f"<style>text{{font-family:{MONO}}}{css}{reduce}</style>"
        f"<defs>{defs}</defs>{body}</svg>"
    )


def grime_defs(uid="g", seed=7, opacity=0.35):
    """Static dirt / wear texture. Rendered once, never animated (cheap)."""
    return (
        f'<filter id="{uid}" x="0" y="0" width="100%" height="100%">'
        f'<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="{seed}" result="n"/>'
        f'<feColorMatrix in="n" type="matrix" values="0 0 0 0 0.55  0 0 0 0 0.42  0 0 0 0 0.25  0 0 0 -2.2 1.25" result="spots"/>'
        f'<feComposite in="spots" in2="SourceGraphic" operator="in"/>'
        f"</filter>"
        f'<filter id="{uid}s" x="0" y="0" width="100%" height="100%">'
        f'<feTurbulence type="turbulence" baseFrequency="0.012 0.35" numOctaves="1" seed="{seed+3}" result="t"/>'
        f'<feColorMatrix in="t" type="matrix" values="0 0 0 0 0.7  0 0 0 0 0.75  0 0 0 0 0.6  0 0 0 -3 1.05"/>'
        f"</filter>"
    )


def grime(w, h, uid="g", opacity=0.08, x=0, y=0):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#000" filter="url(#{uid})" opacity="{opacity}"/>'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#000" filter="url(#{uid}s)" opacity="{opacity*0.5:.3f}"/>'
    )


def chamfer(x, y, w, h, c=12):
    return (f"M{x+c} {y}H{x+w-c}L{x+w} {y+c}V{y+h-c}L{x+w-c} {y+h}H{x+c}"
            f"L{x} {y+h-c}V{y+c}Z")


def plate(x, y, w, h, c=12, fill=None, stroke=None, sw=1.5, extra=""):
    fill = fill or P["deck"]
    stroke = stroke or P["hull_lo"]
    return f'<path d="{chamfer(x,y,w,h,c)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'


def rivet(x, y, r=3.2):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{P["hull_lo"]}"/>'
            f'<circle cx="{x-r*0.3:.1f}" cy="{y-r*0.3:.1f}" r="{r*0.45:.1f}" fill="{P["hull_hi"]}" opacity=".55"/>')


def rivets_box(x, y, w, h, inset=8, r=2.6):
    return "".join(rivet(px, py, r) for px, py in
                   [(x+inset, y+inset), (x+w-inset, y+inset), (x+inset, y+h-inset), (x+w-inset, y+h-inset)])


def hazard_pattern(pid="hz", a=P["amber"], b="#0b0b06", size=14):
    return (f'<pattern id="{pid}" width="{size}" height="{size}" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<rect width="{size}" height="{size}" fill="{b}"/><rect width="{size/2}" height="{size}" fill="{a}"/></pattern>')


def grid_pattern(pid="grid", step=24, color=P["seam"], op=0.5):
    return (f'<pattern id="{pid}" width="{step}" height="{step}" patternUnits="userSpaceOnUse">'
            f'<path d="M{step} 0H0V{step}" fill="none" stroke="{color}" stroke-width="1" opacity="{op}"/></pattern>')


def dots_pattern(pid, pitch, dot, color, op=1.0):
    return (f'<pattern id="{pid}" width="{pitch}" height="{pitch}" patternUnits="userSpaceOnUse">'
            f'<rect width="{dot}" height="{dot}" fill="{color}" opacity="{op}"/></pattern>')


def gear(cx, cy, r, teeth, depth=None, hole=None, tooth_frac=0.5):
    depth = depth or r * 0.16
    ri = r - depth
    pts = []
    n = teeth * 4
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = r if (i % 4 in (1, 2)) else ri
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d = "M" + "L".join(f"{px:.1f} {py:.1f}" for px, py in pts) + "Z"
    if hole:
        d += (f"M{cx+hole} {cy}A{hole} {hole} 0 1 0 {cx-hole} {cy}"
              f"A{hole} {hole} 0 1 0 {cx+hole} {cy}Z")
    return d


def spin(cx, cy, dur, reverse=False):
    a, b = (360, 0) if reverse else (0, 360)
    return (f'<animateTransform attributeName="transform" type="rotate" '
            f'from="{a} {cx} {cy}" to="{b} {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/>')


def led(x, y, color, cls="", r=4):
    return (f'<g class="{cls}"><circle cx="{x}" cy="{y}" r="{r+3}" fill="{color}" opacity=".18"/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>'
            f'<circle cx="{x-r*0.35:.1f}" cy="{y-r*0.35:.1f}" r="{r*0.35:.1f}" fill="#fff" opacity=".6"/></g>')


def text(x, y, s, size=12, fill=None, anchor="start", weight=400, ls=0, extra=""):
    fill = fill or P["text"]
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}" letter-spacing="{ls}" {extra}>{s}</text>')


def packet_motion(path_id, dur, begin, rotate=False):
    rot = ' rotate="auto"' if rotate else ""
    return (f'<animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite"{rot}>'
            f'<mpath xlink:href="#{path_id}" href="#{path_id}"/></animateMotion>')


def pipe(d, w=12, pid=None, color=None, hi=None):
    """Industrial pipe: dark casing, lit ridge, seam line."""
    color = color or P["hull_lo"]
    hi = hi or P["hull"]
    idattr = f' id="{pid}"' if pid else ""
    return (f'<path{idattr} d="{d}" fill="none" stroke="#000" stroke-width="{w+4}" stroke-linejoin="round" opacity=".7"/>'
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{hi}" stroke-width="{max(1,w*0.18):.1f}" stroke-linejoin="round" opacity=".55" transform="translate(0 -{w*0.22:.1f})"/>')


def status_tag(x, y, label, color, anchor="start"):
    w = len(label) * 7.2 + 14
    x0 = x if anchor == "start" else x - w
    return (f'<g><rect x="{x0}" y="{y-12}" width="{w}" height="17" fill="none" stroke="{color}" stroke-width="1"/>'
            f'<rect x="{x0}" y="{y-12}" width="4" height="17" fill="{color}"/>'
            + text(x0 + 9, y + 1, label, 11, color, weight=700, ls=0.5) + "</g>")


def write(name, content):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    return p, len(content.encode())
