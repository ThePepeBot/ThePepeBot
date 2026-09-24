import type { Holder } from "./snapshot.js";

export interface PlanInput {
  holders: Holder[];
  total: bigint;                  // amount of the payout asset available
  minBalance: bigint;
  minPayout: bigint;
  exclude: Map<string, string>;   // address -> label
}

export interface Payout { owner: string; amount: bigint }

export interface Plan {
  payouts: Payout[];
  eligible: number;
  excluded: Record<string, number>;
  belowMin: number;
  carried: bigint;                // rounding + dust, stays in treasury for next cycle
}

/**
 * Pro-rata by balance among eligible holders. Floor division; everything that
 * does not reach a holder (rounding, sub-min_payout dust) is carried.
 * No holder is promised any amount: if total is 0 the plan is empty.
 */
export function planDistribution(p: PlanInput): Plan {
  const excluded: Record<string, number> = {};
  let belowMin = 0;
  const eligible: Holder[] = [];
  for (const h of p.holders) {
    const label = p.exclude.get(h.owner) ?? (h.program ? "programs" : null);
    if (label) { excluded[label] = (excluded[label] ?? 0) + 1; continue; }
    if (h.amount < p.minBalance) { belowMin++; continue; }
    eligible.push(h);
  }
  const weight = eligible.reduce((s, h) => s + h.amount, 0n);
  const payouts: Payout[] = [];
  let paid = 0n;
  if (weight > 0n && p.total > 0n) {
    for (const h of eligible) {
      const amt = (p.total * h.amount) / weight;
      if (amt >= p.minPayout && amt > 0n) { payouts.push({ owner: h.owner, amount: amt }); paid += amt; }
    }
  }
  return { payouts, eligible: eligible.length, excluded, belowMin, carried: p.total - paid };
}
