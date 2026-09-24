import type { Quote, Quoter } from "./quoter.js";

/** Deterministic quoter: outAmount = amount * rate. No network. */
export class MockQuoter implements Quoter {
  constructor(private readonly rate: bigint = 1n) {}
  async quote(inputMint: string, outputMint: string, amount: bigint, slippageBps: number): Promise<Quote> {
    return { inputMint, outputMint, inAmount: amount, outAmount: amount * this.rate, slippageBps, routeLabel: "mock" };
  }
}
