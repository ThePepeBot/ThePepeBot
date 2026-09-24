import { LiveExecutionDisabled } from "../fees/adapter.js";
import type { Payout } from "./plan.js";

export function chunk<T>(xs: T[], size: number): T[][] {
  const out: T[][] = [];
  for (let i = 0; i < xs.length; i += size) out.push(xs.slice(i, i + size));
  return out;
}

/** Sending transfer batches from the treasury multisig is planned, not implemented. */
export async function sendBatch(_batch: Payout[]): Promise<string> {
  throw new LiveExecutionDisabled("sendBatch");
}
