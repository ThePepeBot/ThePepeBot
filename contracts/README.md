# contracts

**v1 needs no custom program.** Distributions are plain SPL token transfers, batched,
signed by the treasury multisig. Custom code onchain is attack surface, so it is deferred
until the transfer approach stops scaling.

| path | status |
|---|---|
| treasury | multisig (e.g. Squads). Operators approve spends. PLANNED, not configured in this repo |
| batch transfers | `automation/src/distributor` builds the plan; sending is PLANNED |
| `programs/pepebot-distributor` | **DRAFT. NOT AUDITED. NOT DEPLOYED.** Merkle-claim distributor spec |

## Proposed merkle-claim distributor

When holder count makes push transfers expensive, switch to pull:

1. automation computes the pro-rata plan (same `planDistribution`) for epoch *n*
2. leaves = `hash(epoch, holder, mint, amount)`; root posted by the multisig with the funded vault
3. holders claim with a proof; a claim-receipt PDA per `(epoch, holder)` blocks double claims
4. unclaimed balance after the window returns to the treasury for a later epoch

Only assets that are freely transferable to arbitrary wallets can go through this path.
Tokenized equities or any restricted asset need provider-side eligibility and are out of scope here.

Nothing in this folder should be deployed without an independent audit.
