# Event protocol (v1)

Types live in `packages/protocol/src/index.ts`. That file is the source of truth.

## SystemEvent (anything → backend)

```json
{ "id": "m1x2-7", "type": "swap.quoted", "ts": 1760000000000,
  "source": "automation", "simulated": false, "data": { "asset": "PEPE" } }
```

`simulated: true` is set by the simulator and by every dry-run path that pretends an action happened.
Consumers must never display a simulated event as live.

Ingest: `POST /events` with `Authorization: Bearer $INGEST_TOKEN`. Chain webhooks: `POST /webhooks/chain`.

## EmoteFrame (backend → bot)

```json
{ "t": "emote", "v": 1, "seq": 42, "emote": "PAYOUT", "intensity": 255,
  "ttlMs": 5000, "reason": "dist.completed", "simulated": true }
```

`ttlMs: 0` means sticky (used by `HALT` until `guard.resume`).

## Bot → backend

| message | when |
|---|---|
| `{"t":"hello","botId","fw","token"}` | first frame, within 5 s of connect or the socket is closed |
| `{"t":"ack","seq"}` | after each emote frame |
| `{"t":"telemetry","rssi","uptimeS","heapFree"}` | every 30 s |

## Event → emote

| event | emote | body |
|---|---|---|
| system.boot | WAKE | eyes ramp, LED sweep, stand |
| fee.accrued / fee.collected | FEED | eyes pulse, amber chase, arms grab |
| route.planned, swap.quoted, dist.snapshot, dist.planned | ROUTE | eye scan, split LEDs, head tilt |
| swap.executed | CRUNCH | double flash, flicker, shake |
| dist.completed | PAYOUT | full eyes, green chase, wave, hop |
| swap.failed, guard.halt | HALT | eyes dim, red strobe, droop (sticky on guard.halt) |
| guard.resume | WAKE | |

Engine rules: HALT > PAYOUT > CRUNCH > FEED > WAKE > ROUTE > IDLE. A playing emote is not interrupted by a lower one. Same emote within 700 ms is dropped.
