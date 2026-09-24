import type { SystemEvent } from "@pepebot/protocol";

export type Publisher = (e: SystemEvent) => Promise<void>;

/** POST events to the backend (which turns them into robot emotes). Never throws. */
export function httpPublisher(url = process.env.BACKEND_URL, token = process.env.INGEST_TOKEN): Publisher {
  if (!url) return async () => {};
  return async (e) => {
    try {
      await fetch(new URL("/events", url), {
        method: "POST",
        headers: { "content-type": "application/json", authorization: `Bearer ${token ?? ""}` },
        body: JSON.stringify(e),
        signal: AbortSignal.timeout(3000),
      });
    } catch {
      /* backend offline: the loop does not depend on the robot */
    }
  };
}
