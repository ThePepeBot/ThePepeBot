import { test } from "node:test";
import assert from "node:assert/strict";
import { planDistribution } from "../src/distributor/plan.js";

const h = (owner: string, amount: bigint, program = false) => ({ owner, amount, program });

test("pro-rata with exclusions, min balance and carry", () => {
  const plan = planDistribution({
    holders: [h("a", 300n), h("b", 100n), h("lp", 10_000n), h("pda", 5_000n, true), h("tiny", 5n)],
    total: 1000n, minBalance: 10n, minPayout: 1n,
    exclude: new Map([["lp", "lp"]]),
  });
  assert.equal(plan.eligible, 2);
  assert.deepEqual(plan.excluded, { lp: 1, programs: 1 });
  assert.equal(plan.belowMin, 1);
  assert.deepEqual(plan.payouts, [{ owner: "a", amount: 750n }, { owner: "b", amount: 250n }]);
  assert.equal(plan.carried, 0n);
});

test("sub-min payouts are carried, never rounded up", () => {
  const plan = planDistribution({
    holders: [h("a", 999n), h("b", 1n)], total: 100n, minBalance: 0n, minPayout: 5n, exclude: new Map(),
  });
  assert.deepEqual(plan.payouts, [{ owner: "a", amount: 99n }]);
  assert.equal(plan.carried, 1n);
});

test("empty treasury -> empty plan", () => {
  const plan = planDistribution({ holders: [h("a", 1n)], total: 0n, minBalance: 0n, minPayout: 1n, exclude: new Map() });
  assert.equal(plan.payouts.length, 0);
});
