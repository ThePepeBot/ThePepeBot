import { test } from "node:test";
import assert from "node:assert/strict";
import { makeEvent } from "@pepebot/protocol";
import { EmoteEngine } from "../../backend/src/emote/engine.js";

test("halt is sticky until resume", () => {
  let t = 0;
  const eng = new EmoteEngine(() => t);
  assert.equal(eng.handle(makeEvent("guard.halt", "operator", false, {}))?.emote, "HALT");
  t += 10_000;
  assert.equal(eng.handle(makeEvent("dist.completed", "sim", true, {})), null);
  assert.equal(eng.handle(makeEvent("guard.resume", "operator", false, {}))?.emote, "WAKE");
});

test("higher priority emote is not interrupted, cooldown drops chatter", () => {
  let t = 0;
  const eng = new EmoteEngine(() => t);
  assert.equal(eng.handle(makeEvent("dist.completed", "sim", true, {}))?.emote, "PAYOUT");
  t += 100;
  assert.equal(eng.handle(makeEvent("fee.accrued", "sim", true, {})), null);
  t += 6000;
  assert.equal(eng.handle(makeEvent("fee.accrued", "sim", true, {}))?.emote, "FEED");
  t += 100;
  assert.equal(eng.handle(makeEvent("fee.accrued", "sim", true, {})), null);
});

test("frames carry the simulated flag", () => {
  const eng = new EmoteEngine(() => 0);
  assert.equal(eng.handle(makeEvent("fee.collected", "sim", true, {}))?.simulated, true);
});
