"""assets/readme/hero-online.svg — the unit powering up inside its reactor housing."""
import math
import random
from lib import (P, EYES, EYE_R, logo_uri, matrix, svg, grime_defs, grime, plate,
                 rivets_box, hazard_pattern, grid_pattern, dots_pattern, spin, led,
                 text, packet_motion, pipe, status_tag, chamfer)

W, H = 1200, 740
CX, CY, R = 600, 372, 250


def glow_defs():
    return (
        '<filter id="glow" x="-20%" y="-60%" width="140%" height="220%">'
        '<feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        '<filter id="softglow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>'
        f'<radialGradient id="eyeglow"><stop offset="0" stop-color="{P["eye_hot"]}" stop-opacity=".95"/>'
        f'<stop offset=".35" stop-color="{P["eye"]}" stop-opacity=".75"/><stop offset="1" stop-color="{P["eye"]}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="core"><stop offset="0" stop-color="{P["hull"]}" stop-opacity=".22"/>'
        f'<stop offset=".7" stop-color="{P["hull_lo"]}" stop-opacity=".08"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{P["phos"]}" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="{P["phos"]}" stop-opacity=".22"/></linearGradient>'
        f'<clipPath id="reactor"><circle cx="{CX}" cy="{CY}" r="{R-12}"/></clipPath>'
        f'<clipPath id="tape"><rect x="44" y="470" width="266" height="146"/></clipPath>'
        f'<clipPath id="chart"><rect x="892" y="470" width="262" height="112"/></clipPath>'
        f'<clipPath id="ticker"><rect x="76" y="700" width="1048" height="26"/></clipPath>'
        f'<clipPath id="reels"><rect x="900" y="354" width="246" height="52"/></clipPath>'
    )


def top_bar():
    d, w = matrix("PEPEBOT // ONLINE", 48, 31, 3.4)
    out = [plate(24, 20, 1152, 46, 10, P["deck2"], P["hull_lo"])]
    out.append(f'<rect x="42" y="27" width="{w+14:.0f}" height="32" fill="url(#unlit)"/>')
    out.append(f'<path d="{d}" fill="{P["phos"]}" filter="url(#glow)" class="flick"/>')
    out.append(text(w + 76, 48, "PEPEBOT-OS 0.1  /  UNIT 00  /  FEE ROUTING + ASSET PURCHASE + HOLDER DISTRIBUTION", 11, P["mute"], ls=0.4))
    out.append(f'<g class="blink1">{status_tag(1160, 47, "MODE: SIMULATION", P["amber"], "end")}</g>')
    return "".join(out)


def reactor():
    o = []
    o.append(f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="url(#core)"/>')
    o.append(f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="{P["hull_lo"]}" stroke-width="3"/>')
    # rotating tick ring
    ticks = []
    for i in range(120):
        a = 2 * math.pi * i / 120
        r1 = R - (18 if i % 10 == 0 else 10)
        x1, y1 = CX + r1 * math.cos(a), CY + r1 * math.sin(a)
        x2, y2 = CX + (R - 3) * math.cos(a), CY + (R - 3) * math.sin(a)
        ticks.append(f"M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}")
    o.append(f'<g><path d="{"".join(ticks)}" stroke="{P["hull"]}" stroke-width="1.6" opacity=".75"/>{spin(CX, CY, 90)}</g>')
    # rust-flecked counter ring
    o.append(f'<g><circle cx="{CX}" cy="{CY}" r="{R-26}" fill="none" stroke="{P["phos_dim"]}" stroke-width="2" '
             f'stroke-dasharray="3 9 44 9 12 20"/>{spin(CX, CY, 40, True)}</g>')
    o.append(f'<circle cx="{CX}" cy="{CY}" r="{R-34}" fill="none" stroke="{P["rust"]}" stroke-width="1" stroke-dasharray="1 7" opacity=".7"/>')
    for rr in (160, 110, 60):
        o.append(f'<circle cx="{CX}" cy="{CY}" r="{rr}" fill="none" stroke="{P["seam"]}" stroke-width="1"/>')
    o.append(f'<path d="M{CX-R+30} {CY}H{CX+R-30}M{CX} {CY-R+30}V{CY+R-30}" stroke="{P["seam"]}" stroke-width="1"/>')
    # radar sweep (behind the bot)
    sweep = []
    for k, (span, op) in enumerate([(44, .05), (26, .08), (12, .12)]):
        a0 = math.radians(-90)
        a1 = math.radians(-90 - span)
        x0, y0 = CX + (R - 14) * math.cos(a0), CY + (R - 14) * math.sin(a0)
        x1, y1 = CX + (R - 14) * math.cos(a1), CY + (R - 14) * math.sin(a1)
        sweep.append(f'<path d="M{CX} {CY}L{x0:.1f} {y0:.1f}A{R-14} {R-14} 0 0 0 {x1:.1f} {y1:.1f}Z" fill="{P["phos"]}" opacity="{op}"/>')
    sweep.append(f'<path d="M{CX} {CY}V{CY-R+14}" stroke="{P["phos"]}" stroke-width="1.5" opacity=".7"/>')
    o.append(f'<g clip-path="url(#reactor)"><g>{"".join(sweep)}{spin(CX, CY, 5)}</g></g>')
    # blips that the sweep "finds"
    for (bx, by, dl) in [(470, 250, 0.3), (742, 470, 2.2), (690, 205, 4.1), (455, 505, 1.4)]:
        o.append(f'<circle cx="{bx}" cy="{by}" r="3" fill="{P["sol"]}" class="blip" style="animation-delay:{dl}s"/>')

    # the bot itself
    S = 430
    lx, ly = CX - S / 2, CY - S / 2 - 7
    eyes = []
    for (fx, fy) in EYES:
        ex, ey = lx + fx * S, ly + fy * S
        er = EYE_R * S
        eyes.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="{er*1.6:.1f}" fill="url(#eyeglow)" class="eyepulse" style="mix-blend-mode:screen"/>')
        for k in range(3):
            eyes.append(
                f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="4" fill="none" stroke="{P["eye_hot"]}" stroke-width="1.6" opacity="0">'
                f'<animate attributeName="r" values="4;{er*0.95:.1f}" dur="2.4s" begin="{k*0.8}s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values=".9;0" dur="2.4s" begin="{k*0.8}s" repeatCount="indefinite"/></circle>')
    o.append(
        f'<g><image href="{logo_uri(520)}" x="{lx}" y="{ly}" width="{S}" height="{S}"/>'
        f'{"".join(eyes)}'
        f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -7;0 0" keyTimes="0;.5;1" '
        f'calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1" dur="3.2s" repeatCount="indefinite"/></g>')
    # scan line over everything in the reactor
    o.append(f'<g clip-path="url(#reactor)"><g>'
             f'<rect x="{CX-R}" y="{CY-R-40}" width="{2*R}" height="40" fill="url(#scan)"/>'
             f'<rect x="{CX-R}" y="{CY-R}" width="{2*R}" height="1.6" fill="{P["phos"]}" opacity=".8"/>'
             f'<animateTransform attributeName="transform" type="translate" values="0 0;0 {2*R+40};0 {2*R+40}" keyTimes="0;.72;1" dur="4.4s" repeatCount="indefinite"/>'
             f'</g></g>')
    # targeting brackets
    b = 26
    bx0, by0, bx1, by1 = CX - R - 6, CY - R - 6, CX + R + 6, CY + R + 6
    br = (f"M{bx0} {by0+b}V{by0}H{bx0+b}M{bx1-b} {by0}H{bx1}V{by0+b}"
          f"M{bx1} {by1-b}V{by1}H{bx1-b}M{bx0+b} {by1}H{bx0}V{by1-b}")
    o.append(f'<path d="{br}" fill="none" stroke="{P["amber"]}" stroke-width="2" class="bracket"/>')
    o.append(text(CX - R - 4, CY - R - 12, "TARGET: UNIT 00", 10, P["amber"], ls=1))
    o.append(text(CX + R + 4, CY + R + 22, "HOUSING: STEEL / RUST GRADE C", 10, P["mute"], "end", ls=1))
    return "".join(o)


def diagnostics():
    o = [plate(32, 88, 290, 330, 12), rivets_box(32, 88, 290, 330)]
    o.append(text(52, 118, "DIAGNOSTICS", 13, P["hull_hi"], weight=700, ls=2))
    o.append(f'<path d="M52 128H302" stroke="{P["seam"]}"/>')
    rows = [
        ("FEE INTAKE", "ACTIVE", P["phos"], "b1"),
        ("TREASURY", "ONLINE", P["phos"], "b2"),
        ("PEPE ROUTER", "READY", P["phos"], "b3"),
        ("ASSET ROUTER", "READY", P["phos"], "b4"),
        ("DISTRIBUTOR", None, P["amber"], "b5"),
        ("ESP32 LINK", "CONNECTED", P["sol"], "b6"),
        ("KILL SWITCH", "SAFE", P["phos"], "b7"),
    ]
    y = 156
    for label, val, col, cls in rows:
        o.append(led(56, y - 4, col, cls, 3.5))
        o.append(text(72, y, label, 13, P["text"], ls=0.5))
        o.append(f'<path d="M{80+len(label)*8} {y-3}H{300-78}" stroke="{P["seam"]}" stroke-dasharray="1 4"/>')
        if val:
            o.append(text(302, y, val, 13, col, "end", 700))
        else:
            o.append(f'<g class="swapA">{text(302, y, "ARMED", 13, P["amber"], "end", 700)}</g>')
            o.append(f'<g class="swapB">{text(302, y, "STANDBY", 13, P["mute"], "end", 700)}</g>')
        y += 34
    o.append(text(52, 404, "readouts simulated / not live", 10, P["amber"], ls=0.6))

    # event bus tape
    o.append(plate(32, 432, 290, 196, 12))
    o.append(text(52, 458, "EVENT BUS", 13, P["hull_hi"], weight=700, ls=2))
    o.append(status_tag(302, 457, "SIM", P["amber"], "end"))
    ev = [("fee.accrued", "pool fees"), ("treasury.sync", "ok"), ("router.plan", "pepe 80 / asset 20"),
          ("swap.quote", "SOL>PEPE ok"), ("swap.dryrun", "not broadcast"), ("bot.emote", "FEED"),
          ("dist.snapshot", "holders indexed"), ("dist.exclude", "lp burn treasury"), ("dist.plan", "batched"),
          ("bot.emote", "PAYOUT"), ("esp32.ack", "seq ok"), ("loop.sleep", "cooldown")]
    lines = []
    for rep in range(2):
        for i, (k, v) in enumerate(ev):
            yy = 486 + (rep * len(ev) + i) * 20
            colr = P["eye"] if k.startswith("bot") else P["phos"]
            lines.append(text(50, yy, ">", 11, P["phos_dim"]) + text(64, yy, k, 11, colr) + text(302, yy, v, 11, P["mute"], "end"))
    o.append(f'<g clip-path="url(#tape)"><g class="tape">{"".join(lines)}</g></g>')
    o.append(f'<rect x="44" y="470" width="266" height="18" fill="{P["deck"]}" opacity=".75"/>')
    return "".join(o)


def right_panels():
    o = [plate(878, 88, 290, 244, 12), rivets_box(878, 88, 290, 244)]
    o.append(text(898, 118, "FEE PRESSURE", 13, P["hull_hi"], weight=700, ls=2))
    o.append(status_tag(1148, 117, "SIM", P["amber"], "end"))
    gx, gy, gr = 1023, 284, 104
    # colour bands
    def arc(a0, a1, r):
        x0, y0 = gx + r * math.cos(math.radians(a0)), gy + r * math.sin(math.radians(a0))
        x1, y1 = gx + r * math.cos(math.radians(a1)), gy + r * math.sin(math.radians(a1))
        return f"M{x0:.1f} {y0:.1f}A{r} {r} 0 0 1 {x1:.1f} {y1:.1f}"
    o.append(f'<path d="{arc(-180,-60,gr)}" stroke="{P["phos_dim"]}" stroke-width="8" fill="none"/>')
    o.append(f'<path d="{arc(-60,-25,gr)}" stroke="{P["amber"]}" stroke-width="8" fill="none" opacity=".8"/>')
    o.append(f'<path d="{arc(-25,0,gr)}" stroke="{P["eye"]}" stroke-width="8" fill="none" opacity=".85"/>')
    tk = []
    for i in range(0, 41):
        a = math.radians(-180 + i * 4.5)
        r0 = gr - (18 if i % 5 == 0 else 11)
        tk.append(f"M{gx+r0*math.cos(a):.1f} {gy+r0*math.sin(a):.1f}L{gx+(gr-5)*math.cos(a):.1f} {gy+(gr-5)*math.sin(a):.1f}")
    o.append(f'<path d="{"".join(tk)}" stroke="{P["text"]}" stroke-width="1.2" opacity=".6"/>')
    o.append(f'<g><path d="M{gx-3} {gy}L{gx} {gy-gr+14}L{gx+3} {gy}Z" fill="{P["eye"]}"/>'
             f'<animateTransform attributeName="transform" type="rotate" values="-62 {gx} {gy};-24 {gx} {gy};-40 {gx} {gy};8 {gx} {gy};-6 {gx} {gy};46 {gx} {gy};20 {gx} {gy};-62 {gx} {gy}" '
             f'keyTimes="0;.14;.26;.44;.55;.7;.82;1" dur="9s" repeatCount="indefinite"/></g>')
    o.append(f'<circle cx="{gx}" cy="{gy}" r="10" fill="{P["hull_lo"]}" stroke="{P["hull"]}" stroke-width="2"/>')
    o.append(text(898, 318, "LOW", 10, P["mute"]) + text(1148, 318, "SWEEP", 10, P["eye"], "end"))

    # cycle timer odometer
    o.append(plate(878, 340, 290, 78, 10, P["deck2"]))
    reels = []
    rw, rh = 36, 52
    digits = [("0", None), ("0", None), (":", None), ("5", 60), ("9", 10)]
    x = 950
    o.append(text(898, 368, "NEXT", 10, P["mute"], ls=1) + text(898, 382, "CYCLE", 10, P["mute"], ls=1) + text(898, 396, "(SIM)", 10, P["amber"], ls=1))
    for ch, period in digits:
        if ch == ":":
            reels.append(text(x + 8, 393, ":", 34, P["phos"], "middle", 700, extra='class="blink1"'))
            x += 18
            continue
        reels.append(f'<rect x="{x}" y="354" width="{rw}" height="{rh}" fill="#000" stroke="{P["seam"]}"/>')
        if period is None:
            reels.append(text(x + rw / 2, 393, ch, 34, P["phos"], "middle", 700))
        else:
            seq = list(range(int(ch), -1, -1)) + [int(ch)]
            col = "".join(text(x + rw / 2, 393 + i * rh, str(d), 34, P["phos"], "middle", 700) for i, d in enumerate(seq))
            reels.append(f'<g class="reel{period}">{col}</g>')
        reels.append(f'<rect x="{x}" y="354" width="{rw}" height="10" fill="#000" opacity=".6"/><rect x="{x}" y="396" width="{rw}" height="10" fill="#000" opacity=".6"/>')
        x += rw + 6
    o.append(f'<g clip-path="url(#reels)">{"".join(reels)}</g>')

    # fee flow chart
    o.append(plate(878, 432, 290, 196, 12))
    o.append(text(898, 458, "FEE FLOW", 13, P["hull_hi"], weight=700, ls=2))
    o.append(status_tag(1148, 457, "SIM", P["amber"], "end"))
    rnd = random.Random(11)
    bars = []
    n, bw = 44, 6
    hs = [int(18 + 70 * abs(math.sin(i * 0.42) * 0.6 + rnd.random() * 0.4)) for i in range(n)]
    for rep in range(2):
        for i, hgt in enumerate(hs):
            bx = 892 + (rep * n + i) * bw
            bars.append(f'<rect x="{bx}" y="{582-hgt}" width="{bw-2}" height="{hgt}" fill="{P["phos_dim"]}"/>'
                        f'<rect x="{bx}" y="{582-hgt}" width="{bw-2}" height="2" fill="{P["phos"]}"/>')
    o.append(f'<g clip-path="url(#chart)"><g class="chart">{"".join(bars)}</g></g>')
    o.append(f'<path d="M892 512H1154" stroke="{P["amber"]}" stroke-dasharray="4 4" opacity=".8"/>')
    o.append(text(1154, 507, "batch threshold", 9, P["amber"], "end"))
    # split bar
    o.append(text(898, 604, "SPLIT", 10, P["mute"], ls=1))
    o.append(f'<rect x="946" y="595" width="164" height="10" fill="{P["hull"]}"/><rect x="1110" y="595" width="44" height="10" fill="{P["sol"]}" opacity=".85"/>')
    o.append(text(946, 620, "PEPE 80", 10, P["hull_hi"]) + text(1154, 620, "ASSETS 20  example", 10, P["sol"], "end"))
    return "".join(o)


def conduit():
    o = []
    y = 668
    o.append(pipe(f"M36 {y}H560", 14, "pin"))
    o.append(pipe(f"M640 {y}H1164", 14, "pout"))
    o.append(pipe(f"M590 646V{CY+R-2}", 8, "pup", P["hull_lo"]))
    o.append(pipe(f"M610 {CY+R-2}V646", 8, "pdn", P["hull_lo"]))
    # packets under the junction box
    pk = []
    for i in range(6):
        pk.append(f'<g><path d="M-6 0L0 -6L6 0L0 6Z" fill="{P["amber"]}"/>{packet_motion("pin", 4.8, -i*0.8)}</g>')
    for i in range(3):
        pk.append(f'<g><rect x="-3" y="-3" width="6" height="6" fill="{P["amber"]}"/>{packet_motion("pup", 1.2, -i*0.4)}</g>')
        pk.append(f'<g><circle r="3.2" fill="{P["phos"]}"/>{packet_motion("pdn", 1.2, -i*0.4)}</g>')
    for i in range(7):
        is_asset = i % 3 == 2
        shape = (f'<rect x="-5" y="-5" width="10" height="10" fill="{P["sol"]}" transform="rotate(45)"/>' if is_asset else
                 f'<circle r="6" fill="{P["hull_hi"]}" stroke="{P["phos"]}" stroke-width="1.5"/><text y="3.5" font-size="8" font-weight="700" text-anchor="middle" fill="#0b1206">P</text>')
        pk.append(f'<g>{shape}{packet_motion("pout", 4.8, -i*0.69)}</g>')
    o.append("".join(pk))
    o.append(plate(556, 646, 88, 44, 8, P["deck2"], P["hull"]))
    o.append(text(600, 673, "CORE", 12, P["phos"], "middle", 700, ls=3, extra='class="blink2"'))
    o.append(text(36, 652, "TRADING FEES IN", 11, P["amber"], weight=700, ls=1.5))
    o.append(text(1164, 652, "PEPE + ASSETS OUT  >  HOLDERS", 11, P["phos"], "end", 700, ls=1.5))
    return "".join(o)


def ticker():
    msg = "HOLD PEPEBOT  ///  RECEIVE PEPE  ///  FEES IN  ///  ASSETS OUT  ///  HOLDERS  ///  REPEAT  ///  "
    msg = msg.replace(" ", "\u00a0")
    L = 1040
    o = [f'<rect x="24" y="698" width="1152" height="30" fill="#000"/>',
         f'<rect x="24" y="698" width="52" height="30" fill="url(#hz)"/>',
         f'<rect x="1124" y="698" width="52" height="30" fill="url(#hz)"/>']
    t = "".join(text(76 + k * L, 718, msg, 13, P["phos"], weight=700, extra=f'textLength="{L}" lengthAdjust="spacing"') for k in range(2))
    o.append(f'<g clip-path="url(#ticker)"><g class="tick">{t}</g></g>')
    return "".join(o)


def build():
    css = f"""
.blink1{{animation:bl 1.1s steps(2,jump-none) infinite}}
.blink2{{animation:bl 2.2s ease-in-out infinite}}
@keyframes bl{{0%,49%{{opacity:1}}50%,100%{{opacity:.25}}}}
.b1{{animation:bl .9s infinite}}.b2{{animation:bl 2.7s infinite}}.b3{{animation:bl 1.7s infinite}}
.b4{{animation:bl 2.1s infinite}}.b5{{animation:bl .5s infinite}}.b6{{animation:bl 1.3s infinite}}.b7{{animation:bl 3.9s infinite}}
.flick{{animation:fl 7s infinite}}
@keyframes fl{{0%,91%,95%,100%{{opacity:1}}92%{{opacity:.3}}93%{{opacity:.9}}94%{{opacity:.45}}}}
.eyepulse{{animation:ep 2.4s ease-in-out infinite}}
@keyframes ep{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
.blip{{opacity:0;animation:blip 5s linear infinite}}
@keyframes blip{{0%,6%{{opacity:1}}40%,100%{{opacity:0}}}}
.bracket{{animation:bl 2.6s infinite}}
.swapA{{animation:sa 6s steps(1) infinite}}.swapB{{animation:sb 6s steps(1) infinite}}
@keyframes sa{{0%{{opacity:1}}50%{{opacity:0}}}}@keyframes sb{{0%{{opacity:0}}50%{{opacity:1}}}}
.tape{{animation:tape 24s linear infinite}}@keyframes tape{{to{{transform:translateY(-240px)}}}}
.chart{{animation:chart 14s linear infinite}}@keyframes chart{{to{{transform:translateX(-264px)}}}}
.tick{{animation:tick 26s linear infinite}}@keyframes tick{{to{{transform:translateX(-1040px)}}}}
.reel10{{animation:r10 10s infinite}}.reel60{{animation:r60 60s infinite}}
"""
    # reel keyframes: hold each digit, roll quickly to next
    for period, count in ((10, 10), (60, 6)):
        frames = []
        for i in range(count + 1):
            p = i / count * 100
            hold = min(p + (100 / count) * 0.85, 100)
            frames.append(f"{p:.3f}%{{transform:translateY({-i*52}px)}}")
            if i < count:
                frames.append(f"{hold:.3f}%{{transform:translateY({-i*52}px)}}")
        css += f"@keyframes r{period}{{{''.join(frames)}}}"
    defs = (grime_defs("g", 5) + glow_defs() + hazard_pattern("hz") + grid_pattern("grid", 24) +
            dots_pattern("unlit", 3.4, 2.4, P["phos_dim"], .28))
    body = (f'<rect width="{W}" height="{H}" fill="{P["void"]}"/>'
            f'<rect width="{W}" height="{H}" fill="url(#grid)"/>'
            f'<path d="{chamfer(8,8,W-16,H-16,22)}" fill="none" stroke="{P["hull_lo"]}" stroke-width="2"/>'
            + top_bar() + reactor() + diagnostics() + right_panels() + conduit() + ticker()
            + grime(W, H, "g", 0.12))
    return svg(W, H, body, css, defs, "PepeBot control unit online (simulated readouts)")
