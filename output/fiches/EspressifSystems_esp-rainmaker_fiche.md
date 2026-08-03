---
## EspressifSystems/esp-rainmaker [MODIFIÉ]
**Type:** Framework
**Domain:** IoT / Edge AI
**Relevance score:** 75/100
**Problem solved:** Enables remote control and monitoring of ESP32-based IoT devices without manual cloud configuration. Provides a firmware agent that automatically handles device claiming, cloud connectivity, and dynamic UI rendering on mobile clients.
**How it works:** ESP RainMaker consists of a firmware agent (this repository) written in C for ESP-IDF, a claiming service for credential provisioning, and a cloud backend. The agent runs on ESP32 series SoCs (ESP32, ESP32-S2, ESP32-S3, ESP32-C2, ESP32-C3, ESP32-C6, ESP32-H2, ESP32-C5) and communicates with the RainMaker Cloud via MQTT or HTTP. Developers define custom devices and parameters in firmware; the cloud and mobile apps (Android/iOS) dynamically render UI based on device metadata. Requires ESP-IDF 4.1 or later.
**Chinese specificity:** Hosted on Gitee/GitHub by EspressifSystems; no particular Chinese specificity beyond the author. Espressif Systems (乐鑫, Shanghai) is the manufacturer of ESP32 SoCs and maintains this official repository.
**Western equivalent:** Amazon FreeRTOS with AWS IoT Core, Google Cloud IoT Core with embedded client libraries, Azure IoT Hub device SDKs
**Maturity:** Active (★ 11, updated 2026-07)
**Language:** English
**Gitee:** https://gitee.com/EspressifSystems/esp-rainmaker
---
