import { createServer, type IncomingMessage } from "node:http";
import { isSystemEvent, makeEvent } from "@pepebot/protocol";
import type { EventBus } from "../bus.js";
import type { BotGateway } from "../bridge/gateway.js";
import type { EmoteEngine } from "../emote/engine.js";
import { parseWebhook } from "../chain/listener.js";

async function readJson(req: IncomingMessage, limit = 256 * 1024): Promise<unknown> {
  let size = 0;
  const chunks: Buffer[] = [];
  for await (const c of req) {
    size += (c as Buffer).length;
    if (size > limit) throw new Error("payload too large");
    chunks.push(c as Buffer);
  }
  return JSON.parse(Buffer.concat(chunks).toString() || "null");
}

export function startHttp(opts: {
  port: number; ingestToken: string; treasury?: string;
  bus: EventBus; gateway: BotGateway; engine: EmoteEngine;
}) {
  const { bus, gateway, engine } = opts;
  const server = createServer(async (req, res) => {
    const send = (code: number, body: unknown) => {
      res.writeHead(code, { "content-type": "application/json" });
      res.end(JSON.stringify(body));
    };
    try {
      if (req.method === "GET" && req.url === "/health") return send(200, { ok: true });
      if (req.method === "GET" && req.url === "/status") {
        return send(200, { bots: gateway.status(), emote: engine.snapshot(), recent: bus.recent() });
      }
      const authed = req.headers.authorization === `Bearer ${opts.ingestToken}`;
      if (req.method === "POST" && req.url === "/events") {
        if (!authed) return send(401, { error: "unauthorized" });
        const body = await readJson(req);
        const list = Array.isArray(body) ? body : [body];
        const ok = list.filter(isSystemEvent);
        ok.forEach((e) => bus.publish(e));
        return send(202, { accepted: ok.length, rejected: list.length - ok.length });
      }
      if (req.method === "POST" && req.url === "/webhooks/chain") {
        if (!authed) return send(401, { error: "unauthorized" });
        if (!opts.treasury) return send(409, { error: "TREASURY_ADDRESS not set" });
        const lamports = parseWebhook(await readJson(req), opts.treasury);
        if (lamports > 0n) bus.publish(makeEvent("fee.accrued", "chain", false, { lamports: lamports.toString(), via: "webhook" }));
        return send(202, { lamports: lamports.toString() });
      }
      send(404, { error: "not found" });
    } catch (err) {
      send(400, { error: (err as Error).message });
    }
  });
  server.listen(opts.port, () => console.log(`[http] listening :${opts.port}`));
  return server;
}
