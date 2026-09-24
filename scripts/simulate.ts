/**
 * npm run sim
 *
 * Runs one full cycle of the loop against SYNTHETIC data: mock fee adapter,
 * mock quoter, generated holder set. No network, no keys, nothing signed.
 * Every event is tagged simulated:true. If BACKEND_URL is set, events are also
 * posted to the backend so a connected robot reacts to the simulation.
 */
import { EMOTE_SUMMARY, makeEvent, type SystemEvent } from "@pepebot/protocol";
import { EmoteEngine } from "../backend/src/emote/engine.js";
import { loadConfig, type Config } from "../automation/src/config.js";
import { runCycle } from "../automation/src/cycle.js";
import { MockFeeAdapter } from "../automation/src/fees/mock.js";
import { MockQuoter } from "../automation/src/swap/mock.js";
import { httpPublisher } from "../automation/src/publish.js";
import type { Holder } from "../automation/src/distributor/snapshot.js";

const fast = process.argv.includes("--fast");
const sleep = (ms: number) => new Promise((r) => setTimeout(r, fast ? 0 : ms));
const log = (s: string) => console.log(s);

// ---- synthetic world -------------------------------------------------------
const base = loadConfig();
const cfg: Config = {
  ...base,
  cycle: { ...base.cycle, dry_run: true },
  pepe: { ...base.pepe, mint: "SIM_PEPE_MINT" },
  assets: { modules: base.assets.modules.map((m) => (m.kind === "spl-token" ? { ...m, mint: "SIM_LST_MINT" } : m)) },
  distribution: {
    ...base.distribution,
    exclude: [
      { label: "lp", address: "SIM_LP_A" }, { label: "lp", address: "SIM_LP_B" },
      { label: "burn", address: "SIM_BURN" }, { label: "treasury", address: "SIM_TREASURY" },
    ],
  },
  guardrails: { ...base.guardrails, kill_switch_file: "./KILL.sim-never" },
};

function syntheticHolders(): Holder[] {
  let seed = 0x9e3779b9;
  const rnd = () => ((seed = (seed * 1664525 + 1013904223) >>> 0) / 2 ** 32);
  const hs: Holder[] = [];
  for (const a of ["SIM_LP_A", "SIM_LP_B", "SIM_BURN", "SIM_TREASURY"]) hs.push({ owner: a, amount: 50_000_000_000n, program: false });
  for (let i = 0; i < 4; i++) hs.push({ owner: `SIM_PDA_${i}`, amount: 10_000_000_000n, program: true });
  for (let i = 0; i < 139; i++) hs.push({ owner: `SIM_SMALL_${i}`, amount: BigInt(1 + Math.floor(rnd() * 99_999)), program: false });
  for (let i = 0; i < 1190; i++) hs.push({ owner: `SIM_HOLDER_${i}`, amount: BigInt(100_000 + Math.floor(rnd() ** 3 * 2_000_000_000)), program: false });
  return hs;
}

// ---- robot view ------------------------------------------------------------
const engine = new EmoteEngine();
const toBackend = httpPublisher();
async function publish(e: SystemEvent) {
  await toBackend(e);
  const f = engine.handle(e);
  if (f && f.emote !== "ROUTE") log(`[bot]   emote -> ${f.emote.padEnd(8)} ${EMOTE_SUMMARY[f.emote]}`);
  await sleep(250);
}
const slowLog = (s: string) => { log(s); };

// ---- run -------------------------------------------------------------------
log("[boot]  PEPEBOT-OS 0.1 // unit 00");
log("[boot]  mode=SIMULATION  broadcast=OFF  kill_switch=SAFE");
log("[boot]  modules  fee-intake  treasury  router  pepe-swap  asset-bay  distributor");
log(`[link]  backend ${process.env.BACKEND_URL ? `${process.env.BACKEND_URL}  (events forwarded)` : "not set  (robot output printed here)"}`);
await publish(makeEvent("system.boot", "sim", true, { service: "simulator" }));
await sleep(400);

const r = await runCycle({
  cfg,
  fees: new MockFeeAdapter("PEPEBOT/SOL", 12_500_000_000n),
  quoter: new MockQuoter(1n),
  holders: async () => syntheticHolders(),
  publish, log: slowLog, source: "sim", simulated: true, cycleNo: 1,
});

log(`[loop]  cycle 0001 ${r.status === "done" ? "complete" : r.status}  //  next cycle in ${cfg.cycle.interval_seconds}s`);
log("[loop]  all numbers above are synthetic. nothing was signed or sent.");
log("[loop]  HOLD PEPEBOT. RECEIVE PEPE.");
