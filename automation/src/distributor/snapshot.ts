import { Connection, PublicKey } from "@solana/web3.js";

export interface Holder { owner: string; amount: bigint; program: boolean }

const TOKEN_PROGRAMS = [
  "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
  "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb",
];

/**
 * Read every token account for `mint` (classic + Token-2022), aggregate by owner.
 * Owners that are not on the ed25519 curve are PDAs (pools, vaults, programs) and
 * are flagged so the planner can exclude them.
 */
export async function snapshotHolders(conn: Connection, mint: string): Promise<Holder[]> {
  const byOwner = new Map<string, bigint>();
  for (const program of TOKEN_PROGRAMS) {
    const accts = await conn.getParsedProgramAccounts(new PublicKey(program), {
      filters: [{ memcmp: { offset: 0, bytes: mint } }],
    });
    for (const a of accts) {
      const info = (a.account.data as { parsed?: { info?: { owner: string; tokenAmount: { amount: string } } } }).parsed?.info;
      if (!info) continue;
      byOwner.set(info.owner, (byOwner.get(info.owner) ?? 0n) + BigInt(info.tokenAmount.amount));
    }
  }
  return [...byOwner].map(([owner, amount]) => ({
    owner, amount, program: !PublicKey.isOnCurve(new PublicKey(owner).toBytes()),
  }));
}
