import { LiveExecutionDisabled, type FeeAdapter } from "./adapter.js";

/** Returns a fixed synthetic claimable amount. Used by the simulator and tests. */
export class MockFeeAdapter implements FeeAdapter {
  readonly id = "adapter:mock";
  constructor(readonly venue: string, private readonly lamports: bigint) {}
  async claimable() { return this.lamports; }
  async claim(dryRun: boolean) {
    if (!dryRun) throw new LiveExecutionDisabled("MockFeeAdapter.claim");
    return null;
  }
}
