import type { ModuleConfig } from "../../config.js";
import type { AssetModule } from "../module.js";

/**
 * Placeholder for tokenized equities. ALWAYS GATED in this build.
 * To enable it, someone has to write a provider adapter that handles:
 *   - which instruments the provider actually offers onchain
 *   - jurisdiction rules for the treasury AND for each recipient
 *   - transfer restrictions / allowlists on the token itself
 *   - holder KYC or accreditation where required
 * Until then the module reports gated and its share stays in the treasury.
 */
export class TokenizedEquityModule implements AssetModule {
  readonly kind = "tokenized-equity" as const;
  readonly id: string;
  constructor(private readonly cfg: ModuleConfig) { this.id = cfg.id; }
  eligibility() {
    if (!this.cfg.enabled) return { ok: false as const, reason: "disabled" };
    return { ok: false as const, reason: "no provider adapter / eligibility unresolved" };
  }
  distributable() { return false; }
  async quote(): Promise<never> { throw new Error("tokenized-equity: gated"); }
}
