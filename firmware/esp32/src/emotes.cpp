// Emote renderer for the rev A body. Must stay in sync with EMOTE_SUMMARY in
// packages/protocol/src/index.ts. Everything here is non-blocking.
#include "emotes.h"
#include "pins.h"
#include <Wire.h>
#include <FastLED.h>
#include <Adafruit_PWMServoDriver.h>

static CRGB eyes[EYE_PIXELS];
static CRGB base[BASE_PIXELS];
static Adafruit_PWMServoDriver pwm(PCA9685_ADDR);

static Emote cur = Emote::OFFLINE;
static uint8_t level = 60;
static uint32_t started = 0;

// servo helpers: pulse in microseconds, clamped to a safe range for SG90/MG90S class servos
static void servoUs(uint8_t ch, int us) {
  us = constrain(us, 700, 2300);
  pwm.writeMicroseconds(ch, us);
}
static int deg(int d) { return map(constrain(d, 0, 180), 0, 180, 700, 2300); }

static const CRGB EYE_RED = CRGB(255, 30, 10);
static const CRGB PHOS    = CRGB(160, 255, 60);
static const CRGB AMBER   = CRGB(255, 150, 20);

Emote emoteFromString(const char* s) {
  if (!strcmp(s, "WAKE")) return Emote::WAKE;
  if (!strcmp(s, "FEED")) return Emote::FEED;
  if (!strcmp(s, "ROUTE")) return Emote::ROUTE;
  if (!strcmp(s, "CRUNCH")) return Emote::CRUNCH;
  if (!strcmp(s, "PAYOUT")) return Emote::PAYOUT;
  if (!strcmp(s, "HALT")) return Emote::HALT;
  return Emote::IDLE;
}

const char* emoteName(Emote e) {
  static const char* n[] = {"IDLE", "WAKE", "FEED", "ROUTE", "CRUNCH", "PAYOUT", "HALT", "OFFLINE"};
  return n[(uint8_t)e];
}

void bodyBegin() {
  Wire.begin(PIN_I2C_SDA, PIN_I2C_SCL);
  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(SERVO_FREQ_HZ);
  FastLED.addLeds<WS2812B, PIN_EYE_DATA, GRB>(eyes, EYE_PIXELS);
  FastLED.addLeds<WS2812B, PIN_BASE_DATA, GRB>(base, BASE_PIXELS);
  FastLED.setMaxPowerInVoltsAndMilliamps(5, 1500);   // LED budget, servos are on their own rail
  pinMode(PIN_STATUS_LED, OUTPUT);
  pinMode(PIN_PIEZO, OUTPUT);
  bodyPlay(Emote::OFFLINE, 40);
}

void bodyPlay(Emote e, uint8_t intensity) {
  cur = e;
  level = intensity;
  started = millis();
  if (e == Emote::CRUNCH) tone(PIN_PIEZO, 1800, 60);
  if (e == Emote::PAYOUT) tone(PIN_PIEZO, 2400, 120);
  if (e == Emote::HALT)   tone(PIN_PIEZO, 400, 400);
}

static void fillEyes(CRGB c, uint8_t b) { for (auto& p : eyes) p = c; for (auto& p : eyes) p.nscale8(b); }

void bodyTick(uint32_t now) {
  const uint32_t t = now - started;
  const float s = t / 1000.0f;
  const uint8_t breathe = 40 + (uint8_t)(sin8((now / 12) & 0xFF) / 4);
  digitalWrite(PIN_STATUS_LED, cur == Emote::OFFLINE ? ((now / 800) & 1) : HIGH);

  switch (cur) {
    case Emote::OFFLINE:  // no backend: slow amber blink, eyes low, parked
      fillEyes(EYE_RED, 20);
      fill_solid(base, BASE_PIXELS, ((now / 800) & 1) ? AMBER : CRGB::Black);
      for (auto& p : base) p.nscale8(40);
      servoUs(CH_HEAD_TILT, deg(80));
      break;

    case Emote::IDLE:     // eyes breathe, dim wave, micro sway
      fillEyes(EYE_RED, scale8(breathe, level + 60));
      for (int i = 0; i < BASE_PIXELS; i++) base[i] = PHOS, base[i].nscale8(sin8(i * 16 + now / 10) / 8);
      servoUs(CH_HEAD_TILT, deg(90 + (int)(3 * sinf(s * 0.8f))));
      servoUs(CH_ARM_L, deg(90)); servoUs(CH_ARM_R, deg(90));
      break;

    case Emote::WAKE:     // eyes ramp, sweep, stand
      fillEyes(EYE_RED, min<uint32_t>(255, t / 6));
      fill_solid(base, BASE_PIXELS, CRGB::Black);
      base[(t / 60) % BASE_PIXELS] = PHOS;
      servoUs(CH_HEAD_TILT, deg(90));
      break;

    case Emote::FEED:     // eyes pulse, amber chase, arms grab
      fillEyes(EYE_RED, 120 + sin8(t / 3) / 2);
      fill_solid(base, BASE_PIXELS, CRGB::Black);
      for (int k = 0; k < 3; k++) base[(t / 50 + k) % BASE_PIXELS] = AMBER;
      servoUs(CH_ARM_L, deg(((t / 400) & 1) ? 50 : 100));
      servoUs(CH_ARM_R, deg(((t / 400) & 1) ? 130 : 80));
      break;

    case Emote::ROUTE:    // eye scan, split base, head tilt
      for (int i = 0; i < EYE_PIXELS; i++) eyes[i] = (i % EYE_PIXELS_PER_RING == (t / 70) % EYE_PIXELS_PER_RING) ? EYE_RED : CRGB(20, 2, 0);
      for (int i = 0; i < BASE_PIXELS; i++) base[i] = i < BASE_PIXELS * 8 / 10 ? PHOS : AMBER, base[i].nscale8(90);
      servoUs(CH_HEAD_TILT, deg(105));
      break;

    case Emote::CRUNCH:   // double flash, flicker, body shake
      fillEyes(EYE_RED, (t < 120 || (t > 240 && t < 360)) ? 255 : 60);
      for (auto& p : base) p = random8() > 180 ? PHOS : CRGB::Black;
      servoUs(CH_HEAD_TILT, deg(90 + (((t / 70) & 1) ? 6 : -6)));
      break;

    case Emote::PAYOUT:   // full eyes, green chase, wave, hop
      fillEyes(EYE_RED, 255);
      fill_solid(base, BASE_PIXELS, CRGB::Black);
      for (int k = 0; k < 5; k++) base[(t / 35 + k * 3) % BASE_PIXELS] = PHOS;
      servoUs(CH_ARM_R, deg(60 + (int)(40 * sinf(s * 9))));
      servoUs(CH_ARM_L, deg(120 - (int)(40 * sinf(s * 9))));
      servoUs(CH_EYE_L, deg(90 + (int)(10 * sinf(s * 6))));
      servoUs(CH_EYE_R, deg(90 - (int)(10 * sinf(s * 6))));
      break;

    case Emote::HALT:     // eyes dim, red strobe, head droop
      fillEyes(EYE_RED, 25);
      fill_solid(base, BASE_PIXELS, ((now / 150) & 1) ? CRGB::Red : CRGB::Black);
      servoUs(CH_HEAD_TILT, deg(60));
      servoUs(CH_ARM_L, deg(140)); servoUs(CH_ARM_R, deg(40));
      break;
  }
  FastLED.show();
}
