// PepeBot rev A firmware
//   WiFi -> websocket client -> ws://GATEWAY_HOST:GATEWAY_PORT/bot
//   sends hello {botId, fw, token}, receives EmoteFrame JSON, acks by seq,
//   falls back to IDLE when a frame's ttl expires, shows OFFLINE when the link drops.
// The robot is an output device. It holds no keys and cannot move funds.
#include <Arduino.h>
#include <WiFi.h>
#include <WebSocketsClient.h>
#include <ArduinoJson.h>
#include "config.h"
#include "emotes.h"

#ifndef PEPEBOT_FW
#define PEPEBOT_FW "dev"
#endif

static WebSocketsClient ws;
static bool linked = false;
static uint32_t ttlUntil = 0;       // 0 = sticky (e.g. HALT)
static bool sticky = false;
static uint32_t lastTelemetry = 0;

static void sendJson(JsonDocument& d) {
  String out;
  serializeJson(d, out);
  ws.sendTXT(out);
}

static void onFrame(const char* payload, size_t len) {
  JsonDocument d;
  if (deserializeJson(d, payload, len)) return;
  const char* t = d["t"] | "";
  if (strcmp(t, "emote") != 0 || (d["v"] | 0) != 1) return;

  Emote e = emoteFromString(d["emote"] | "IDLE");
  uint8_t intensity = d["intensity"] | 128;
  uint32_t ttl = d["ttlMs"] | 0;
  bodyPlay(e, intensity);
  sticky = (ttl == 0 && e != Emote::IDLE);
  ttlUntil = ttl ? millis() + ttl : 0;

  JsonDocument ack;
  ack["t"] = "ack";
  ack["seq"] = d["seq"] | 0;
  sendJson(ack);
  Serial.printf("[bot] emote -> %s (%s)%s\n", emoteName(e), (const char*)(d["reason"] | "?"),
                (d["simulated"] | false) ? " SIM" : "");
}

static void onWs(WStype_t type, uint8_t* payload, size_t len) {
  switch (type) {
    case WStype_CONNECTED: {
      linked = true;
      JsonDocument h;
      h["t"] = "hello"; h["botId"] = BOT_ID; h["fw"] = PEPEBOT_FW; h["token"] = BOT_TOKEN;
      sendJson(h);
      bodyPlay(Emote::WAKE, 200);
      ttlUntil = millis() + 3000;
      Serial.println("[link] connected");
      break;
    }
    case WStype_DISCONNECTED:
      if (linked) Serial.println("[link] lost");
      linked = false;
      sticky = false;
      bodyPlay(Emote::OFFLINE, 40);
      break;
    case WStype_TEXT:
      onFrame((const char*)payload, len);
      break;
    default:
      break;
  }
}

void setup() {
  Serial.begin(115200);
  bodyBegin();
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.printf("[boot] PepeBot fw %s  bot=%s\n", PEPEBOT_FW, BOT_ID);
  ws.begin(GATEWAY_HOST, GATEWAY_PORT, GATEWAY_PATH);
  ws.onEvent(onWs);
  ws.setReconnectInterval(3000);
  ws.enableHeartbeat(15000, 3000, 2);
}

void loop() {
  ws.loop();
  const uint32_t now = millis();
  if (linked && !sticky && ttlUntil && (int32_t)(now - ttlUntil) > 0) {
    bodyPlay(Emote::IDLE, 60);
    ttlUntil = 0;
  }
  if (linked && now - lastTelemetry > 30000) {
    lastTelemetry = now;
    JsonDocument t;
    t["t"] = "telemetry"; t["rssi"] = WiFi.RSSI(); t["uptimeS"] = now / 1000; t["heapFree"] = ESP.getFreeHeap();
    sendJson(t);
  }
  bodyTick(now);
  delay(10);   // ~100 fps is plenty for LEDs and servos
}
