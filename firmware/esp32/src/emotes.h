#pragma once
#include <Arduino.h>

enum class Emote : uint8_t { IDLE, WAKE, FEED, ROUTE, CRUNCH, PAYOUT, HALT, OFFLINE };

Emote emoteFromString(const char* s);
const char* emoteName(Emote e);

void bodyBegin();
// Start an emote. intensity 0-255. Animations are non-blocking; call bodyTick() every loop.
void bodyPlay(Emote e, uint8_t intensity);
void bodyTick(uint32_t nowMs);
