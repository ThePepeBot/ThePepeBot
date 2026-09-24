import { existsSync } from "node:fs";
import type { Config } from "./config.js";

export type GuardResult = { ok: true } | { ok: false; reason: string };

/** Checked before every cycle and before every spend. Any failure halts the cycle. */
export function preflight(cfg: Config): GuardResult {
  if (existsSync(cfg.guardrails.kill_switch_file)) return { ok: false, reason: `kill switch file present (${cfg.guardrails.kill_switch_file})` };
  if (cfg.pepe.slippage_bps > cfg.guardrails.max_slippage_bps) return { ok: false, reason: "slippage above guardrail" };
  return { ok: true };
}
