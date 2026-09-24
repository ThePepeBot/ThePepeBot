# Asset modules

Code: `automation/src/assets/`. Config: `assets.modules` in `config/allocation.example.yaml`.

The assets share of each cycle is split across modules by `weight_bps`. Each module must answer three questions:

```ts
interface AssetModule {
  eligibility(): { ok: true } | { ok: false; reason: string }; // may the treasury buy this at all?
  distributable(): boolean;                                     // may it go to arbitrary holders?
  quote(budget, quoter, slippageBps): Promise<{ outAmount; route }>;
}
```

A module that is not eligible **does not spend**. Its share stays in the treasury.

| module | kind | status |
|---|---|---|
| `spl-token` | any freely transferable SPL token, bought via aggregator quote | built (quote only) |
| `tokenized-equity` | tokenized stocks / RWAs | **always GATED** in this build |

## Tokenized equities

These are not ordinary tokens. Depending on the issuer they may:

- be unavailable in some jurisdictions, for the treasury operator or for recipients
- require KYC, accreditation or allowlisting of every receiving wallet
- restrict transfers at the token-program level
- have provider-specific redemption and corporate-action rules

So PepeBot never assumes every holder can receive every asset. A real tokenized-equity module needs a
provider adapter that encodes that provider's rules, and a per-recipient eligibility check before a
distribution plan can include it. Until someone writes and reviews one, the module reports
`no provider adapter / eligibility unresolved` and skips.

## Adding a module

1. Implement `AssetModule` in `automation/src/assets/modules/`.
2. Register its `kind` in `assets/registry.ts` and the zod schema in `config.ts`.
3. Add it to the config with a weight. Weights must sum to 10000.
4. Run `npm run sim` and `npm test`.
