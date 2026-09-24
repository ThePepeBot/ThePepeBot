import type { ModuleConfig } from "../../config.js";
import { WSOL, type Quoter } from "../../swap/quoter.js";
import type { AssetModule } from "../module.js";

/** Plain SPL token bought with SOL through the quoter. Freely transferable. */
export class SplTokenModule implements AssetModule {
  readonly kind = "spl-token" as const;
  readonly id: string;
  constructor(private readonly cfg: ModuleConfig) { this.id = cfg.id; }
  eligibility() {
    if (!this.cfg.enabled) return { ok: false as const, reason: "disabled" };
    if (!this.cfg.mint || this.cfg.mint.startsWith("REPLACE_")) return { ok: false as const, reason: "mint not configured" };
    return { ok: true as const };
  }
  distributable() { return true; }
  async quote(budget: bigint, quoter: Quoter, slippageBps: number) {
    const q = await quoter.quote(WSOL, this.cfg.mint!, budget, slippageBps);
    return { outAmount: q.outAmount, route: q.routeLabel };
  }
}
