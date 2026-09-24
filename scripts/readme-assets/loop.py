"""assets/readme/loop-machine.svg — the whole fee -> asset -> holder circuit as one machine."""
import math
import random
from lib import (P, EYES, EYE_R, logo_uri, matrix, svg, grime_defs, grime, plate, rivets_box,
                 hazard_pattern, grid_pattern, gear, spin, led, text, packet_motion, pipe,
                 status_tag, chamfer)

W, H = 1200, 1000
TAGC = {"EXTERNAL": P["mute"], "ADAPTER": P["amber"], "CONFIG": P["amber"], "BUILT / SIM": P["phos"],
        "DRY-RUN": P["phos"], "QUOTE ONLY": P["amber"], "PLANNED": P["mute"], "PLAN BUILT": P["phos"]}


def machine(x, y, w, h, num, name, tag, lit=P["phos"]):
    o = [plate(x, y, w, h, 12, P["deck"], P["hull_lo"], 2), rivets_box(x, y + 30, w, h - 30, 7, 2.2)]
    o.append(f'<path d="M{x+12} {y}H{x+w-12}L{x+w} {y+12}V{y+28}H{x}V{y+12}Z" fill="{P["deck2"]}"/>')
    o.append(f'<path d="M{x} {y+28}H{x+w}" stroke="{P["hull_lo"]}" stroke-width="1.5"/>')
    o.append(text(x + 14, y + 19, num, 12, P["amber"], weight=700, ls=1))
    o.append(text(x + 40, y + 19, name, 12, P["hull_hi"], weight=700, ls=2))
    o.append(led(x + w - 16, y + 14, lit, "bl1", 3))
    o.append(status_tag(x + w - 10, y + h - 10, tag, TAGC[tag], "end"))
    return "".join(o)


def trade_floor():
    x, y, w, h = 80, 100, 233, 200
    o = [machine(x, y, w, h, "01", "TRADE FLOOR", "EXTERNAL")]
    rnd = random.Random(3)
    cx = x + 22
    for i in range(12):
        up = rnd.random() > 0.42
        col = P["phos"] if up else P["eye"]
        bh = rnd.randint(14, 44)
        by = y + 60 + rnd.randint(0, 50)
        o.append(f'<path d="M{cx+4} {by-10}V{by+bh+10}" stroke="{col}" stroke-width="1" opacity=".7"/>')
        o.append(f'<rect x="{cx}" y="{by}" width="8" height="{bh}" fill="{col}" opacity=".9" class="cndl" style="animation-delay:{-i*0.37:.2f}s"/>')
        cx += 16
    o.append(f'<g class="swapA">{text(x+16, y+176, "BUY", 11, P["phos"], weight=700)}</g>')
    o.append(f'<g class="swapB">{text(x+16, y+176, "SELL", 11, P["eye"], weight=700)}</g>')
    o.append(text(x + 58, y + 176, "swaps pay pool fees", 10, P["mute"]))
    return "".join(o)


def fee_intake():
    x, y, w, h = 358, 100, 233, 200
    o = [machine(x, y, w, h, "02", "FEE INTAKE", "ADAPTER")]
    fx = x + w / 2
    o.append(f'<path d="M{fx-70} {y+50}H{fx+70}L{fx+18} {y+112}V{y+130}H{fx-18}V{y+112}Z" fill="{P["hull_lo"]}" stroke="{P["hull"]}" stroke-width="2"/>')
    o.append(f'<path d="M{fx-62} {y+56}H{fx+62}" stroke="{P["hull_hi"]}" stroke-width="1" opacity=".6"/>')
    for i in range(7):
        ox = fx - 48 + i * 16
        o.append(f'<g class="drop" style="animation-delay:{-i*0.41:.2f}s"><path d="M{ox} {y+34}l5 5l-5 5l-5 -5z" fill="{P["amber"]}"/></g>')
    o.append(f'<rect x="{fx-8}" y="{y+112}" width="16" height="20" fill="{P["amber"]}" opacity=".5" class="bl2"/>')
    o.append(text(x + 16, y + 158, "claim venue fees", 10, P["text"]))
    o.append(text(x + 16, y + 173, "adapter per launch venue", 10, P["mute"]))
    return "".join(o)


def treasury():
    x, y, w, h = 636, 100, 233, 200
    o = [machine(x, y, w, h, "03", "TREASURY", "CONFIG")]
    vx, vy, vr = x + 88, y + 98, 52
    o.append(f'<circle cx="{vx}" cy="{vy}" r="{vr+8}" fill="{P["deck2"]}" stroke="{P["hull_lo"]}" stroke-width="3"/>')
    for i in range(12):
        a = 2 * math.pi * i / 12
        o.append(f'<circle cx="{vx+(vr+2)*math.cos(a):.1f}" cy="{vy+(vr+2)*math.sin(a):.1f}" r="2.4" fill="{P["hull"]}"/>')
    o.append(f'<circle cx="{vx}" cy="{vy}" r="{vr-6}" fill="{P["hull_lo"]}" stroke="{P["rust"]}" stroke-width="2" stroke-dasharray="3 5"/>')
    spokes = "".join(f"M{vx} {vy}L{vx+34*math.cos(a):.1f} {vy+34*math.sin(a):.1f}" for a in [k * math.pi / 3 for k in range(6)])
    o.append(f'<g><path d="{spokes}" stroke="{P["hull_hi"]}" stroke-width="4" stroke-linecap="round"/>'
             f'<circle cx="{vx}" cy="{vy}" r="34" fill="none" stroke="{P["hull_hi"]}" stroke-width="3"/>'
             f'<circle cx="{vx}" cy="{vy}" r="8" fill="{P["hull"]}"/>'
             f'<animateTransform attributeName="transform" type="rotate" values="0 {vx} {vy};140 {vx} {vy};140 {vx} {vy};0 {vx} {vy};0 {vx} {vy}" '
             f'keyTimes="0;.25;.5;.75;1" dur="6s" repeatCount="indefinite"/></g>')
    # fill gauge
    gx, gy, gh = x + 180, y + 44, 110
    o.append(f'<rect x="{gx}" y="{gy}" width="20" height="{gh}" fill="#000" stroke="{P["hull_lo"]}"/>')
    o.append(f'<rect x="{gx+3}" y="{gy+3}" width="14" height="{gh-6}" fill="{P["phos"]}" opacity=".85" class="fill"/>')
    for k in range(1, 5):
        o.append(f'<path d="M{gx} {gy+k*gh/5:.0f}h6" stroke="{P["text"]}" opacity=".5"/>')
    o.append(text(x + 16, y + 176, "multisig wallet", 10, P["text"]))
    return "".join(o)


def core():
    x, y, w, h = 910, 90, 260, 330
    o = [machine(x, y, w, h, "04", "PEPEBOT CORE", "BUILT / SIM", P["eye"])]
    S = 206
    lx, ly = x + (w - S) / 2, y + 40
    eyes = []
    for fx, fy in EYES:
        ex, ey = lx + fx * S, ly + fy * S
        eyes.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="{EYE_R*S*1.7:.1f}" fill="url(#eyeglow)" class="eyeflash" style="mix-blend-mode:screen"/>')
    o.append(f'<image href="{logo_uri(240)}" x="{lx}" y="{ly}" width="{S}" height="{S}"/>{"".join(eyes)}')
    o.append(f'<path d="M{x+14} {y+256}H{x+w-14}" stroke="{P["seam"]}"/>')
    o.append(text(x + 16, y + 276, "orchestrator + emote engine", 10, P["text"]))
    o.append(text(x + 16, y + 294, "state", 10, P["mute"]))
    for k, st in enumerate(["IDLE", "FEED", "ROUTE", "PAYOUT"]):
        o.append(f'<g class="st{k}">{text(x + 60, y + 294, st, 10, P["eye"], weight=700)}</g>')
    return "".join(o)


def router():
    x, y, w, h = 900, 480, 270, 220
    o = [machine(x, y, w, h, "05", "ALLOCATION ROUTER", "DRY-RUN")]
    ax, ay, ar, at = x + 78, y + 92, 44, 14
    bx, by, br, bt = ax + 73, ay, 33, 11
    o.append(f'<g><path d="{gear(ax, ay, ar, at, 8, 10)}" fill="{P["hull_lo"]}" stroke="{P["hull"]}" stroke-width="1.5" fill-rule="evenodd"/>'
             f'<circle cx="{ax}" cy="{ay}" r="22" fill="none" stroke="{P["rust"]}" stroke-dasharray="2 4"/>{spin(ax, ay, 7)}</g>')
    o.append(f'<g transform="rotate(12 {bx} {by})"><g><path d="{gear(bx, by, br, bt, 7, 7)}" fill="{P["rust"]}" stroke="{P["rust_hi"]}" stroke-width="1.5" fill-rule="evenodd"/>'
             f'{spin(bx, by, 7*bt/at, True)}</g></g>')
    o.append(f'<circle cx="{ax}" cy="{ay}" r="5" fill="{P["amber"]}"/><circle cx="{bx}" cy="{by}" r="4" fill="{P["amber"]}"/>')
    o.append(text(x + 200, y + 70, "IN", 10, P["mute"]) + text(x + 200, y + 86, "fee stream", 9, P["text"]))
    # allocation bars
    o.append(text(x + 16, y + 164, "PEPE", 10, P["hull_hi"], weight=700))
    o.append(f'<rect x="{x+64}" y="{y+155}" width="150" height="10" fill="#000"/><rect x="{x+64}" y="{y+155}" width="120" height="10" fill="{P["hull"]}" class="alloc"/>')
    o.append(text(x + 254, y + 164, "80", 10, P["hull_hi"], "end"))
    o.append(text(x + 16, y + 182, "ASSET", 10, P["sol"], weight=700))
    o.append(f'<rect x="{x+64}" y="{y+173}" width="150" height="10" fill="#000"/><rect x="{x+64}" y="{y+173}" width="30" height="10" fill="{P["sol"]}" opacity=".85"/>')
    o.append(text(x + 254, y + 182, "20", 10, P["sol"], "end"))
    o.append(text(x + 16, y + 206, "example split", 9, P["mute"]))
    return "".join(o)


def swap_unit():
    x, y, w, h = 580, 500, 220, 80
    o = [plate(x, y, w, h, 10, P["deck"], P["hull"], 2)]
    tx, ty = x + 38, y + 40
    blades = "".join(
        f'<path d="M{tx} {ty}Q{tx+20*math.cos(a+0.6):.1f} {ty+20*math.sin(a+0.6):.1f} {tx+26*math.cos(a):.1f} {ty+26*math.sin(a):.1f}" stroke="{P["hull_hi"]}" stroke-width="5" fill="none" stroke-linecap="round"/>'
        for a in [k * 2 * math.pi / 6 for k in range(6)])
    o.append(f'<circle cx="{tx}" cy="{ty}" r="30" fill="#000" stroke="{P["hull_lo"]}" stroke-width="3"/><g>{blades}{spin(tx, ty, 0.8)}</g><circle cx="{tx}" cy="{ty}" r="6" fill="{P["rust_hi"]}"/>')
    o.append(text(x + 80, y + 26, "06  PEPE SWAP", 11, P["hull_hi"], weight=700, ls=1.5))
    o.append(text(x + 80, y + 44, "SOL > PEPE", 11, P["phos"]))
    o.append(text(x + 80, y + 60, "aggregator route", 9, P["mute"]))
    o.append(status_tag(x + w - 8, y + 74, "QUOTE ONLY", TAGC["QUOTE ONLY"], "end"))
    return "".join(o)


def asset_bay():
    x, y, w, h = 580, 600, 220, 120
    o = [plate(x, y, w, h, 10, P["deck"], P["sol"], 1.5)]
    o.append(text(x + 14, y + 22, "07  ASSET MODULE BAY", 11, P["sol"], weight=700, ls=1.5))
    slots = [("SOL", P["phos"], "ok"), ("wBTC", P["phos"], "ok"), ("EQTY", P["eye"], "gate"), ("----", P["mute"], "empty")]
    for i, (lab, col, st) in enumerate(slots):
        sx = x + 12 + i * 51
        o.append(f'<rect x="{sx}" y="{y+34}" width="45" height="42" fill="#000" stroke="{col}" stroke-width="1"/>')
        o.append(text(sx + 22.5, y + 60, lab, 10, col, "middle", 700))
        cls = "bl3" if st == "gate" else ("bl1" if st == "ok" else "")
        o.append(f'<rect x="{sx+4}" y="{y+38}" width="37" height="3" fill="{col}" class="{cls}"/>')
    o.append(text(x + 12, y + 94, "EQTY: provider + eligibility gated", 9, P["eye"]))
    o.append(status_tag(x + w - 8, y + 114, "PLANNED", TAGC["PLANNED"], "end"))
    return "".join(o)


def distributor():
    x, y, w, h = 80, 480, 320, 240
    o = [machine(x, y, w, h, "08", "DISTRIBUTOR", "PLAN BUILT")]
    rx, ry, rr = x + 82, y + 118, 60
    o.append(f'<circle cx="{rx}" cy="{ry}" r="{rr}" fill="#000" stroke="{P["hull_lo"]}" stroke-width="3"/>')
    for k in (20, 40):
        o.append(f'<circle cx="{rx}" cy="{ry}" r="{k}" fill="none" stroke="{P["seam"]}"/>')
    o.append(f'<path d="M{rx-rr} {ry}H{rx+rr}M{rx} {ry-rr}V{ry+rr}" stroke="{P["seam"]}"/>')
    o.append(f'<g><path d="M{rx} {ry}L{rx} {ry-rr+3}A{rr-3} {rr-3} 0 0 0 {rx-(rr-3)*math.sin(0.6):.1f} {ry-(rr-3)*math.cos(0.6):.1f}Z" fill="{P["phos"]}" opacity=".25"/>'
             f'<path d="M{rx} {ry}V{ry-rr+3}" stroke="{P["phos"]}" stroke-width="1.5"/>{spin(rx, ry, 3)}</g>')
    rnd = random.Random(9)
    for i in range(14):
        a, d = rnd.random() * 6.28, rnd.uniform(10, rr - 8)
        o.append(f'<circle cx="{rx+d*math.cos(a):.1f}" cy="{ry+d*math.sin(a):.1f}" r="1.8" fill="{P["phos"]}" class="blip" style="animation-delay:{-rnd.random()*3:.2f}s"/>')
    steps = ["SNAPSHOT", "EXCLUDE", "PRO-RATA", "BATCH", "SEND"]
    for i, s in enumerate(steps):
        sy = y + 62 + i * 25
        o.append(led(x + 172, sy - 4, P["sol"] if s != "SEND" else P["amber"], f"seq{i}", 3))
        o.append(text(x + 184, sy, s, 11, P["text"] if s != "SEND" else P["amber"], weight=700, ls=1))
    o.append(text(x + 184, y + 190, "send: planned", 9, P["amber"]))
    return "".join(o)


def holders():
    x, y, w, h = 80, 800, 1090, 180
    o = [plate(x, y, w, h, 12, P["deck"], P["hull_lo"], 2)]
    o.append(text(x + 16, y + 22, "09  HOLDERS", 12, P["hull_hi"], weight=700, ls=2))
    o.append(text(x + 150, y + 22, "PEPEBOT balance snapshot  /  demo payout sweep", 10, P["mute"]))
    o.append(status_tag(x + w - 10, y + 22, "SIM", P["amber"], "end"))
    excluded = {(0, 3): "LP", (2, 17): "BURN", (4, 29): "TRSY", (1, 36): "LP"}
    cells = []
    for r in range(5):
        for c in range(40):
            cx, cy = x + 20 + c * 26.5, y + 38 + r * 26
            if (r, c) in excluded:
                cells.append(f'<rect x="{cx}" y="{cy}" width="20" height="18" fill="url(#hatch)" stroke="{P["eye"]}" stroke-width="1"/>')
                continue
            dl = c * 0.07 + r * 0.05
            cells.append(f'<path d="M{cx} {cy}h20v18h-20z M{cx+13} {cy+6}h7v6h-7z" fill="{P["hull_lo"]}" fill-rule="evenodd" class="cell" style="animation-delay:{dl:.2f}s"/>')
    o.append("".join(cells))
    o.append(f'<rect x="{x+w-436}" y="{y+13}" width="12" height="10" fill="url(#hatch)" stroke="{P["eye"]}"/>')
    o.append(text(x + w - 418, y + 22, "excluded: LP / burn / treasury / programs", 10, P["eye"]))
    return "".join(o)


def flows():
    o = []
    # pipes first (machines are drawn over them, so packets disappear into machines)
    o.append(pipe("M60 230H910", 14, "main"))
    o.append(pipe("M1040 420V480", 12, "c2r"))
    o.append(pipe("M900 540H400", 12, "pepe", P["hull_lo"], P["hull_hi"]))
    o.append(pipe("M900 650H400", 12, "asset", "#0d3b2c", P["sol"]))
    o.append(pipe("M240 720V772H1150", 12, "bus"))
    o.append(pipe("M80 910H40V230H80", 12, "ret", "#26301f", P["mute"]))
    for k in range(10):
        dx = 284 + k * 96
        o.append(f'<path d="M{dx} 778V800" stroke="{P["hull_lo"]}" stroke-width="4"/>')
    pk = []
    for i in range(18):
        pk.append(f'<g><path d="M-6 0L0 -6L6 0L0 6Z" fill="{P["amber"]}"/>{packet_motion("main", 7, -i*7/18)}</g>')
    for i in range(2):
        pk.append(f'<g><circle r="4" fill="{P["amber"]}"/>{packet_motion("c2r", 1.2, -i*0.6)}</g>')
    for i in range(6):
        pk.append(f'<g><circle r="6" fill="{P["hull_hi"]}" stroke="{P["phos"]}" stroke-width="1.5"/><text y="3.5" font-size="8" font-weight="700" text-anchor="middle" fill="#0b1206">P</text>{packet_motion("pepe", 4.2, -i*0.7)}</g>')
    for i in range(3):
        pk.append(f'<g><rect x="-5" y="-5" width="10" height="10" fill="{P["sol"]}" transform="rotate(45)"/>{packet_motion("asset", 4.2, -i*1.4)}</g>')
    for i in range(12):
        is_a = i % 4 == 3
        shp = (f'<rect x="-4" y="-4" width="8" height="8" fill="{P["sol"]}" transform="rotate(45)"/>' if is_a
               else f'<circle r="4.5" fill="{P["hull_hi"]}" stroke="{P["phos"]}"/>')
        pk.append(f'<g>{shp}{packet_motion("bus", 6, -i*0.5)}</g>')
    for i in range(8):
        pk.append(f'<g><rect x="-3" y="-3" width="6" height="6" fill="{P["mute"]}"/>{packet_motion("ret", 8, -i*1.0)}</g>')
    o.append("".join(pk))
    return "".join(o)


def repeat_badge():
    d, wdt = matrix("REPEAT", 0, 0, 3)
    return (f'<rect x="22" y="470" width="36" height="{wdt+24:.0f}" fill="#000" stroke="{P["mute"]}"/>'
            f'<g transform="translate(51 {482}) rotate(90)"><path d="{d}" fill="{P["phos"]}" filter="url(#glow)" class="bl2"/></g>')


def title():
    return (text(40, 46, "SCHEMATIC PB-LOOP-01", 13, P["hull_hi"], weight=700, ls=2)
            + text(292, 46, "trading fees  >  treasury  >  core  >  router  >  PEPE / assets  >  distributor  >  holders  >  repeat", 11, P["mute"])
            + status_tag(1160, 45, "FLOW RATES ILLUSTRATIVE", P["amber"], "end")
            + f'<path d="M40 62H1160" stroke="{P["seam"]}"/>')


def build():
    css = """
@keyframes bl{0%,49%{opacity:1}50%,100%{opacity:.25}}
.bl1{animation:bl 1.4s infinite}.bl2{animation:bl 2.2s infinite}.bl3{animation:bl .6s infinite}
.cndl{transform-box:fill-box;transform-origin:center;animation:cndl 2.6s ease-in-out infinite alternate}
@keyframes cndl{from{transform:scaleY(.45)}to{transform:scaleY(1.15)}}
.swapA{animation:sa 2.4s steps(1) infinite}.swapB{animation:sb 2.4s steps(1) infinite}
@keyframes sa{0%{opacity:1}50%{opacity:0}}@keyframes sb{0%{opacity:0}50%{opacity:1}}
.drop{animation:drop 2.9s linear infinite}
@keyframes drop{0%{transform:translateY(0);opacity:0}10%{opacity:1}70%{transform:translateY(64px);opacity:1}80%,100%{transform:translateY(70px);opacity:0}}
.fill{transform-box:fill-box;transform-origin:bottom;animation:fill 7s ease-in-out infinite}
@keyframes fill{0%{transform:scaleY(.15)}70%{transform:scaleY(.95)}78%{transform:scaleY(.95)}90%,100%{transform:scaleY(.15)}}
.eyeflash{animation:ef 3.5s infinite}
@keyframes ef{0%,100%{opacity:.25}8%{opacity:1}14%{opacity:.35}20%{opacity:1}40%{opacity:.4}}
.st0,.st1,.st2,.st3{opacity:0;animation:st 8s steps(1) infinite}
.st1{animation-delay:2s}.st2{animation-delay:4s}.st3{animation-delay:6s}
@keyframes st{0%{opacity:1}25%{opacity:0}}
@media (prefers-reduced-motion: reduce){.st1{opacity:1!important}.seq0{opacity:1!important}}
.alloc{animation:bl 3s infinite}
.blip{animation:blip 3s linear infinite}@keyframes blip{0%,5%{opacity:1}60%,100%{opacity:.1}}
.seq0,.seq1,.seq2,.seq3,.seq4{opacity:.15;animation:seq 5s steps(1) infinite}
.seq1{animation-delay:1s}.seq2{animation-delay:2s}.seq3{animation-delay:3s}.seq4{animation-delay:4s}
@keyframes seq{0%{opacity:1}20%{opacity:.15}}
.cell{animation:cell 4s ease-out infinite}
@keyframes cell{0%{fill:#b8ff4f}12%{fill:#6e8c3a}40%,100%{fill:#34471d}}
"""
    defs = (grime_defs("g", 12) + hazard_pattern("hz") + grid_pattern("grid", 20) +
            '<filter id="glow" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="1.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
            f'<radialGradient id="eyeglow"><stop offset="0" stop-color="{P["eye_hot"]}" stop-opacity=".95"/><stop offset=".35" stop-color="{P["eye"]}" stop-opacity=".75"/><stop offset="1" stop-color="{P["eye"]}" stop-opacity="0"/></radialGradient>'
            f'<pattern id="hatch" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="5" height="5" fill="#1a0805"/><rect width="2" height="5" fill="{P["eye"]}" opacity=".6"/></pattern>')
    body = (f'<rect width="{W}" height="{H}" fill="{P["void"]}"/><rect width="{W}" height="{H}" fill="url(#grid)"/>'
            f'<path d="{chamfer(8,8,W-16,H-16,22)}" fill="none" stroke="{P["hull_lo"]}" stroke-width="2"/>'
            + title() + flows() + trade_floor() + fee_intake() + treasury() + core() + router()
            + swap_unit() + asset_bay() + distributor() + holders() + repeat_badge()
            + grime(W, H, "g", 0.1))
    return svg(W, H, body, css, defs, "PepeBot loop: trading fees to treasury to router to PEPE and asset purchases to holder distribution")


TARGETS = {"loop-machine.svg": build}
