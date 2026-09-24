import { LiveExecutionDisabled } from "../fees/adapter.js";
import type { Quote, Quoter } from "./quoter.js";

/**
 * Fetches quotes from a Jupiter-style aggregator quote endpoint (SWAP_QUOTE_URL).
 * Quote only: building, signing and sending the swap is intentionally not implemented.
 */
export class AggregatorQuoter implements Quoter {
  constructor(private readonly url = process.env.SWAP_QUOTE_URL ?? "https://lite-api.jup.ag/swap/v1/quote") {}

  async quote(inputMint: string, outputMint: string, amount: bigint, slippageBps: number): Promise<Quote> {
    const q = new URL(this.url);
    q.searchParams.set("inputMint", inputMint);
    q.searchParams.set("outputMint", outputMint);
    q.searchParams.set("amount", amount.toString());
    q.searchParams.set("slippageBps", String(slippageBps));
    const res = await fetch(q, { signal: AbortSignal.timeout(8000) });
    if (!res.ok) throw new Error(`quote http ${res.status}`);
    const j = (await res.json()) as { outAmount?: string; routePlan?: Array<{ swapInfo?: { label?: string } }> };
    if (!j.outAmount) throw new Error("quote: no outAmount");
    return {
      inputMint, outputMint, inAmount: amount, outAmount: BigInt(j.outAmount), slippageBps,
      routeLabel: j.routePlan?.map((r) => r.swapInfo?.label ?? "?").join(">") ?? "unknown",
    };
  }
}

export async function executeSwap(_q: Quote): Promise<string> {
  throw new LiveExecutionDisabled("executeSwap");
}
