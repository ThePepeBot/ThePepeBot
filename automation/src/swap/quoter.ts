export interface Quote {
  inputMint: string;
  outputMint: string;
  inAmount: bigint;
  outAmount: bigint;
  slippageBps: number;
  routeLabel: string;
}

export interface Quoter {
  quote(inputMint: string, outputMint: string, amount: bigint, slippageBps: number): Promise<Quote>;
}

export const WSOL = "So11111111111111111111111111111111111111112";
