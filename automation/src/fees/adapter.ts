/**
 * A FeeAdapter knows how to see (and eventually claim) the trading fees owed
 * to the treasury on a given venue. Venue-specific adapters are NOT included:
 * which launchpad / AMM PEPEBOT trades on decides how fees are claimed.
 */
export interface FeeAdapter {
  readonly id: string;
  readonly venue: string;
  /** lamports currently claimable by the treasury */
  claimable(): Promise<bigint>;
  /** claim fees into the treasury. Returns a signature, or null when dry-run. */
  claim(dryRun: boolean): Promise<string | null>;
}

export class LiveExecutionDisabled extends Error {
  constructor(what: string) {
    super(`${what}: live execution is not implemented in this build (dry-run only)`);
  }
}
