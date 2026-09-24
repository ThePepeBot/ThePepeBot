import { makeEvent } from "@pepebot/protocol";
import { EventBus } from "./bus.js";
import { EmoteEngine } from "./emote/engine.js";
import { BotGateway } from "./bridge/gateway.js";
import { startHttp } from "./http/server.js";
import { watchTreasury } from "./chain/listener.js";

const env = process.env;
const HTTP_PORT = Number(env.HTTP_PORT ?? 8080);
const BOT_WS_PORT = Number(env.BOT_WS_PORT ?? 8787);
const BOT_TOKEN = env.BOT_TOKEN ?? "change-me";
const INGEST_TOKEN = env.INGEST_TOKEN ?? "change-me-too";

if (BOT_TOKEN === "change-me" || INGEST_TOKEN === "change-me-too") {
  console.warn("[boot] default tokens in use. Set BOT_TOKEN and INGEST_TOKEN before exposing this service.");
}

const bus = new EventBus();
const engine = new EmoteEngine();
const gateway = new BotGateway(BOT_WS_PORT, BOT_TOKEN, () => engine.snapshot());

bus.subscribe((e) => {
  const tag = e.simulated ? "SIM " : "LIVE";
  console.log(`[bus] ${tag} ${e.type} ${JSON.stringify(e.data)}`);
  const frame = engine.handle(e);
  if (frame) {
    gateway.send(frame);
    console.log(`[bot] emote -> ${frame.emote} (${frame.reason})`);
  }
});

startHttp({ port: HTTP_PORT, ingestToken: INGEST_TOKEN, treasury: env.TREASURY_ADDRESS, bus, gateway, engine });
console.log(`[link] bot gateway ws://0.0.0.0:${BOT_WS_PORT}/bot`);

if (env.SOLANA_RPC_URL && env.TREASURY_ADDRESS) {
  watchTreasury(bus, env.SOLANA_RPC_URL, env.SOLANA_WS_URL, env.TREASURY_ADDRESS);
} else {
  console.log("[chain] TREASURY_ADDRESS not set: onchain watcher off (simulation still works)");
}

bus.publish(makeEvent("system.boot", "operator", false, { service: "backend" }));
