---
## EspressifSystems/esp-drone [MODIFIÉ]
**Type:** Application
**Domain:** Edge AI
**Relevance score:** 73/100
**Problem solved:** Provide a Wi-Fi-controlled quadcopter firmware stack for ESP32/ESP32-S2/ESP32-S3 microcontrollers, enabling flight stabilization and position-hold modes without proprietary drone platforms. Ported from Crazyflie to reduce development friction for educational and hobbyist UAV projects.
**How it works:** Core flight control logic (stabilization, height-hold, position-hold) ported from Crazyflie firmware (GPL 3.0); runs on ESP-IDF v5.0 (Espressif's FreeRTOS-based framework). Hardware targets ESP32, ESP32-S2, ESP32-S3 SoCs with Wi-Fi radio; control via mobile apps (iOS/Android) or cfclient Python client over Wi-Fi, or ESP-NOW protocol from ESP-BOX3 joystick. Includes DSP library (esp32-lin) for sensor fusion and motor control.
**Chinese specificity:** Developed and maintained by Espressif Systems (Shanghai), the manufacturer of ESP32 SoCs; official Gitee mirror synchronized from GitHub. Leverages Espressif's ESP-IDF ecosystem and hardware platform as the sole target architecture.
**Western equivalent:** Crazyflie firmware (Bitcraze), ArduCopter (ArduPilot), PX4 autopilot
**Maturity:** Active (★ 64, 21 forks, updated 2026-06)
**Language:** Bilingual CN-EN
**Gitee:** https://gitee.com/EspressifSystems/esp-drone
---
