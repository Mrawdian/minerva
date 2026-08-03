---
## EspressifSystems/ESP8266_RTOS_SDK [MODIFIÉ]
**Type:** Board Support Package
**Domain:** Embedded
**Relevance score:** 100/100
**Problem solved:** Provides an RTOS-based SDK for the ESP8266 microcontroller with FreeRTOS, lwIP, and Wi-Fi drivers integrated. Addresses the need for a complete development environment to build networked embedded applications on the ESP8266 without relying solely on the non-OS SDK.
**How it works:** C-based SDK built on FreeRTOS kernel with integrated lwIP TCP/IP stack, mbedTLS for TLS/SSL, and proprietary Wi-Fi libraries (libmain). Compilation uses the Xtensa LX106 GCC toolchain (v8.4.0 or v4.8.5 depending on SDK version). Supports menuconfig-driven build configuration. Core components include SPIFFS filesystem, cJSON, libcoap, and noPoll WebSocket library. Targets the single-core Xtensa-based ESP8266 SoC.
**Chinese specificity:** Espressif Systems (乐鑫, Shanghai) is the manufacturer of the ESP8266 and ESP32 SoCs; this is the official SDK maintained by the vendor. No particular Chinese standard compliance or domestic ecosystem integration beyond the vendor's role in the global IoT chipset market.
**Western equivalent:** ESP-IDF (Espressif's newer framework for ESP32), FreeRTOS with lwIP stack on other microcontrollers, Arduino core for ESP8266
**Maturity:** Active (★ 101, 66 forks, updated 2026-07)
**Language:** Bilingual CN-EN
**Gitee:** https://gitee.com/EspressifSystems/ESP8266_RTOS_SDK
---
