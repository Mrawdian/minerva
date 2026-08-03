---
## EspressifSystems/esp-idf [MODIFIÉ]
**Type:** Framework
**Domain:** Embedded
**Relevance score:** 94/100
**Problem solved:** Provide a unified development framework and build system for Espressif ESP32 and ESP32-S2 SoCs, including bootloader, partition table generation, and hardware abstraction across Windows, Linux, and macOS host platforms.
**How it works:** ESP-IDF is a CMake-based build framework written in C/C++ with Python tooling (idf.py CLI). It includes FreeRTOS as the RTOS kernel, HAL drivers for peripherals (GPIO, SPI, I2C, UART, WiFi, BLE), partition table management, and OTA update support. The framework uses git submodules to manage dependencies and provides menuconfig for project configuration. Supported targets include ESP32, ESP32-S2, and earlier ESP8266/ESP8285 via a separate RTOS SDK.
**Chinese specificity:** Espressif Systems (乐鑫, Shanghai) is the manufacturer of ESP32/ESP32-S2 SoCs and maintains this official framework. The Gitee repository is an official mirror synchronized daily from GitHub; no Chinese-specific standards or integrations are evident beyond the vendor's origin.
**Western equivalent:** Arduino IDE (for ESP32 boards), Zephyr RTOS (Linux Foundation), PlatformIO (cross-platform embedded development)
**Maturity:** Stable (★ 877, 390 forks, updated 2026-07)
**Language:** Bilingual CN-EN
**Gitee:** https://gitee.com/EspressifSystems/esp-idf
---
