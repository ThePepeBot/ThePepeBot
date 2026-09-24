import type { ModuleConfig } from "../config.js";
import type { Quoter } from "../swap/quoter.js";

export type Eligibility = { ok: true } | { ok: false; reason: string };

/**
 * An AssetModule turns a SOL budget into some onchain asset held by the treasury.
 * Each module declares its own eligibility gate. A gated module never spends:
 * its share stays in the treasury.
 *
 * Tokenized equities in particular can carry provider, jurisdiction, transfer and
 * holder-eligibility restrictions. A module for them must encode those rules
 * itself; the distributor never assumes every holder may receive every asset.
 */
export interface AssetModule {
  readonly id: string;
  readonly kind: ModuleConfig["kind"];
  eligibility(): Eligibility;
  /** Can the acquired asset be distributed to arbitrary holders? */
  distributable(): boolean;
  quote(budget: bigint, quoter: Quoter, slippageBps: number): Promise<{ outAmount: bigint; route: string }>;
}

export type ModuleFactory = (cfg: ModuleConfig) => AssetModule;
