import { test } from "node:test";
import assert from "node:assert/strict";
import { allocate, distributable, splitWeighted } from "../src/router/allocate.js";

test("allocate splits by bps and never loses a lamport", () => {
  const s = allocate(12_450_000_000n, 8000);
  assert.equal(s.pepe, 9_960_000_000n);
  assert.equal(s.assets, 2_490_000_000n);
  for (const n of [0n, 1n, 7n, 999_999_999n]) {
    const r = allocate(n, 3333);
    assert.equal(r.pepe + r.assets, n);
  }
});

test("allocate rejects bad input", () => {
  assert.throws(() => allocate(-1n, 5000));
  assert.throws(() => allocate(1n, 10_001));
});

test("distributable applies reserve then cap", () => {
  assert.equal(distributable(12_500_000_000n, 50_000_000n, 100_000_000_000n), 12_450_000_000n);
  assert.equal(distributable(10n, 50n, 1000n), 0n);
  assert.equal(distributable(10_000n, 0n, 500n), 500n);
});

test("splitWeighted gives dust to the last module", () => {
  const parts = splitWeighted(101n, [{ weight_bps: 5000 }, { weight_bps: 5000 }]);
  assert.deepEqual(parts.map(([, v]) => v), [50n, 51n]);
});
