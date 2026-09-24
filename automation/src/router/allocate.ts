export interface Split { pepe: bigint; assets: bigint }

/**
 * Split distributable lamports by basis points. Integer math only.
 * Rounding dust goes to the assets share so the total is always exact.
 */
export function allocate(distributable: bigint, pepeBps: number): Split {
  if (distributable < 0n) throw new Error("negative distributable");
  if (pepeBps < 0 || pepeBps > 10_000) throw new Error("pepeBps out of range");
  const pepe = (distributable * BigInt(pepeBps)) / 10_000n;
  return { pepe, assets: distributable - pepe };
}

/** Apply reserve and per-cycle cap. Returns what may be spent this cycle. */
export function distributable(claimable: bigint, reserve: bigint, cap: bigint): bigint {
  const afterReserve = claimable > reserve ? claimable - reserve : 0n;
  return afterReserve > cap ? cap : afterReserve;
}

/** Split an amount across weighted modules (weights in bps). Last module takes rounding dust. */
export function splitWeighted<T extends { weight_bps: number }>(amount: bigint, items: T[]): Array<[T, bigint]> {
  let left = amount;
  return items.map((it, i) => {
    const share = i === items.length - 1 ? left : (amount * BigInt(it.weight_bps)) / 10_000n;
    left -= share;
    return [it, share];
  });
}
