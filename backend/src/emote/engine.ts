import { EMOTE_RULES, type Emote, type EmoteFrame, type SystemEvent } from "@pepebot/protocol";

export { EMOTE_RULES };


const PRIORITY: Record<Emote, number> = { HALT: 100, PAYOUT: 80, CRUNCH: 60, FEED: 50, WAKE: 40, ROUTE: 30, IDLE: 0 };
const COOLDOWN_MS = 700;

/**
 * Turns system events into emote frames.
 * - a higher-priority emote that is still playing is not interrupted
 * - guard.halt is sticky: nothing but guard.resume clears it
 * - identical emotes inside the cooldown window are dropped (no servo chatter)
 */
export class EmoteEngine {
  private seq = 0;
  private current: { frame: EmoteFrame; until: number } | null = null;
  private halted = false;
  private lastSent = new Map<Emote, number>();

  constructor(private readonly now: () => number = Date.now) {}

  handle(e: SystemEvent): EmoteFrame | null {
    const rule = EMOTE_RULES[e.type];
    if (!rule) return null;
    const t = this.now();

    if (this.halted && e.type !== "guard.resume") return null;
    if (e.type === "guard.halt") this.halted = true;
    if (e.type === "guard.resume") this.halted = false;

    const active = this.current && (this.current.until === Infinity || this.current.until > t) ? this.current.frame : null;
    if (active && e.type !== "guard.resume" && PRIORITY[active.emote] > PRIORITY[rule.emote]) return null;

    const last = this.lastSent.get(rule.emote) ?? -Infinity;
    if (t - last < COOLDOWN_MS && e.type !== "guard.halt" && e.type !== "guard.resume") return null;

    const frame: EmoteFrame = {
      t: "emote", v: 1, seq: ++this.seq, emote: rule.emote, intensity: rule.intensity,
      ttlMs: rule.ttlMs, reason: e.type, simulated: e.simulated,
    };
    this.current = { frame, until: rule.ttlMs === 0 ? Infinity : t + rule.ttlMs };
    this.lastSent.set(rule.emote, t);
    return frame;
  }

  /** Frame to replay when a bot (re)connects. */
  snapshot(): EmoteFrame | null {
    if (!this.current) return null;
    if (this.current.until !== Infinity && this.current.until < this.now()) return null;
    return this.current.frame;
  }
}
