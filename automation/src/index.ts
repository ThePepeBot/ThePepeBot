import { Connection } from "@solana/web3.js";
import { loadConfig } from "./config.js";
import { runCycle } from "./cycle.js";
import { AggregatorQuoter } from "./swap/jupiter.js";
import { snapshotHolders } from "./distributor/snapshot.js";
import { httpPublisher } from "./publish.js";
import type { FeeAdapter } from "./fees/adapter.js";

/**
 * Scheduler for real (dry-run) cycles against mainnet data.
 * There is no venue fee adapter in this build, so the treasury's SOL balance
 * above reserve stands in for "claimable". Quotes and snapshots are real reads;
 * nothing is signed.
 */
const cfg = loadConfig();
const rpc = process.env.SOLANA_RPC_URL;
if (!rpc) { console.error("SOLANA_RPC_URL is required. For a fully offline demo run: npm run sim"); process.exit(1); }
const conn = new Connection(rpc, "confirmed");

const balanceAdapter: FeeAdapter = {
  id: "adapter:treasury-balance", venue: "n/a",
  claimable: async () => BigInt(await conn.getBalance(new (await import("@solana/web3.js")).PublicKey(cfg.treasury.address))),
  claim: async () => null,
};

let n = 0;
async function tick() {
  n++;
  const r = await runCycle({
    cfg, fees: balanceAdapter, quoter: new AggregatorQuoter(),
    holders: () => snapshotHolders(conn, cfg.distribution.token_mint),
    publish: httpPublisher(), log: console.log, source: "automation", simulated: false, cycleNo: n,
  }).catch((e) => { console.error("[loop]  cycle failed:", e instanceof Error ? e.message : e); return null; });
  console.log(`[loop]  cycle ${String(n).padStart(4, "0")} ${r?.status ?? "error"}`);
}

await tick();
if (!process.argv.includes("--once")) setInterval(tick, cfg.cycle.interval_seconds * 1000);
