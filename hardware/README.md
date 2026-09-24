# hardware / rev A

The body. An ESP32-S3 that listens to the backend and turns loop events into light and motion.
It is an output device only: no keys, no wallet, no way to move funds.

![rev A](../assets/readme/hardware.svg)

## BOM (rev A, proposed)

| qty | part | note |
|---:|---|---|
| 1 | ESP32-S3 DevKitC-1 | wifi, websocket client |
| 1 | PCA9685 16-ch PWM board | I2C 0x40, drives all servos |
| 5 | MG90S micro servo | eye stalk L/R, arm L/R, head tilt |
| 2 | WS2812B ring, 12 px | eyes, chained L then R |
| 1 | WS2812B strip, 16 px | base ring |
| 1 | 74AHCT125 | 3.3 V to 5 V level shift for both LED data lines |
| 1 | 5 V 6 A supply | servos + LEDs, separate from ESP32 USB |
| 1 | 1000 µF 10 V electrolytic | across 5 V rail at LED input |
| 1 | inline fuse, 5 A | on the 5 V rail |
| 1 | piezo buzzer | GPIO7 |
| 1 | 5 mm panel lamp + NPN | status, GPIO4 |
| - | shell | enclosure CAD planned, see `cad/` |

## Pinout

Source of truth: `firmware/esp32/include/pins.h`.

| signal | ESP32-S3 | goes to |
|---|---|---|
| I2C SDA | GPIO8 | PCA9685 SDA |
| I2C SCL | GPIO9 | PCA9685 SCL |
| EYE DATA | GPIO5 | 74AHCT125 → eye ring L → eye ring R (24 px) |
| BASE DATA | GPIO6 | 74AHCT125 → base strip (16 px) |
| STATUS | GPIO4 | NPN → panel lamp |
| PIEZO | GPIO7 | piezo |

| PCA9685 ch | servo |
|---|---|
| CH0 | eye stalk L |
| CH1 | eye stalk R |
| CH2 | arm L |
| CH3 | arm R |
| CH4 | head tilt |

## Power

- Servos and LEDs run from the 5 V 6 A rail. **Never power servos from the ESP32 3V3 pin.**
- Common ground between the 5 V rail, PCA9685 and ESP32.
- 1000 µF cap across the rail at the LED input, fuse on the rail.
- Firmware caps LED draw at 1.5 A (`FastLED.setMaxPowerInVoltsAndMilliamps`).
- Legs are passive springs. No actuators below the base.

## Status

Wiring and firmware are rev A drafts. Enclosure, PCB and a tested power budget are planned.
