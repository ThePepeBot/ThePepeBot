"""Section header boards, the HOLD/RECEIVE board, the conduit divider and the shutdown footer."""
from lib import (P, EYES, EYE_R, logo_uri, matrix, matrix_width, svg, grime_defs, grime, plate, rivets_box,
                 hazard_pattern, text, chamfer, led, packet_motion, pipe, status_tag)

SECTIONS = [
    ("01", "WHAT IS THIS THING", "identification"),
    ("02", "THE LOOP", "fees in / assets out / repeat"),
    ("03", "ROUTER + ASSET BAY", "where the fee stream goes"),
    ("04", "PAYOUT SEQUENCE", "how holders get paid"),
    ("05", "THE BODY", "events you can see"),
    ("06", "SYSTEM MAP", "chain to servo"),
    ("07", "TERMINAL", "one simulated cycle"),
    ("08", "HARDWARE", "rev A reference build"),
    ("09", "BOOT IT", "build / run / flash"),
    ("10", "MANIFEST", "built vs planned"),
    ("11", "FAILSAFES", "security / limits / risk"),
]


def glow_filter(sd=1.8):
    return (f'<filter id="glow" x="-10%" y="-60%" width="120%" height="220%"><feGaussianBlur stdDeviation="{sd}" result="b"/>'
            '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')


def header(num, title, sub):
    W, H = 1200, 100
    pitch = 4.2
    d, tw = matrix(title, 0, 0, pitch)
    nd, nw = matrix(num, 0, 0, 5)
    bx = 150
    css = f"""
.sweep{{animation:sw 5s cubic-bezier(.6,0,.4,1) infinite}}@keyframes sw{{0%{{transform:translateX(-120px)}}55%,100%{{transform:translateX({tw+140:.0f}px)}}}}
.bl{{animation:bl 1.3s infinite}}@keyframes bl{{0%,49%{{opacity:1}}50%,100%{{opacity:.2}}}}
.fl{{animation:fl 9s infinite}}@keyframes fl{{0%,93%,97%,100%{{opacity:1}}94%{{opacity:.35}}95%{{opacity:.9}}96%{{opacity:.5}}}}
"""
    defs = (grime_defs("g", int(num) + 60) + hazard_pattern("hz", size=12) + glow_filter() +
            f'<pattern id="unlit" width="{pitch}" height="{pitch}" patternUnits="userSpaceOnUse" x="{bx+16}" y="34"><rect width="{pitch*0.72:.2f}" height="{pitch*0.72:.2f}" fill="{P["phos_dim"]}" opacity=".22"/></pattern>'
            f'<clipPath id="lit"><path d="{d}" transform="translate({bx+16} 34)"/></clipPath>'
            f'<linearGradient id="sg" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".95"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
    o = [f'<rect width="{W}" height="{H}" fill="{P["void"]}"/>',
         f'<path d="{chamfer(4,6,W-8,H-12,14)}" fill="{P["deck"]}" stroke="{P["hull_lo"]}" stroke-width="2"/>',
         f'<rect x="4" y="{H-14}" width="{W-8}" height="4" fill="url(#hz)" opacity=".55"/>',
         # number block
         f'<path d="{chamfer(16,16,112,62,8)}" fill="#000" stroke="{P["amber"]}" stroke-width="1.5"/>',
         text(28, 32, "SEC", 9, P["amber"], ls=2),
         f'<path d="{nd}" fill="{P["amber"]}" transform="translate({80 - nw/2:.1f} 38)" filter="url(#glow)"/>',
         # LED board
         f'<rect x="{bx}" y="22" width="{tw+32:.0f}" height="54" fill="#000" stroke="{P["seam"]}"/>',
         f'<rect x="{bx+10}" y="30" width="{tw+12:.0f}" height="38" fill="url(#unlit)"/>',
         f'<g class="fl"><path d="{d}" transform="translate({bx+16} 34)" fill="{P["phos"]}" filter="url(#glow)"/></g>',
         f'<g clip-path="url(#lit)"><rect x="{bx}" y="30" width="90" height="40" fill="url(#sg)" class="sweep"/></g>',
         rivets_box(bx, 22, tw + 32, 54, 4, 1.6),
         # right side
         text(W - 56, 46, sub, 12, P["text"], "end", ls=0.5),
         text(W - 56, 64, f"pepebot / sec {num}", 10, P["mute"], "end", ls=1),
         led(W - 34, 50, P["phos"], "bl", 5),
         grime(W, H, "g", 0.1)]
    return svg(W, H, "".join(o), css, defs, f"{num} {title}")


def hold_receive():
    W, H = 1200, 156
    pitch = 5.4
    d1, w1 = matrix("HOLD PEPEBOT.", 0, 0, pitch)
    d2, w2 = matrix("RECEIVE PEPE.", 0, 0, pitch)
    gap = W - 72 - w1 - w2
    x1 = 36
    x2 = W - 36 - w2
    ay = 40 + 3.5 * pitch
    css = """
.l1{animation:l1 6s infinite}.l2{animation:l2 6s infinite}
@keyframes l1{0%,4%{opacity:.08}6%,92%{opacity:1}96%,100%{opacity:.08}}
@keyframes l2{0%,34%{opacity:.08}36%,92%{opacity:1}96%,100%{opacity:.08}}
.ch{animation:ch 6s infinite}@keyframes ch{0%,8%{opacity:0}12%{opacity:1}30%{opacity:.2}34%,100%{opacity:0}}
"""
    chev = []
    cx0 = x1 + w1 + 22
    for k in range(5):
        cx = cx0 + k * (gap - 44) / 5
        chev.append(f'<path d="M{cx:.0f} {ay-16:.0f}l14 16l-14 16" fill="none" stroke="{P["amber"]}" stroke-width="5" class="ch" style="animation-delay:{k*0.25:.2f}s"/>')
    defs = (grime_defs("g", 77) + glow_filter(2.4) +
            f'<pattern id="unlit" width="{pitch}" height="{pitch}" patternUnits="userSpaceOnUse" x="{x1}" y="40"><rect width="{pitch*0.72:.2f}" height="{pitch*0.72:.2f}" fill="{P["phos_dim"]}" opacity=".2"/></pattern>'
            + hazard_pattern("hz", size=12))
    o = [f'<rect width="{W}" height="{H}" fill="{P["void"]}"/>',
         f'<path d="{chamfer(4,4,W-8,H-8,16)}" fill="#000" stroke="{P["hull_lo"]}" stroke-width="3"/>',
         f'<rect x="20" y="28" width="{W-40}" height="{7*pitch+26:.0f}" fill="url(#unlit)"/>',
         f'<g class="l1"><path d="{d1}" transform="translate({x1} 40)" fill="{P["phos"]}" filter="url(#glow)"/></g>',
         f'<g class="l2"><path d="{d2}" transform="translate({x2:.1f} 40)" fill="{P["eye"]}" filter="url(#glow)"/></g>',
         "".join(chev),
         f'<rect x="4" y="{H-58}" width="{W-8}" height="6" fill="url(#hz)" opacity=".6"/>',
         text(36, H - 26, "The core loop in two lines. Payouts only happen when real fees exist and the distributor runs. No yield, return or amount is promised.", 11.5, P["text"]),
         rivets_box(4, 4, W - 8, H - 8, 12, 3),
         grime(W, H, "g", 0.12)]
    return svg(W, H, "".join(o), css, defs, "HOLD PEPEBOT. RECEIVE PEPE.")


def divider():
    W, H = 1200, 34
    o = [f'<rect width="{W}" height="{H}" fill="{P["void"]}"/>', pipe("M0 17H1200", 10, "dv")]
    for x in range(60, W, 180):
        o.append(f'<rect x="{x}" y="7" width="14" height="20" fill="{P["hull_lo"]}" stroke="{P["hull"]}"/>')
    for i in range(8):
        col = P["amber"] if i % 3 else P["phos"]
        o.append(f'<g><rect x="-4" y="-4" width="8" height="8" fill="{col}" transform="rotate(45)"/>{packet_motion("dv", 9, -i*9/8)}</g>')
    return svg(W, H, "".join(o), "", "", "conduit")


def footer():
    W, H = 1200, 320
    S = 240
    lx, ly = 40, 40
    eyes = "".join(
        f'<circle cx="{lx+fx*S:.1f}" cy="{ly+fy*S:.1f}" r="{EYE_R*S*1.7:.1f}" fill="url(#eyeglow)" class="pd" style="mix-blend-mode:screen"/>'
        for fx, fy in EYES)
    d, w = matrix("UNIT 00 // IDLE", 0, 0, 4.6)
    css = """
.pd{animation:pd 8s ease-in-out infinite}@keyframes pd{0%,100%{opacity:.9}40%{opacity:.9}60%{opacity:0}75%{opacity:.05}80%{opacity:.7}82%{opacity:.1}90%{opacity:.9}}
.dim{animation:dim 8s ease-in-out infinite}@keyframes dim{0%,40%,90%,100%{opacity:0}60%,75%{opacity:.45}}
.cur{animation:cur 1s steps(1) infinite}@keyframes cur{50%{opacity:0}}
"""
    defs = (grime_defs("g", 88) + glow_filter(2) +
            f'<radialGradient id="eyeglow"><stop offset="0" stop-color="{P["eye_hot"]}" stop-opacity=".95"/><stop offset=".35" stop-color="{P["eye"]}" stop-opacity=".75"/><stop offset="1" stop-color="{P["eye"]}" stop-opacity="0"/></radialGradient>'
            f'<pattern id="unlit" width="4.6" height="4.6" patternUnits="userSpaceOnUse" x="330" y="70"><rect width="3.3" height="3.3" fill="{P["phos_dim"]}" opacity=".2"/></pattern>'
            + hazard_pattern("hz", size=14))
    o = [f'<rect width="{W}" height="{H}" fill="{P["void"]}"/>',
         f'<path d="{chamfer(4,4,W-8,H-8,18)}" fill="{P["deck"]}" stroke="{P["hull_lo"]}" stroke-width="2"/>',
         f'<image href="{logo_uri(240)}" x="{lx}" y="{ly}" width="{S}" height="{S}"/>', eyes,
         f'<rect x="{lx}" y="{ly}" width="{S}" height="{S}" fill="#000" class="dim"/>',
         f'<rect x="320" y="60" width="{w+22:.0f}" height="54" fill="#000" stroke="{P["seam"]}"/>',
         f'<rect x="326" y="66" width="{w+10:.0f}" height="42" fill="url(#unlit)"/>',
         f'<path d="{d}" transform="translate(330 70)" fill="{P["phos"]}" filter="url(#glow)"/>',
         text(322, 150, "fees in.  assets out.  holders.  repeat.", 16, P["text"], weight=700, ls=1),
         text(322, 180, "open source: firmware, backend, automation, hardware notes and every README asset.", 12, P["mute"]),
         text(322, 200, "regenerate the visuals:  python3 scripts/readme-assets/build.py", 12, P["mute"]),
         text(322, 244, "END OF TRANSMISSION", 13, P["amber"], weight=700, ls=3),
         f'<rect x="{322+19*10.9:.0f}" y="232" width="10" height="15" fill="{P["amber"]}" class="cur"/>',
         f'<rect x="4" y="{H-26}" width="{W-8}" height="8" fill="url(#hz)" opacity=".5"/>',
         rivets_box(4, 4, W - 8, H - 8, 12, 3),
         grime(W, H, "g", 0.12)]
    return svg(W, H, "".join(o), css, defs, "PepeBot end of transmission")


TARGETS = {f"sec-{n}.svg": (lambda n=n, t=t, s=s: header(n, t, s)) for n, t, s in SECTIONS}
TARGETS.update({"hold-receive.svg": hold_receive, "divider.svg": divider, "footer.svg": footer})
