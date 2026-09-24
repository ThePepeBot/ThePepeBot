import { makeEvent, type EventSource } from "@pepebot/protocol";
import { fmtSol, isLive, toLamports, type Config } from "./config.js";
import type { FeeAdapter } from "./fees/adapter.js";
import { allocate, distributable, splitWeighted } from "./router/allocate.js";
import type { Quoter } from "./swap/quoter.js";
import { WSOL } from "./swap/quoter.js";
import { buildModules } from "./assets/registry.js";
import type { Holder } from "./distributor/snapshot.js";
import { planDistribution } from "./distributor/plan.js";
import { chunk } from "./distributor/batch.js";
import { preflight } from "./guard.js";
import type { Publisher } from "./publish.js";

export interface CycleDeps {
  cfg: Config;
  fees: FeeAdapter;
  quoter: Quoter;
  holders: () => Promise<Holder[]>;
  publish: Publisher;
  log: (line: string) => void;
  source: EventSource;
  simulated: boolean;
  cycleNo: number;
}

export interface CycleResult { status: "done" | "halted" | "empty"; spentLamports: bigint }

const pad = (tag: string) => `[${tag}]`.padEnd(8);

/**
 * One pass of the loop: fees -> reserve/cap -> split -> PEPE quote -> asset modules
 * -> holder snapshot -> pro-rata plan -> batches.
 * In this build every spend path is dry-run: quotes are fetched, nothing is signed.
 */
export async function runCycle(d: CycleDeps): Promise<CycleResult> {
  const { cfg, log, simulated, source } = d;
  const emit = (type: Parameters<typeof makeEvent>[0], data: Record<string, unknown>) =>
    d.publish(makeEvent(type, source, simulated, data));
  const L = (tag: string, s: string) => log(`${pad(tag)}${s}`);
  const dry = !isLive(cfg);

  const g = preflight(cfg);
  if (!g.ok) { L("guard", `HALT  ${g.reason}`); await emit("guard.halt", { reason: g.reason }); return { status: "halted", spentLamports: 0n }; }

  // 1. fees
  L("fee", `tick  venue=${d.fees.id}  pool=${d.fees.venue}`);
  const claimable = await d.fees.claimable();
  L("fee", `claimable  ${fmtSol(claimable)} SOL${simulated ? "  (simulated)" : ""}`);
  await d.fees.claim(dry);
  await emit("fee.collected", { lamports: claimable.toString(), dryRun: dry });

  // 2. route
  const spend = distributable(claimable, toLamports(cfg.treasury.reserve_sol), toLamports(cfg.guardrails.max_sol_per_cycle));
  if (spend === 0n) { L("route", "nothing above reserve -> skip cycle"); await emit("system.idle", {}); return { status: "empty", spentLamports: 0n }; }
  const split = allocate(spend, cfg.allocation.pepe_bps);
  L("route", `allocation  PEPE ${cfg.allocation.pepe_bps / 100}%  |  ASSETS ${cfg.allocation.assets_bps / 100}%`);
  L("route", `reserve ${cfg.treasury.reserve_sol.toFixed(3)} SOL kept  ->  distributable ${fmtSol(spend)} SOL`);
  await emit("route.planned", { pepe: split.pepe.toString(), assets: split.assets.toString() });

  // 3. PEPE
  const pq = await d.quoter.quote(WSOL, cfg.pepe.mint, split.pepe, cfg.pepe.slippage_bps);
  L("swap", `quote  SOL>PEPE  ${fmtSol(split.pepe)} SOL  slippage cap ${cfg.pepe.slippage_bps}bps  route=${pq.routeLabel}`);
  await emit("swap.quoted", { asset: "PEPE", inLamports: split.pepe.toString() });
  if (dry) L("swap", "DRY-RUN  quote only, nothing signed or broadcast");
  if (simulated) await emit("swap.executed", { asset: "PEPE", dryRun: true });

  // 4. asset modules
  const payoutAssets: Array<{ id: string; amount: bigint }> = [{ id: "PEPE", amount: pq.outAmount }];
  let held = 0n;
  const mods = buildModules(cfg.assets.modules).map((mod, i) => ({ mod, weight_bps: cfg.assets.modules[i]!.weight_bps }));
  for (const [{ mod, weight_bps }, budget] of splitWeighted(split.assets, mods)) {
    const el = mod.eligibility();
    const w = `${weight_bps / 100}%`;
    if (!el.ok) {
      L("asset", `${mod.id.padEnd(13)} GATED   ${w}  ${el.reason} -> skip`);
      held += budget;
      await emit("asset.skipped", { module: mod.id, reason: el.reason });
      continue;
    }
    const q = await mod.quote(budget, d.quoter, cfg.pepe.slippage_bps);
    L("asset", `${mod.id.padEnd(13)} ENABLED ${w}  ${fmtSol(budget)} SOL quote ok  ${dry ? "DRY-RUN" : ""}`);
    if (mod.distributable()) payoutAssets.push({ id: mod.id, amount: q.outAmount });
  }
  if (held > 0n) L("asset", `gated share ${fmtSol(held)} SOL -> held in treasury`);

  // 5. distribution
  const holders = await d.holders();
  L("dist", `snapshot  mint=PEPEBOT  accounts=${holders.length.toLocaleString("en-US")}${simulated ? "  (simulated)" : ""}`);
  await emit("dist.snapshot", { accounts: holders.length });
  const exclude = new Map(cfg.distribution.exclude.map((e) => [e.address, e.label]));
  let batches = 0, recipients = 0, eligible = 0;
  const carried: string[] = [];
  for (const [i, a] of payoutAssets.entries()) {
    const plan = planDistribution({
      holders, total: a.amount, exclude,
      minBalance: BigInt(cfg.distribution.min_balance), minPayout: BigInt(cfg.distribution.min_payout),
    });
    if (i === 0) {
      L("dist", `exclude   ${Object.entries(plan.excluded).map(([k, v]) => `${k}:${v}`).join("  ")}`);
      L("dist", `min_balance ${cfg.distribution.min_balance}  below=${plan.belowMin}  eligible=${plan.eligible.toLocaleString("en-US")}`);
      eligible = plan.eligible;
    }
    recipients = Math.max(recipients, plan.payouts.length);
    batches = Math.max(batches, chunk(plan.payouts, cfg.distribution.batch_size).length);
    if (plan.carried > 0n) carried.push(a.id);
  }
  L("dist", `pro-rata plan  assets=${payoutAssets.map((a) => a.id).join(",")}  rounding/dust -> carried (${carried.join(",") || "none"})`);
  L("dist", `batches  ${batches} x ${cfg.distribution.batch_size}  recipients=${recipients.toLocaleString("en-US")}  status=PLANNED (not sent)`);
  await emit("dist.planned", { eligible, recipients, batches });
  if (simulated) await emit("dist.completed", { recipients, dryRun: true });

  return { status: "done", spentLamports: dry ? 0n : spend };
}
