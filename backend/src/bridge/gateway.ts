import { WebSocketServer, WebSocket } from "ws";
import type { BotMessage, EmoteFrame } from "@pepebot/protocol";

interface BotConn { ws: WebSocket; botId: string; fw: string; alive: boolean; lastAck: number; rssi?: number }

/**
 * Websocket gateway the ESP32 connects to (ws://host:BOT_WS_PORT/bot).
 * Handshake: bot sends {t:"hello", botId, fw, token} within 5 s or is dropped.
 */
export class BotGateway {
  private wss: WebSocketServer;
  private bots = new Set<BotConn>();

  constructor(port: number, private readonly token: string, private readonly onConnect: () => EmoteFrame | null) {
    this.wss = new WebSocketServer({ port, path: "/bot" });
    this.wss.on("connection", (ws) => this.accept(ws));
    setInterval(() => this.heartbeat(), 15_000).unref();
  }

  private accept(ws: WebSocket) {
    let conn: BotConn | null = null;
    const timer = setTimeout(() => { if (!conn) ws.close(4001, "hello timeout"); }, 5000);
    ws.on("message", (raw) => {
      let msg: BotMessage;
      try { msg = JSON.parse(raw.toString()); } catch { return; }
      if (!conn) {
        if (msg.t !== "hello" || msg.token !== this.token) { ws.close(4003, "bad hello"); return; }
        clearTimeout(timer);
        conn = { ws, botId: msg.botId, fw: msg.fw, alive: true, lastAck: 0 };
        this.bots.add(conn);
        console.log(`[link] bot ${msg.botId} fw ${msg.fw} connected`);
        const replay = this.onConnect();
        if (replay) ws.send(JSON.stringify(replay));
        return;
      }
      if (msg.t === "ack") conn.lastAck = msg.seq;
      if (msg.t === "telemetry") conn.rssi = msg.rssi;
    });
    ws.on("pong", () => { if (conn) conn.alive = true; });
    ws.on("close", () => {
      clearTimeout(timer);
      if (conn) { this.bots.delete(conn); console.log(`[link] bot ${conn.botId} disconnected`); }
    });
  }

  private heartbeat() {
    for (const b of this.bots) {
      if (!b.alive) { b.ws.terminate(); this.bots.delete(b); continue; }
      b.alive = false;
      b.ws.ping();
    }
  }

  send(frame: EmoteFrame) {
    const payload = JSON.stringify(frame);
    for (const b of this.bots) if (b.ws.readyState === WebSocket.OPEN) b.ws.send(payload);
  }

  status() {
    return [...this.bots].map((b) => ({ botId: b.botId, fw: b.fw, lastAck: b.lastAck, rssi: b.rssi ?? null }));
  }
}
