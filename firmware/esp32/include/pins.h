#pragma once
// Rev A pin map. Must match hardware/README.md and assets/readme/hardware.svg.

#define PIN_I2C_SDA     8    // -> PCA9685 SDA
#define PIN_I2C_SCL     9    // -> PCA9685 SCL
#define PIN_EYE_DATA    5    // -> 74AHCT125 -> WS2812 eye rings (L then R, chained)
#define PIN_BASE_DATA   6    // -> 74AHCT125 -> WS2812 base strip
#define PIN_STATUS_LED  4    // panel status lamp (via transistor)
#define PIN_PIEZO       7    // piezo buzzer

#define PCA9685_ADDR    0x40
#define SERVO_FREQ_HZ   50

// PCA9685 channels
#define CH_EYE_L        0
#define CH_EYE_R        1
#define CH_ARM_L        2
#define CH_ARM_R        3
#define CH_HEAD_TILT    4

#define EYE_PIXELS_PER_RING 12
#define EYE_PIXELS      (EYE_PIXELS_PER_RING * 2)
#define BASE_PIXELS     16
