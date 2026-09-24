import { Connection, LAMPORTS_PER_SOL, PublicKey } from "@solana/web3.js";
import { makeEvent } from "@pepebot/protocol";
import type { EventBus } from "../bus.js";

/**
 * Watches the treasury account over the RPC websocket.
 * Any SOL balance increase is published as fee.accrued (simulated: false).
 * This only observes; it never signs anything.
 */
export function watchTreasury(bus: EventBus, rpcUrl: string, wsUrl: string | undefined, treasury: string) {
  const conn = new Connection(rpcUrl, { commitment: "confirmed", wsEndpoint: wsUrl });
  const key = new PublicKey(treasury);
  let last: number | null = null;

  conn.getBalance(key).then((b) => { last = b; console.log(`[chain] treasury ${treasury} ${(b / LAMPORTS_PER_SOL).toFixed(4)} SOL`); });

  const sub = conn.onAccountChange(key, (info, ctx) => {
    const now = info.lamports;
    if (last !== null && now > last) {
      bus.publish(makeEvent("fee.accrued", "chain", false, {
        lamports: String(now - last), slot: ctx.slot, treasury,
      }));
    }
    last = now;
  });
  return () => conn.removeAccountChangeListener(sub);
}

/**
 * Minimal adapter for "enhanced transaction" style webhooks (array of txs with nativeTransfers).
 * Providers differ; adapt parseWebhook() to yours.
 */
export function parseWebhook(body: unknown, treasury: string): bigint {
  if (!Array.isArray(body)) return 0n;
  let total = 0n;
  for (const tx of body) {
    const transfers = (tx as { nativeTransfers?: { toUserAccount?: string; amount?: number }[] }).nativeTransfers ?? [];
    for (const t of transfers) if (t.toUserAccount === treasury && typeof t.amount === "number") total += BigInt(t.amount);
  }
  return total;
}
