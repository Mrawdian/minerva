---
## EspressifSystems/esp-skainet
**Type:** Framework
**Domain:** Embedded
**Relevance score:** 67/100
**Problem solved:** Provide a complete solution for wake-word keyword recognition and offline voice commands on ESP32 microcontrollers with low memory consumption and reduced latency.
**How it works:** ESP-Skainet integrates two voice processing engines: WakeNet for wake-word keyword detection (Alexa, 天猫精灵, etc.) and MultiNet for recognition of up to 200 voice commands without network reconnection. The pipeline processes audio streams from microphones or files stored in flash/SD via an Audio Front-End (AFE) module performing signal preprocessing. The architecture leverages the ESP32-S3 with its high-speed octal SPI PSRAM to deploy optimized inference models.
**Chinese specificity:** Native integration of Chinese keywords (Alibaba's 天猫精灵, Xiaomi's 小爱同学) and support for Mandarin voice commands. Developed by Espressif Systems, a Chinese SoC WiFi/BLE manufacturer dominating the Asian IoT market.
**Western equivalent:** Amazon Alexa Voice Service SDK, Google Assistant SDK (require cloud connection); PocketSphinx (offline speech recognition but less optimized for microcontrollers)
**Maturity:** Active (★ 24, 10 forks, updated 2026-02)
**Language:** Bilingual CN-EN
**Gitee:** https://gitee.com/EspressifSystems/esp-skainet
---
