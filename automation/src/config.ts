import { readFileSync } from "node:fs";
import { parse } from "yaml";
import { z } from "zod";

const Module = z.object({
  id: z.string(),
  kind: z.enum(["spl-token", "tokenized-equity"]),
  mint: z.string().optional(),
  provider: z.string().nullable().optional(),
  weight_bps: z.number().int().min(0).max(10_000),
  enabled: z.boolean(),
  jurisdictions_allowed: z.array(z.string()).optional(),
  requires_holder_kyc: z.boolean().optional(),
});

export const ConfigSchema = z.object({
  cycle: z.object({ interval_seconds: z.number().int().positive(), dry_run: z.boolean() }),
  treasury: z.object({ address: z.string(), reserve_sol: z.number().min(0) }),
  allocation: z
    .object({ pepe_bps: z.number().int().min(0), assets_bps: z.number().int().min(0) })
    .refine((a) => a.pepe_bps + a.assets_bps === 10_000, "allocation must sum to 10000 bps"),
  pepe: z.object({ mint: z.string(), slippage_bps: z.number().int().min(0).max(1000) }),
  assets: z.object({
    modules: z.array(Module).refine(
      (m) => m.length === 0 || m.reduce((s, x) => s + x.weight_bps, 0) === 10_000,
      "asset module weights must sum to 10000 bps",
    ),
  }),
  distribution: z.object({
    token_mint: z.string(),
    min_balance: z.number().int().min(0),
    min_payout: z.number().int().min(0),
    batch_size: z.number().int().min(1).max(200),
    exclude: z.array(z.object({ label: z.string(), address: z.string() })),
  }),
  guardrails: z.object({
    max_sol_per_cycle: z.number().positive(),
    max_slippage_bps: z.number().int().min(0),
    kill_switch_file: z.string(),
  }),
});

export type Config = z.infer<typeof ConfigSchema>;
export type ModuleConfig = z.infer<typeof Module>;

export function loadConfig(path = process.env.PEPEBOT_CONFIG ?? "config/allocation.example.yaml"): Config {
  const cfg = ConfigSchema.parse(parse(readFileSync(path, "utf8")));
  if (cfg.pepe.slippage_bps > cfg.guardrails.max_slippage_bps) {
    throw new Error("pepe.slippage_bps exceeds guardrails.max_slippage_bps");
  }
  return cfg;
}

export const LAMPORTS = 1_000_000_000n;
export const toLamports = (sol: number): bigint => BigInt(Math.round(sol * 1e9));
export const fmtSol = (l: bigint): string => (Number(l) / 1e9).toFixed(3);

/** Live execution needs BOTH the config flag off and the env flag on. */
export function isLive(cfg: Config): boolean {
  return cfg.cycle.dry_run === false && process.env.PEPEBOT_LIVE === "true";
}
