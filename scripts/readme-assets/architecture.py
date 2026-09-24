"""assets/readme/architecture.svg — chain to backend to automation to bridge to body.
Animated lines = code in this repo carries that signal (in simulation / dry-run).
Static dashed amber lines = planned paths that do not exist yet."""
from lib import P, matrix, svg, grime_defs, grime, plate, text, chamfer

W, H = 1200, 920
ST = {"IN REPO": P["phos"], "PARTIAL": P["amber"], "PLANNED": P["mute"], "EXTERNAL": P["sol"]}


def box(x, y, w, h, label, sub, status, sub2=None):
    col = ST[status]
    dash = ' stroke-dasharray="5 4"' if status == "PLANNED" else ""
    o = [f'<path d="{chamfer(x,y,w,h,8)}" fill="{P["deck2"] if status!="PLANNED" else P["void"]}" stroke="{col if status!="IN REPO" else P["hull_lo"]}" stroke-width="1.5"{dash}/>',
         f'<rect x="{x}" y="{y+8}" width="4" height="{h-16}" fill="{col}"/>',
         text(x + 14, y + 22, label, 12.5, P["text"], weight=700),
         (text(x + w - 10, y + 20, status, 9, col, "end", 700, 1) if len(label) * 7.6 + len(status) * 6.4 + 34 < w
          else text(x + w - 10, y + h - 9, status, 9, col, "end", 700, 1)),
         text(x + 14, y + 40, sub, 10, P["mute"])]
    if sub2:
        o.append(text(x + 14, y + 56, sub2, 10, P["mute"]))
    return "".join(o)


def lane(y, h, name, path):
    d, w = matrix(name, 0, 0, 2.3)
    return (f'<path d="{chamfer(20,y,112,h,8)}" fill="{P["deck"]}" stroke="{P["hull_lo"]}"/>'
            f'<path d="{d}" fill="{P["hull_hi"]}" transform="translate({76 - w/2:.1f} {y + h/2 - 16:.1f})"/>'
            + text(76, y + h / 2 + 18, path, 9.5, P["mute"], "middle")
            + f'<path d="M140 {y+h+14}H1180" stroke="{P["seam"]}" stroke-dasharray="2 6"/>')


def flow(d, color=None, speed=1.0, label=None, lx=0, ly=0, anchor="start"):
    color = color or P["phos"]
    o = (f'<path d="{d}" fill="none" stroke="#000" stroke-width="6" opacity=".8"/>'
         f'<path d="{d}" fill="none" stroke="{P["hull_lo"]}" stroke-width="2.5"/>'
         f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2" class="flow" style="animation-duration:{speed}s" marker-end="url(#ah)"/>')
    if label:
        o += text(lx, ly, label, 9.5, color, anchor)
    return o


def planned(d, label=None, lx=0, ly=0, anchor="start"):
    o = f'<path d="{d}" fill="none" stroke="{P["amber"]}" stroke-width="1.5" stroke-dasharray="3 5" opacity=".85" marker-end="url(#ahA)"/>'
    if label:
        o += text(lx, ly, label, 9.5, P["amber"], anchor)
    return o


def build():
    o = [f'<rect width="{W}" height="{H}" fill="{P["void"]}"/><rect width="{W}" height="{H}" fill="url(#grid)"/>',
         f'<path d="{chamfer(8,8,W-16,H-16,18)}" fill="none" stroke="{P["hull_lo"]}" stroke-width="2"/>']
    # legend
    o.append(text(24, 42, "SYSTEM MAP PB-ARCH-02", 13, P["hull_hi"], weight=700, ls=2))
    lx = 330
    for k, c in ST.items():
        o.append(f'<rect x="{lx}" y="32" width="10" height="10" fill="{c}"/>' + text(lx + 16, 42, k, 10, c, weight=700, ls=1))
        lx += 110
    o.append(f'<path d="M790 38h26" stroke="{P["phos"]}" stroke-width="2" class="flow"/>' + text(822, 42, "live path (sim / dry-run)", 10, P["text"]))
    o.append(f'<path d="M985 38h26" stroke="{P["amber"]}" stroke-width="1.5" stroke-dasharray="3 5"/>' + text(1017, 42, "planned path", 10, P["amber"]))

    lanes = [(70, 110, "CHAIN", "solana mainnet"), (220, 110, "INGEST", "backend/"),
             (370, 190, "ENGINE", "automation/"), (590, 100, "BRIDGE", "backend/"),
             (720, 160, "BODY", "firmware/ hardware/")]
    for y, h, n, pth in lanes:
        o.append(lane(y, h, n, pth))

    # --- flows under boxes
    o.append(flow("M350 130H368", P["amber"]))
    o.append(flow("M465 165V192H440V362H245V393", P["amber"], 1.2, "fees", 448, 352))
    o.append(flow("M675 165V205H300V243", P["sol"], 1.4, "account changes", 560, 200))
    o.append(flow("M420 280H458", P["sol"]))
    o.append(flow("M625 393V317", P["phos"], 0.9, "cycle events", 632, 356))
    o.append(flow("M460 300H146V642H158", P["eye"], 0.8, "system events", 150, 470))
    o.append(flow("M460 642H498", P["eye"], 0.6))
    o.append(flow("M840 642H802", P["eye"], 0.6, "drives", 806, 634))
    o.append(flow("M650 674V708H290V738", P["eye"], 0.7, "emote frames / ws", 300, 702))
    o.append(flow("M420 768H458", P["phos"], 0.5))
    o.append(flow("M420 842H458", P["phos"], 0.5))
    o.append(flow("M420 805H700V768H718", P["phos"], 0.5))
    o.append(flow("M700 805V842H718", P["phos"], 0.5))
    o.append(f'<path d="M980 805H955V768H942M955 805V842H942" fill="none" stroke="{P["eye"]}" stroke-width="2" stroke-dasharray="1 3" opacity=".7"/>')
    # automation internals
    o.append(flow("M330 427H348", P["amber"], 0.7))
    o.append(flow("M520 427H538", P["amber"], 0.7))
    o.append(flow("M710 427H728", P["hull_hi"], 0.7))
    o.append(flow("M710 445H719V507H728", P["sol"], 0.9))
    o.append(flow("M930 427H948", P["hull_hi"], 0.7))
    o.append(flow("M930 507H948", P["sol"], 0.9))
    o.append(flow("M245 475V461", P["phos"], 0.6))
    # planned broadcast paths
    o.append(planned("M830 393V360H780V200H880V167", "swap tx: planned", 786, 358))
    o.append(planned("M1125 393V167", "payout tx: planned", 1118, 380, "end"))

    # --- boxes
    B = [
        (160, 95, 190, 70, "PEPEBOT pool", "trading venue", "EXTERNAL"),
        (370, 95, 190, 70, "fee source", "creator / LP fee account", "EXTERNAL"),
        (580, 95, 190, 70, "treasury", "operator multisig", "EXTERNAL"),
        (790, 95, 180, 70, "PEPE + asset mints", "SPL / Token-2022", "EXTERNAL"),
        (990, 95, 180, 70, "holder accounts", "PEPEBOT balances", "EXTERNAL"),
        (160, 245, 260, 70, "chain listener", "RPC websocket + webhook ingress", "IN REPO"),
        (460, 245, 300, 70, "event bus", "packages/protocol: typed events", "IN REPO"),
        (800, 245, 280, 70, "status api", "GET /health  /status", "PARTIAL", "dashboard: planned"),
        (160, 395, 170, 64, "fee adapter", "venue claim()", "PARTIAL", "mock in repo"),
        (350, 395, 170, 64, "guardrails", "caps + kill switch", "IN REPO", "dry-run default"),
        (540, 395, 170, 64, "allocator", "split by config", "IN REPO"),
        (730, 395, 200, 64, "pepe swap", "aggregator quote", "PARTIAL", "execution planned"),
        (730, 475, 200, 64, "asset modules", "provider + compliance", "PLANNED", "gate per module"),
        (950, 395, 220, 144, "distributor", "snapshot  exclude", "PARTIAL", "pro-rata  batch"),
        (160, 475, 550, 64, "cycle scheduler", "runCycle() on an interval  /  one cycle = claim > allocate > buy > plan payout", "IN REPO"),
        (160, 610, 300, 64, "emote engine", "event > emote  /  priority + cooldown", "IN REPO"),
        (500, 610, 300, 64, "bot gateway", "ws :8787  seq / ack / heartbeat", "IN REPO"),
        (840, 610, 330, 64, "simulator", "scripts/simulate.ts  /  no keys needed", "IN REPO"),
        (160, 740, 260, 130, "ESP32-S3", "ws client", "IN REPO", "emote state machine"),
        (460, 740, 220, 56, "PCA9685 + 5 servos", "eyes x2  arms x2  tilt", "IN REPO"),
        (460, 814, 220, 56, "WS2812 eye rings", "2 x 12 px behind lenses", "IN REPO"),
        (720, 740, 220, 56, "WS2812 base strip", "16 px  chase / strobe", "IN REPO"),
        (720, 814, 220, 56, "status lamp + piezo", "link state  /  chirps", "IN REPO"),
        (980, 740, 190, 130, "power", "5V 6A supply", "PLANNED", "bulk cap + level shift"),
    ]
    for b in B:
        o.append(box(*b))
    # distributor inner steps
    for i, s in enumerate(["SNAPSHOT", "EXCLUDE", "PRO-RATA", "BATCH", "SEND"]):
        cy = 470 + i * 14
        col = P["phos"] if s != "SEND" else P["amber"]
        o.append(f'<rect x="964" y="{cy-7}" width="6" height="6" fill="{col}" class="seq{i}"/>' + text(976, cy, s, 9, col))
    o.append(text(1060, 526, "send: planned", 9, P["amber"]))
    # esp32 chip art
    o.append(f'<rect x="178" y="806" width="60" height="46" fill="#000" stroke="{P["hull"]}"/>'
             + "".join(f'<path d="M{182+k*8} 806v-5M{182+k*8} 852v5" stroke="{P["hull_hi"]}"/>' for k in range(7))
             + text(208, 834, "S3", 13, P["hull_hi"], "middle", 700))
    o.append(f'<circle cx="270" cy="828" r="6" fill="{P["sol"]}" class="bl"/>' + text(282, 832, "link", 10, P["sol"]))
    o.append(grime(W, H, "g", 0.08))
    css = """
.flow{stroke-dasharray:6 8;animation:flow 1s linear infinite}@keyframes flow{to{stroke-dashoffset:-14}}
.bl{animation:bl 1.2s infinite}@keyframes bl{0%,49%{opacity:1}50%,100%{opacity:.2}}
.seq0,.seq1,.seq2,.seq3,.seq4{opacity:.2;animation:seq 5s steps(1) infinite}
.seq1{animation-delay:1s}.seq2{animation-delay:2s}.seq3{animation-delay:3s}.seq4{animation-delay:4s}
@keyframes seq{0%{opacity:1}20%{opacity:.2}}
"""
    defs = (grime_defs("g", 44) +
            f'<pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="{P["seam"]}" opacity=".35"/></pattern>'
            f'<marker id="ah" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L8 4L0 8Z" fill="{P["text"]}"/></marker>'
            f'<marker id="ahA" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L8 4L0 8Z" fill="{P["amber"]}"/></marker>')
    return svg(W, H, "".join(o), css, defs, "PepeBot system architecture")


TARGETS = {"architecture.svg": build}
