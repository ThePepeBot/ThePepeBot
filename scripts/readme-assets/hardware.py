"""assets/readme/hardware.svg — cutaway of the unit plus the wiring it runs on.
Pin numbers here match firmware/esp32/include/pins.h."""
import math
from lib import P, EYES, logo_uri, matrix, svg, grime_defs, grime, plate, text, chamfer, led, rivets_box

W, H = 1200, 660
S = 360
LX, LY = 152, 170

PINS = [("5V", P["eye"]), ("GND", P["mute"]), ("GPIO8  SDA", P["sol"]), ("GPIO9  SCL", P["sol"]),
        ("GPIO5  EYE DATA", P["amber"]), ("GPIO6  BASE DATA", P["amber"]), ("GPIO4  STATUS", P["phos"]),
        ("GPIO7  PIEZO", P["phos"])]


def fx(u, v):
    return LX + u * S, LY + v * S


def cutaway():
    o = [plate(20, 70, 620, 570, 14, P["deck"], P["hull_lo"], 2), rivets_box(20, 70, 620, 570, 10, 3)]
    o.append(text(40, 100, "UNIT 00  CUTAWAY", 13, P["hull_hi"], weight=700, ls=2))
    o.append(text(620, 100, "scan: x-ray pass", 10, P["mute"], "end"))
    uri = logo_uri(520)
    o.append(f'<use href="#logo" opacity=".92"/>')
    # x-ray band: blueprint-tinted copy + internal parts, visible only inside a moving slot
    guts = (f'<rect x="{LX+175}" y="{LY+215}" width="60" height="38" fill="none" stroke="{P["phos"]}" stroke-width="1.5"/>'
            + text(LX + 205, LY + 238, "ESP32", 9, P["phos"], "middle", 700)
            + f'<rect x="{LX+168}" y="{LY+262}" width="74" height="24" fill="none" stroke="{P["sol"]}" stroke-width="1.2"/>'
            + text(LX + 205, LY + 278, "PCA9685", 8, P["sol"], "middle")
            + f'<path d="M{LX+205} {LY+215}V{LY+110}M{LX+180} {LY+230}L{LX+120} {LY+60}M{LX+230} {LY+230}L{LX+280} {LY+60}'
              f'M{LX+168} {LY+274}L{LX+70} {LY+250}M{LX+242} {LY+274}L{LX+350} {LY+320}M{LX+205} {LY+286}V{LY+306}H{LX+120}M{LX+205} {LY+306}H{LX+300}" '
              f'stroke="{P["phos"]}" stroke-width="1" stroke-dasharray="3 3" fill="none"/>'
            + f'<path d="M{LX+100} {LY+306}H{LX+310}" stroke="{P["amber"]}" stroke-width="3" stroke-dasharray="4 3"/>')
    guts = f'<g transform="translate({LX} {LY}) scale({S/400}) translate({-LX} {-LY})">{guts}</g>'
    o.append(f'<g clip-path="url(#xray)"><rect x="{LX}" y="{LY}" width="{S}" height="{S}" fill="#021208" opacity=".7"/>'
             f'<use href="#logo" filter="url(#blueprint)"/>{guts}</g>')
    o.append(f'<g><rect x="{LX-10}" y="{LY}" width="3" height="{S}" fill="{P["phos"]}"/>'
             f'<animateTransform attributeName="transform" type="translate" values="0 0;{S+60} 0;0 0" dur="9s" repeatCount="indefinite"/></g>')
    callouts = [
        (EYES[0], (38, 150), "EYE L", "WS2812 x12|servo CH0"),
        (EYES[1], (622, 150), "EYE R", "WS2812 x12|servo CH1"),
        ((0.5, 0.25), (622, 250), "HEAD", "tilt|servo CH4"),
        ((0.12, 0.6), (38, 330), "ARM L", "servo CH2"),
        ((0.88, 0.8), (622, 480), "ARM R", "servo CH3"),
        ((0.55, 0.62), (622, 370), "BAY", "ESP32-S3|PCA9685"),
        ((0.5, 0.76), (38, 450), "BASE", "WS2812 x16"),
        ((0.37, 0.88), (38, 560), "LEGS", "spring mounts|passive"),
    ]
    for k, ((u, v), (tx, ty), a, b) in enumerate(callouts):
        px, py = fx(u, v)
        right = tx > 400
        ex = tx - 96 if right else tx + 100
        o.append(f'<path d="M{px:.1f} {py:.1f}L{ex} {ty-4}" stroke="{P["amber"]}" stroke-width="1" class="lead"/>')
        o.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="none" stroke="{P["amber"]}" stroke-width="1.5"/>'
                 f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="{P["amber"]}" class="ping" style="animation-delay:{k*0.35:.2f}s"/>')
        anchor = "end" if right else "start"
        o.append(text(tx, ty, a, 11, P["amber"], anchor, 700, 1.5))
        for j, part in enumerate(b.split("|")):
            o.append(text(tx, ty + 14 + j * 13, part, 9.5, P["text"], anchor))
    return "".join(o)


def schematic():
    o = [plate(660, 70, 520, 570, 14, P["deck"], P["hull_lo"], 2), rivets_box(660, 70, 520, 570, 10, 3)]
    o.append(text(680, 100, "WIRING", 13, P["hull_hi"], weight=700, ls=2))
    o.append(text(1160, 100, "matches firmware/esp32/include/pins.h", 10, P["mute"], "end"))
    # ESP32 block
    ex, ey = 680, 130
    o.append(f'<path d="{chamfer(ex,ey,170,300,6)}" fill="#000" stroke="{P["hull"]}" stroke-width="2"/>')
    o.append(f'<rect x="{ex+20}" y="{ey+14}" width="130" height="60" fill="{P["deck2"]}" stroke="{P["hull_lo"]}"/>'
             + text(ex + 85, ey + 40, "ESP32-S3", 13, P["hull_hi"], "middle", 700)
             + text(ex + 85, ey + 58, "DevKitC-1", 10, P["mute"], "middle"))
    pin_y = {}
    for i, (name, col) in enumerate(PINS):
        py = ey + 100 + i * 24
        pin_y[name] = py
        o.append(f'<rect x="{ex+164}" y="{py-4}" width="12" height="8" fill="{col}"/>' + text(ex + 158, py + 4, name, 10, col, "end"))
    # PCA9685
    px_, py_ = 930, 120
    o.append(f'<path d="{chamfer(px_,py_,230,120,6)}" fill="#000" stroke="{P["sol"]}" stroke-width="1.5"/>'
             + text(px_ + 14, py_ + 22, "PCA9685", 12, P["sol"], weight=700) + text(px_ + 14, py_ + 38, "16ch PWM  /  I2C 0x40", 9.5, P["mute"]))
    for k in range(5):
        sx = px_ + 16 + k * 43
        o.append(f'<rect x="{sx}" y="{py_+56}" width="34" height="46" fill="{P["deck2"]}" stroke="{P["hull_lo"]}"/>'
                 f'<g><path d="M{sx+17} {py_+80}l0 -14" stroke="{P["hull_hi"]}" stroke-width="3" stroke-linecap="round"/>'
                 f'<animateTransform attributeName="transform" type="rotate" values="-35 {sx+17} {py_+80};35 {sx+17} {py_+80};-35 {sx+17} {py_+80}" dur="{1.6+k*0.45:.2f}s" repeatCount="indefinite"/></g>'
                 f'<circle cx="{sx+17}" cy="{py_+80}" r="4" fill="{P["rust_hi"]}"/>'
                 + text(sx + 17, py_ + 98, f"CH{k}", 8.5, P["text"], "middle"))
    # level shifter
    lx, ly = 930, 280
    o.append(f'<path d="{chamfer(lx,ly,110,56,5)}" fill="#000" stroke="{P["amber"]}" stroke-width="1.5"/>'
             + text(lx + 55, ly + 24, "74AHCT125", 10, P["amber"], "middle", 700) + text(lx + 55, ly + 40, "3V3 > 5V data", 9, P["mute"], "middle"))
    # eye rings
    for r_i, (cx, cy) in enumerate([(1080, 300), (1140, 300)]):
        for k in range(12):
            a = 2 * math.pi * k / 12
            o.append(f'<circle cx="{cx+18*math.cos(a):.1f}" cy="{cy+18*math.sin(a):.1f}" r="3.2" fill="{P["eye"]}" class="px" style="animation-delay:{(k+r_i*12)*0.06:.2f}s"/>')
        o.append(text(cx, cy + 38, f"EYE {'LR'[r_i]}", 9, P["eye"], "middle", 700))
    # base strip
    for k in range(16):
        o.append(f'<rect x="{930+k*14.5:.1f}" y="392" width="10" height="10" fill="{P["amber"]}" class="px" style="animation-delay:{k*0.05:.2f}s"/>')
    o.append(text(930, 420, "BASE STRIP  16 px", 9, P["amber"], weight=700))
    # status + piezo
    o.append(led(940, 470, P["phos"], "bl", 5) + text(954, 474, "STATUS", 10, P["phos"]))
    o.append(f'<circle cx="1050" cy="470" r="10" fill="none" stroke="{P["phos"]}" stroke-width="1.5"/><circle cx="1050" cy="470" r="3" fill="{P["phos"]}"/>'
             f'<circle cx="1050" cy="470" r="10" fill="none" stroke="{P["phos"]}" class="chirp"/>' + text(1066, 474, "PIEZO", 10, P["phos"]))
    # power
    wx, wy = 680, 470
    o.append(f'<path d="{chamfer(wx,wy,170,120,6)}" fill="#000" stroke="{P["eye"]}" stroke-width="1.5"/>'
             + text(wx + 14, wy + 24, "5V 6A SUPPLY", 11, P["eye"], weight=700)
             + text(wx + 14, wy + 42, "servos + LEDs on", 9.5, P["mute"]) + text(wx + 14, wy + 56, "their own rail", 9.5, P["mute"])
             + text(wx + 14, wy + 78, "1000uF bulk cap", 9.5, P["mute"]) + text(wx + 14, wy + 92, "common ground", 9.5, P["mute"])
             + text(wx + 14, wy + 106, "fuse inline", 9.5, P["mute"]))
    # wires
    def wire(d, col, speed=1.0):
        return (f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.5" opacity=".45"/>'
                f'<path d="{d}" fill="none" stroke="{col}" stroke-width="2" class="sig" style="animation-duration:{speed}s"/>')
    rx = ex + 176
    o.append(wire(f"M{rx} {pin_y['GPIO8  SDA']}H900V190H930", P["sol"], 0.6))
    o.append(wire(f"M{rx} {pin_y['GPIO9  SCL']}H910V200H930", P["sol"], 0.6))
    o.append(wire(f"M{rx} {pin_y['GPIO5  EYE DATA']}H920V300H930", P["amber"], 0.8))
    o.append(wire(f"M1040 300H1058", P["amber"], 0.8))
    o.append(wire(f"M{rx} {pin_y['GPIO6  BASE DATA']}H905V318H930M1040 318H1052V380H930V392", P["amber"], 0.8))
    o.append(wire(f"M{rx} {pin_y['GPIO4  STATUS']}H895V470H930", P["phos"], 1.2))
    o.append(wire(f"M{rx} {pin_y['GPIO7  PIEZO']}H885V492H1050V480", P["phos"], 1.2))
    o.append(f'<path d="M850 530H1165V240M1165 530V412" fill="none" stroke="{P["eye"]}" stroke-width="2.5" opacity=".7"/>'
             + text(1000, 548, "5V RAIL", 9, P["eye"], "middle", 700))
    o.append(text(680, 620, "never power servos from the ESP32 3V3 pin", 10, P["amber"]))
    return "".join(o)


def build():
    d, w = matrix("HARDWARE REV A", 0, 0, 3)
    head = (f'<rect x="20" y="20" width="{w+30:.0f}" height="36" fill="#000" stroke="{P["hull_lo"]}"/>'
            f'<path d="{d}" fill="{P["phos"]}" transform="translate(35 28)" filter="url(#glow)"/>'
            + text(1180, 44, "prototype reference  /  your build may differ", 11, P["mute"], "end"))
    css = """
.lead{stroke-dasharray:3 4;animation:flow 1.2s linear infinite}@keyframes flow{to{stroke-dashoffset:-14}}
.sig{stroke-dasharray:4 14;animation:flow 1s linear infinite}
.ping{transform-box:fill-box;transform-origin:center;animation:ping 2.8s ease-out infinite}
@keyframes ping{0%{transform:scale(1);opacity:.9}70%,100%{transform:scale(3.2);opacity:0}}
.px{animation:px 1.44s steps(1) infinite}@keyframes px{0%{opacity:1}15%{opacity:.18}}
.bl{animation:bl 1.2s infinite}@keyframes bl{0%,49%{opacity:1}50%,100%{opacity:.2}}
.chirp{transform-box:fill-box;transform-origin:center;animation:ping 1.6s ease-out infinite}
"""
    defs = (grime_defs("g", 52) +
            f'<clipPath id="xray"><rect x="{LX-70}" y="{LY}" width="70" height="{S}"><animateTransform attributeName="transform" type="translate" values="0 0;{S+60} 0;0 0" dur="9s" repeatCount="indefinite"/></rect></clipPath>'
            f'<image id="logo" href="{logo_uri(520)}" x="{LX}" y="{LY}" width="{S}" height="{S}"/>'
            '<filter id="blueprint"><feColorMatrix type="matrix" values="0 0 0 0 0.25  .4 .5 .2 0 0.2  0 0 0 0 0.1  0 0 0 .55 0"/></filter>'
            '<filter id="glow" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="1.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
            f'<pattern id="bp" width="16" height="16" patternUnits="userSpaceOnUse"><path d="M16 0H0V16" fill="none" stroke="{P["seam"]}" opacity=".5"/></pattern>')
    body = (f'<rect width="{W}" height="{H}" fill="{P["void"]}"/><rect width="{W}" height="{H}" fill="url(#bp)"/>'
            + head + cutaway() + schematic() + grime(W, H, "g", 0.08))
    return svg(W, H, body, css, defs, "PepeBot hardware cutaway and wiring")


TARGETS = {"hardware.svg": build}
