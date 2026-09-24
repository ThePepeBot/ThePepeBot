import type { ModuleConfig } from "../config.js";
import type { AssetModule, ModuleFactory } from "./module.js";
import { SplTokenModule } from "./modules/splToken.js";
import { TokenizedEquityModule } from "./modules/tokenizedEquity.js";

const FACTORIES: Record<ModuleConfig["kind"], ModuleFactory> = {
  "spl-token": (c) => new SplTokenModule(c),
  "tokenized-equity": (c) => new TokenizedEquityModule(c),
};

export function buildModules(cfgs: ModuleConfig[]): AssetModule[] {
  return cfgs.map((c) => FACTORIES[c.kind](c));
}
