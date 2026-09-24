/**
 * @pepebot/protocol
 *
 * The shared vocabulary between the automation engine, the backend and the robot.
 *   SystemEvent  : something happened in the loop (fees, swaps, payouts, guards)
 *   EmoteFrame   : what the body should do about it (sent to the ESP32 over websocket)
 * See docs/EVENT-PROTOCOL.md for the wire format.
 */

export const SYSTEM_EVENT_TYPES = [
  "system.boot",
  "system.idle",
  "fee.accrued",      // treasury balance went up (observed onchain or simulated)
  "fee.collected",    // a fee claim completed
  "route.planned",    // allocation computed for this cycle
  "swap.quoted",
  "swap.executed",
  "swap.failed",
  "asset.skipped",    // a module was gated or disabled
  "dist.snapshot",
  "dist.planned",
  "dist.completed",
  "guard.halt",       // kill switch or cap tripped
  "guard.resume",
] as const;

export type SystemEventType = (typeof SYSTEM_EVENT_TYPES)[number];
export type EventSource = "chain" | "automation" | "sim" | "operator";

export interface SystemEvent<D extends Record<string, unknown> = Record<string, unknown>> {
  id: string;
  type: SystemEventType;
  ts: number;            // unix ms
  source: EventSource;
  /** true for anything produced by the simulator or a dry-run. Never shown as live. */
  simulated: boolean;
  data: D;
}

export const EMOTES = ["IDLE", "WAKE", "FEED", "ROUTE", "CRUNCH", "PAYOUT", "HALT"] as const;
export type Emote = (typeof EMOTES)[number];

/** backend -> bot */
export interface EmoteFrame {
  t: "emote";
  v: 1;
  seq: number;
  emote: Emote;
  intensity: number;     // 0-255
  ttlMs: number;         // bot falls back to IDLE after this
  reason: SystemEventType;
  simulated: boolean;
}

/** bot -> backend */
export type BotMessage =
  | { t: "hello"; botId: string; fw: string; token: string }
  | { t: "ack"; seq: number }
  | { t: "telemetry"; rssi: number; uptimeS: number; heapFree: number };

export function isSystemEventType(x: unknown): x is SystemEventType {
  return typeof x === "string" && (SYSTEM_EVENT_TYPES as readonly string[]).includes(x);
}

export function isSystemEvent(x: unknown): x is SystemEvent {
  if (!x || typeof x !== "object") return false;
  const e = x as Record<string, unknown>;
  return (
    typeof e.id === "string" &&
    isSystemEventType(e.type) &&
    typeof e.ts === "number" &&
    typeof e.simulated === "boolean" &&
    typeof e.source === "string" &&
    !!e.data && typeof e.data === "object"
  );
}

let counter = 0;
export function makeEvent<D extends Record<string, unknown>>(
  type: SystemEventType,
  source: EventSource,
  simulated: boolean,
  data: D,
): SystemEvent<D> {
  counter = (counter + 1) % 1_000_000;
  return { id: `${Date.now().toString(36)}-${counter}`, type, ts: Date.now(), source, simulated, data };
}

/** What each emote looks like on the rev A body. Firmware: firmware/esp32/src/emotes.cpp */
export const EMOTE_SUMMARY: Record<Emote, string> = {
  IDLE:   "eyes:breathe  leds:dim wave  servo:micro sway",
  WAKE:   "eyes:ramp  leds:sweep  servo:stand",
  FEED:   "eyes:pulse  leds:amber chase  arms:grab",
  ROUTE:  "eyes:scan  leds:split  head:tilt",
  CRUNCH: "eyes:flash x2  leds:flicker  body:shake",
  PAYOUT: "eyes:full  leds:green chase  arms:wave  hop",
  HALT:   "eyes:dim  leds:red strobe  head:droop",
};

export interface EmoteRule { emote: Emote; intensity: number; ttlMs: number }

/** Event -> emote table. The backend EmoteEngine and the simulator both read this. */
export const EMOTE_RULES: Partial<Record<SystemEventType, EmoteRule>> = {
  "system.boot":    { emote: "WAKE",   intensity: 200, ttlMs: 3000 },
  "system.idle":    { emote: "IDLE",   intensity: 60,  ttlMs: 0 },
  "fee.accrued":    { emote: "FEED",   intensity: 160, ttlMs: 2500 },
  "fee.collected":  { emote: "FEED",   intensity: 255, ttlMs: 3000 },
  "route.planned":  { emote: "ROUTE",  intensity: 180, ttlMs: 2000 },
  "swap.quoted":    { emote: "ROUTE",  intensity: 120, ttlMs: 1500 },
  "swap.executed":  { emote: "CRUNCH", intensity: 255, ttlMs: 2500 },
  "swap.failed":    { emote: "HALT",   intensity: 120, ttlMs: 2500 },
  "dist.snapshot":  { emote: "ROUTE",  intensity: 140, ttlMs: 2000 },
  "dist.planned":   { emote: "ROUTE",  intensity: 180, ttlMs: 2000 },
  "dist.completed": { emote: "PAYOUT", intensity: 255, ttlMs: 5000 },
  "guard.halt":     { emote: "HALT",   intensity: 255, ttlMs: 0 },   // sticky until guard.resume
  "guard.resume":   { emote: "WAKE",   intensity: 200, ttlMs: 2500 },
};
