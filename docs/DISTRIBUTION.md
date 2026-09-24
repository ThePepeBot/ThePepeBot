# Distribution

Code: `automation/src/distributor/`. Tests: `automation/test/plan.test.ts`.

1. **Snapshot.** Every token account for the PEPEBOT mint (classic + Token-2022), aggregated by owner.
2. **Exclude.** Configured addresses (LP vaults, burn, treasury) and any off-curve owner (PDAs: pools, programs).
3. **Min balance.** Holders below `distribution.min_balance` are skipped this cycle.
4. **Pro-rata.** `payout = floor(total × balance / eligible_supply)`, integer math.
5. **Min payout.** Amounts below `min_payout` are not sent. Rounding and dust are **carried** in the treasury to the next cycle.
6. **Batch.** Payouts chunked by `batch_size`. Sending: PLANNED (multisig-signed SPL transfers, later possibly the merkle claim in `contracts/`).

What this does **not** do:

- It does not promise anyone a payout. If fees are zero, the plan is empty.
- It does not send restricted assets (see [ASSET-MODULES.md](ASSET-MODULES.md)). Only modules that report `distributable() === true` enter the plan.
- Snapshot timing is a known design question (single snapshot vs. time-weighted). v1 uses a single snapshot per cycle; this is gameable around the snapshot and is documented as a limitation.
