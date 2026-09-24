"""assets/readme/terminal.svg — a CRT playing back one simulated cycle of `npm run sim`.
The text mirrors what scripts/simulate.ts prints, so the README never shows output the code can't produce."""
import re
from lib import P, svg, grime_defs, grime, plate, rivets_box, text, led, chamfer, MONO

W, H = 1200, 620
SX, SY, SW, SH = 40, 72, 1120, 510     # screen
LH = 22.5
X0 = SX + 26
Y0 = SY + 34
VISIBLE = 19
T = 38.0  # seconds per cycle

TAGCOL = {"boot": P["mute"], "link": P["sol"], "bot": P["eye"], "fee": P["amber"], "route": P["phos"],
          "swap": P["hull_hi"], "asset": P["sol"], "dist": P["phos"], "loop": P["amber"]}

# (delay-after-previous, line)   {a}=amber {r}=red {g}=green {m}=muted {/}=reset
SCRIPT = [
    (0.4, "$ npm run sim"),
    (1.3, "{m}> pepebot@0.1.0 sim{/}"),
    (0.15, "{m}> tsx scripts/simulate.ts --dry-run{/}"),
    (0.7, "[boot]  PEPEBOT-OS 0.1 // unit 00"),
    (0.25, "[boot]  mode={a}SIMULATION{/}  broadcast={a}OFF{/}  kill_switch={g}SAFE{/}"),
    (0.25, "[boot]  modules  fee-intake  treasury  router  pepe-swap  asset-bay  distributor"),
    (0.9, "[link]  backend http://localhost:8080  {g}(events forwarded){/}"),
    (0.5, "[bot]   emote -> {r}WAKE{/}     eyes:ramp  leds:sweep  servo:stand"),
    (1.4, "[fee]   tick  venue=adapter:mock  pool=PEPEBOT/SOL"),
    (0.6, "[fee]   claimable  12.500 SOL  {a}(simulated){/}"),
    (0.4, "[bot]   emote -> {r}FEED{/}     eyes:pulse  leds:amber chase  arms:grab"),
    (1.2, "[route] allocation  PEPE 80%  |  ASSETS 20%"),
    (0.3, "[route] reserve 0.050 SOL kept  ->  distributable 12.450 SOL"),
    (1.0, "[swap]  quote  SOL>PEPE  9.960 SOL  slippage cap 50bps  route=mock"),
    (0.6, "[swap]  {a}DRY-RUN{/}  quote only, nothing signed or broadcast"),
    (0.4, "[bot]   emote -> {r}CRUNCH{/}   eyes:flash x2  leds:flicker  body:shake"),
    (0.8, "[asset] sol-lst       {g}ENABLED{/} 50%  1.245 SOL quote ok  {a}DRY-RUN{/}"),
    (0.4, "[asset] tokenized-eq  {r}GATED{/}   50%  no provider adapter / eligibility unresolved -> skip"),
    (0.3, "[asset] gated share 1.245 SOL -> held in treasury"),
    (1.4, "[dist]  snapshot  mint=PEPEBOT  accounts=1,337  {a}(simulated){/}"),
    (0.4, "[dist]  exclude   lp:2  burn:1  treasury:1  programs:4"),
    (0.4, "[dist]  min_balance 100000  below=139  eligible=1,190"),
    (0.6, "[dist]  pro-rata plan  assets=PEPE,sol-lst  rounding/dust -> carried (PEPE,sol-lst)"),
    (0.5, "[dist]  batches  24 x 50  recipients=1,190  status={a}PLANNED (not sent){/}"),
    (0.6, "[bot]   emote -> {r}PAYOUT{/}   eyes:full  leds:green chase  arms:wave  hop"),
    (1.2, "[loop]  cycle 0001 complete  //  next cycle in 3600s"),
    (0.5, "[loop]  all numbers above are synthetic. nothing was signed or sent."),
    (0.6, "[loop]  {g}HOLD PEPEBOT. RECEIVE PEPE.{/}"),
    (0.9, "$ "),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_line(s, y, idx):
    col = {"a": P["amber"], "r": P["eye"], "g": P["phos"], "m": P["mute"]}
    spans = []
    base = P["text"]
    m = re.match(r"\[(\w+)\]", s)
    if s.startswith("$"):
        spans.append(f'<tspan fill="{P["phos"]}" font-weight="700">$</tspan><tspan fill="{P["text"]}">{esc(s[1:])}</tspan>')
    else:
        if m:
            tag = m.group(1)
            spans.append(f'<tspan fill="{TAGCOL.get(tag, base)}" font-weight="700">{esc(m.group(0))}</tspan>')
            s = s[len(m.group(0)):]
        cur = base
        for part in re.split(r"(\{[agrm/]\})", s):
            if not part:
                continue
            mm = re.fullmatch(r"\{([agrm/])\}", part)
            if mm:
                cur = base if mm.group(1) == "/" else col[mm.group(1)]
                continue
            spans.append(f'<tspan fill="{cur}">{esc(part)}</tspan>')
    body = "".join(spans)
    return (f'<text x="{X0}" y="{y:.1f}" font-size="14" xml:space="preserve" class="ln{idx}" '
            f'style="white-space:pre">{body}</text>')


def build():
    css = [f".scr{{animation:flick 5s infinite}}@keyframes flick{{0%,100%{{opacity:1}}48%{{opacity:.96}}50%{{opacity:1}}}}"]
    lines = []
    times = []
    t = 0
    for d, _ in SCRIPT:
        t += d
        times.append(t)
    end_p = 95.0
    covers = []
    for i, (_, s) in enumerate(SCRIPT):
        y = Y0 + i * LH
        p = times[i] / T * 100
        css.append(f".ln{i}{{opacity:0;animation:ln{i} {T}s linear infinite}}"
                   f"@keyframes ln{i}{{0%,{p:.2f}%{{opacity:0}}{p+0.01:.2f}%,{end_p}%{{opacity:1}}{end_p+1.5:.2f}%,100%{{opacity:0}}}}")
        lines.append(render_line(s, y, i))
        if s.startswith("$") and len(s) > 2:
            # typing shutter: a screen-coloured block slides right to reveal the command
            tw = len(s) * 8.45
            dur_p = 1.0 / T * 100
            css.append(f".cv{i}{{animation:cv{i} {T}s linear infinite}}"
                       f"@keyframes cv{i}{{0%,{p:.2f}%{{transform:translateX(0)}}{p+dur_p:.2f}%,100%{{transform:translateX({tw+20:.0f}px)}}}}")
            covers.append(f'<g class="cv{i}"><rect x="{X0+12}" y="{y-16}" width="{tw+40:.0f}" height="{LH}" fill="#020503"/>'
                          f'<rect x="{X0+12}" y="{y-14}" width="9" height="17" fill="{P["phos"]}"/></g>')
    # scroll
    frames = ["0%{transform:translateY(0)}"]
    shift = 0
    for i in range(VISIBLE, len(SCRIPT)):
        p = times[i] / T * 100
        frames.append(f"{p-0.01:.2f}%{{transform:translateY({-shift*LH:.1f}px)}}")
        shift += 1
        frames.append(f"{p+0.5:.2f}%{{transform:translateY({-shift*LH:.1f}px)}}")
    frames.append(f"{end_p+1.6:.2f}%{{transform:translateY({-shift*LH:.1f}px)}}")
    frames.append(f"{end_p+1.7:.2f}%,100%{{transform:translateY(0)}}")
    css.append(f".scroll{{animation:scroll {T}s linear infinite}}@keyframes scroll{{{''.join(frames)}}}")
    # blinking cursor on the last prompt
    last = len(SCRIPT) - 1
    cy = Y0 + last * LH
    cursor = f'<g class="ln{last}"><rect x="{X0+22}" y="{cy-14}" width="9" height="17" fill="{P["phos"]}" class="cur"/></g>'
    css.append(".cur{animation:cur 1s steps(1) infinite}@keyframes cur{50%{opacity:0}}")
    css.append(f".band{{animation:band 7s linear infinite}}@keyframes band{{from{{transform:translateY(0)}}to{{transform:translateY({SH+120}px)}}}}")
    css.append("@media (prefers-reduced-motion: reduce){[class^=ln]{opacity:1!important}[class^=cv]{display:none}}")
    css.append("@keyframes bl{0%,49%{opacity:1}50%,100%{opacity:.25}}.bl1{animation:bl 1.2s infinite}.bl2{animation:bl .7s infinite}")

    defs = (grime_defs("g", 21) +
            f'<clipPath id="screen"><rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" rx="18"/></clipPath>'
            f'<pattern id="scan" width="4" height="3" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".45"/></pattern>'
            f'<radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".75"/></radialGradient>'
            f'<linearGradient id="bandg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{P["phos"]}" stop-opacity="0"/><stop offset=".5" stop-color="{P["phos"]}" stop-opacity=".06"/><stop offset="1" stop-color="{P["phos"]}" stop-opacity="0"/></linearGradient>'
            f'<filter id="phosphor" x="-2%" y="-2%" width="104%" height="104%"><feGaussianBlur stdDeviation="1.1" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')

    body = [f'<rect width="{W}" height="{H}" fill="{P["void"]}"/>',
            f'<path d="{chamfer(8,8,W-16,H-16,20)}" fill="{P["deck"]}" stroke="{P["hull_lo"]}" stroke-width="2"/>',
            rivets_box(8, 8, W - 16, H - 16, 14, 3),
            led(44, 38, P["phos"], "bl1", 4), led(62, 38, P["amber"], "bl2", 4), led(80, 38, P["eye"], "", 4),
            text(100, 43, "TTY0", 13, P["hull_hi"], weight=700, ls=2),
            text(150, 43, "pepebot@unit-00:~/pepebot", 13, P["text"]),
            text(1160, 43, "SIMULATION / NOT LIVE DATA / NOTHING IS BROADCAST", 12, P["amber"], "end", 700, 1),
            f'<rect x="{SX-6}" y="{SY-6}" width="{SW+12}" height="{SH+12}" rx="22" fill="#000" stroke="{P["hull_lo"]}" stroke-width="3"/>',
            f'<g clip-path="url(#screen)"><rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" fill="#020503"/>',
            f'<g class="scr" filter="url(#phosphor)"><g class="scroll">{"".join(lines)}{"".join(covers)}{cursor}</g></g>',
            f'<rect x="{SX}" y="{SY-120}" width="{SW}" height="120" fill="url(#bandg)" class="band"/>',
            f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" fill="url(#scan)"/>',
            f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" fill="url(#vig)"/></g>',
            f'<g transform="rotate(-7 1010 130)" opacity=".85"><rect x="890" y="108" width="240" height="44" fill="none" stroke="{P["amber"]}" stroke-width="2.5"/>'
            f'<text x="1010" y="137" font-size="17" font-weight="800" fill="{P["amber"]}" text-anchor="middle" letter-spacing="3">SIMULATION</text></g>',
            text(SX, H - 18, "output of scripts/simulate.ts  /  every figure is generated by the simulator", 11, P["mute"]),
            grime(W, H, "g", 0.08)]
    return svg(W, H, "".join(body), "".join(css), defs, "Simulated PepeBot terminal cycle")


TARGETS = {"terminal.svg": build}
