"""assets/readme/reactions.svg — what the body does when the machine does something.
Five bays, one vector PepeBot per bay, each running the emote the firmware plays for that event."""
from lib import P, matrix, svg, grime_defs, grime, plate, rivets_box, text, chamfer, led, spin

W, H = 1200, 470

EMOTES = [
    ("system.idle", "IDLE", P["hull"], "slow breathe", "dim wave", "micro sway"),
    ("fee.collected", "FEED", P["amber"], "pulse", "amber chase", "arms grab"),
    ("swap.executed", "CRUNCH", P["sol"], "double flash", "flicker", "body shake"),
    ("distribution.done", "PAYOUT", P["phos"], "full burn", "green chase", "wave + hop"),
    ("guard.halt", "HALT", P["eye"], "dim / stutter", "red strobe", "head droop"),
]


def anim_rot(values, cx, cy, dur, times=None, begin=0):
    vals = ";".join(f"{v} {cx} {cy}" for v in values)
    kt = f' keyTimes="{times}"' if times else ""
    return (f'<animateTransform attributeName="transform" type="rotate" values="{vals}"{kt} dur="{dur}s" '
            f'begin="{begin}s" repeatCount="indefinite" additive="sum"/>')


def anim_tr(values, dur, times=None):
    kt = f' keyTimes="{times}"' if times else ""
    return (f'<animateTransform attributeName="transform" type="translate" values="{values}"{kt} '
            f'dur="{dur}s" repeatCount="indefinite" additive="sum"/>')


def minibot(kind):
    """Vector PepeBot in local coords: feet at y=0, eyes near y=-135."""
    hull, hi, lo, rust = P["hull"], P["hull_hi"], P["hull_lo"], P["rust"]
    # per-emote motion
    body_anim = arm_l = arm_r = head_anim = spring = ""
    eye_cls = f"eye-{kind}"
    if kind == "IDLE":
        body_anim = anim_tr("0 0;0 -2;0 0", 3.6)
        arm_l = anim_rot([0, -6, 0], -44, -60, 3.6)
        arm_r = anim_rot([0, 6, 0], 44, -60, 3.6)
    elif kind == "FEED":
        arm_l = anim_rot([0, -38, -30, 0], -44, -60, 1.1, "0;.35;.6;1")
        arm_r = anim_rot([0, 38, 30, 0], 44, -60, 1.1, "0;.35;.6;1")
        body_anim = anim_tr("0 0;0 2;0 0", 1.1)
    elif kind == "CRUNCH":
        body_anim = anim_tr("0 0;-3 0;3 0;-2 0;2 0;0 0;0 0", 0.9, "0;.1;.2;.3;.4;.5;1")
        arm_l = anim_rot([0, 10, -10, 0, 0], -44, -60, 0.9, "0;.15;.3;.45;1")
        arm_r = anim_rot([0, -10, 10, 0, 0], 44, -60, 0.9, "0;.15;.3;.45;1")
    elif kind == "PAYOUT":
        body_anim = anim_tr("0 0;0 -18;0 0;0 0", 1.3, "0;.3;.6;1")
        arm_l = anim_rot([60, 95, 60], -44, -60, 0.5)
        arm_r = anim_rot([-60, -95, -60], 44, -60, 0.5)
        spring = '<animateTransform attributeName="transform" type="scale" values="1 1;1 1.35;1 1;1 1" keyTimes="0;.3;.6;1" dur="1.3s" repeatCount="indefinite" additive="sum"/>'
    elif kind == "HALT":
        head_anim = anim_rot([0, 9, 9, 0], 0, -40, 6, "0;.2;.85;1")
        arm_l = anim_rot([0, -18, -18, 0], -44, -60, 6, "0;.2;.85;1")
        arm_r = anim_rot([0, 18, 18, 0], 44, -60, 6, "0;.2;.85;1")

    def zig(x):
        pts = [(x, -2)]
        for k in range(7):
            pts.append((x + (7 if k % 2 == 0 else -7), -5 - k * 3.4))
        pts.append((x, -30))
        return "M" + "L".join(f"{a:.1f} {b:.1f}" for a, b in pts)

    legs = (f'<g><path d="{zig(-20)}{zig(20)}" stroke="#8a8f86" stroke-width="3" fill="none"/>{spring}</g>'
            f'<ellipse cx="-20" cy="0" rx="14" ry="5" fill="{lo}" stroke="{hull}"/><ellipse cx="20" cy="0" rx="14" ry="5" fill="{lo}" stroke="{hull}"/>')

    def arm(side, anim):
        s = -1 if side == "l" else 1
        sx, sy = 44 * s, -60
        ex, ey = 64 * s, -38
        claw = "".join(f'<circle cx="{ex + dx*s:.1f}" cy="{ey + dy:.1f}" r="4.5" fill="{hull}" stroke="{lo}"/>'
                       for dx, dy in [(2, 12), (9, 6), (-6, 13)])
        return (f'<g><path d="M{sx} {sy}L{ex} {ey}" stroke="{hull}" stroke-width="8" stroke-linecap="round"/>'
                f'<path d="M{sx} {sy}L{ex} {ey}" stroke="{rust}" stroke-width="2" stroke-dasharray="2 5"/>'
                f'<circle cx="{sx}" cy="{sy}" r="7" fill="{hull}" stroke="{lo}" stroke-width="2"/>{claw}{anim}</g>')

    dome = "M-46 -32C-46 -86 -30 -112 0 -112C30 -112 46 -86 46 -32Z"
    arch = "M-26 -34C-26 -72 -16 -90 0 -90C16 -90 26 -72 26 -34Z"
    rivets = "".join(f'<circle cx="{x}" cy="{y}" r="2" fill="{hi}"/>' for x, y in
                     [(-14, -60), (14, -60), (-14, -44), (14, -44), (-36, -70), (36, -70), (-30, -92), (30, -92)])
    leds = "".join(f'<rect x="{-40 + i*10.5:.1f}" y="-33" width="7" height="5" class="led-{kind}" style="animation-delay:{i*0.09:.2f}s"/>'
                   for i in range(8))
    eyes = ""
    for s in (-1, 1):
        ex, ey = 30 * s, -136
        eyes += (f'<path d="M{10*s} -108L{ex - 4*s} {ey + 12}" stroke="#8a8f86" stroke-width="4"/>'
                 f'<circle cx="{ex}" cy="{ey}" r="19" fill="{lo}" stroke="{hull}" stroke-width="4"/>'
                 f'<circle cx="{ex}" cy="{ey}" r="14" fill="url(#eyeR)" class="{eye_cls}"/>'
                 f'<circle cx="{ex}" cy="{ey}" r="9" fill="none" stroke="#ffb199" stroke-width=".8" opacity=".6"/>'
                 f'<circle cx="{ex}" cy="{ey}" r="4.5" fill="none" stroke="#ffb199" stroke-width=".8" opacity=".6"/>'
                 f'<circle cx="{ex-6*s if s>0 else ex-6}" cy="{ey-5}" r="2.4" fill="#fff" opacity=".8"/>')
    head = (f'<g>{eyes}<path d="{dome}" fill="{hull}" stroke="{lo}" stroke-width="2"/>'
            f'<path d="M20 -108C36 -96 44 -70 46 -32H30C30 -70 26 -96 12 -110Z" fill="#3b8fa3" opacity=".45"/>'
            f'<path d="{arch}" fill="{lo}" opacity=".55"/><path d="{arch}" fill="none" stroke="{hi}" stroke-width="2" opacity=".6"/>'
            f'<path d="M-40 -58h8v6h-8zM28 -84l6 6" stroke="{rust}" stroke-width="2" opacity=".8"/>{rivets}'
            f'<rect x="-48" y="-36" width="96" height="10" fill="#2a2e22" stroke="{lo}"/>{leds}{head_anim}</g>')
    return (f'<g>{legs}<g>{arm("l", arm_l)}{arm("r", arm_r)}{head}{body_anim}</g></g>')


def bay(i, event, emote, col, eyes, leds, servo):
    x, y, w, h = 20 + i * 236, 20, 224, 430
    o = [plate(x, y, w, h, 12, P["deck"], P["hull_lo"], 2), rivets_box(x, y, w, h, 8, 2.4)]
    o.append(text(x + 16, y + 30, "EVENT", 10, P["mute"], ls=2))
    o.append(text(x + 16, y + 48, event, 13, P["text"], weight=700))
    d, mw = matrix(emote, 0, 0, 3.2)
    o.append(f'<rect x="{x+12}" y="{y+60}" width="{w-24}" height="36" fill="#000"/>'
             f'<rect x="{x+12}" y="{y+60}" width="{w-24}" height="36" fill="url(#unlit)"/>')
    o.append(f'<path d="{d}" fill="{col}" transform="translate({x + w/2 - mw/2:.1f} {y+67})" filter="url(#glow)"/>')
    # floor
    fy = y + 318
    o.append(f'<ellipse cx="{x+w/2}" cy="{fy+2}" rx="70" ry="9" fill="#000" opacity=".8"/>')
    o.append(f'<path d="M{x+14} {fy+8}H{x+w-14}" stroke="{P["seam"]}" stroke-width="2"/>')
    o.append(f'<g transform="translate({x + w/2} {fy})">{minibot(emote)}</g>')
    rows = [("EYES", eyes), ("LEDS", leds), ("SERVO", servo)]
    for k, (a, b) in enumerate(rows):
        ry = y + 356 + k * 20
        o.append(text(x + 16, ry, a, 10, P["mute"], ls=1.5) + text(x + w - 16, ry, b, 11, col if col != P["phos_dim"] else P["hull_hi"], "end", 700))
    return "".join(o)


def build():
    css = """
@keyframes eb{0%,100%{opacity:.45}50%{opacity:1}}
.eye-IDLE{animation:eb 3.6s ease-in-out infinite}
.eye-FEED{animation:eb .55s ease-in-out infinite}
.eye-CRUNCH{animation:ec .9s infinite}@keyframes ec{0%,8%,18%{opacity:1}4%,13%,30%,100%{opacity:.35}}
.eye-PAYOUT{opacity:1}
.eye-HALT{animation:eh 6s infinite}@keyframes eh{0%,15%{opacity:.9}20%{opacity:.12}22%{opacity:.5}24%,80%{opacity:.12}90%,100%{opacity:.9}}
.led-IDLE{fill:#4d6b25;animation:lw 2.4s ease-in-out infinite}
.led-FEED{fill:#ffae1a;animation:lc .8s steps(1) infinite}
.led-CRUNCH{fill:#14f195;animation:lc .25s steps(1) infinite}
.led-PAYOUT{fill:#b8ff4f;animation:lc .7s steps(1) infinite}
.led-HALT{fill:#ff2d17;animation:ls .5s steps(1) infinite}
@keyframes lw{0%,100%{opacity:.25}50%{opacity:.9}}
@keyframes lc{0%{opacity:1}30%{opacity:.15}}
@keyframes ls{0%{opacity:1}50%{opacity:.08}}
"""
    defs = (grime_defs("g", 31) +
            '<filter id="glow" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="1.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
            f'<pattern id="unlit" width="3.2" height="3.2" patternUnits="userSpaceOnUse" x="0" y="0"><rect width="2.2" height="2.2" fill="{P["phos_dim"]}" opacity=".22"/></pattern>'
            f'<radialGradient id="eyeR" cx=".45" cy=".42"><stop offset="0" stop-color="#ffd2c2"/><stop offset=".25" stop-color="{P["eye"]}"/><stop offset="1" stop-color="#6b0a02"/></radialGradient>')
    body = f'<rect width="{W}" height="{H}" fill="{P["void"]}"/>' + "".join(bay(i, *e) for i, e in enumerate(EMOTES)) + grime(W, H, "g", 0.1)
    return svg(W, H, body, css, defs, "PepeBot emote matrix: how the physical bot reacts to system events")


TARGETS = {"reactions.svg": build}
