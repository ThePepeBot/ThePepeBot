# firmware/esp32

Rev A body firmware. PlatformIO, Arduino framework, ESP32-S3.

```
cp include/config.example.h include/config.h   # wifi, gateway host, BOT_TOKEN
pio run -t upload && pio device monitor
```

| file | does |
|---|---|
| `include/pins.h` | pin map (matches `hardware/README.md`) |
| `src/main.cpp` | wifi, websocket link to `backend` `/bot`, hello/ack/telemetry, ttl fallback |
| `src/emotes.cpp` | the 7 emotes + OFFLINE, non-blocking LED/servo animation |

Status: written against the protocol in `packages/protocol`. **Not yet compiled in CI and not yet validated on rev A hardware.**
Servo angles are starting points; tune them to your linkage before running arms at full travel.

The bot is output-only. It never holds keys and has no path to move funds.
