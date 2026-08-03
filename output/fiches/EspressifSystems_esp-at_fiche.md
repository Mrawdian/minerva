---
## EspressifSystems/esp-at [MODIFIÉ]
**Type:** Framework
**Domain:** IoT
**Relevance score:** 84/100
**Problem solved:** Provide a standardized AT command interface for Espressif ESP32/ESP8266 SoCs to enable host microcontrollers to control wireless connectivity (WiFi, Bluetooth, cellular) without implementing full network stacks, reducing firmware complexity on resource-constrained platforms.
**How it works:** ESP-AT is a firmware framework built on ESP-IDF and ESP8266-RTOS-SDK that runs on Espressif SoCs (ESP32, ESP32-C2, ESP32-C3, ESP32-C5, ESP32-C6, ESP32-C61, ESP32-S2) and exposes AT command sets for WiFi, Bluetooth, and TCP/IP operations. The host communicates via UART or SPI using text-based AT commands and receives structured responses. The framework includes built-in command handlers, customizable user-defined AT commands, and pre-compiled firmware binaries for each chip variant. Development targets Windows, Linux, and macOS.
**Chinese specificity:** Espressif Systems (Shanghai) is the manufacturer of ESP32/ESP8266 SoCs and maintains this as an official project; the Gitee repository is an official domestic mirror synchronized from GitHub. No integration with Chinese cloud platforms (Baidu, Alibaba, Tencent) or WeChat/Alipay APIs is evident in the provided context.
**Western equivalent:** Arduino AT library (for Arduino boards), Quectel AT command framework (for cellular modules), u-blox AT command sets (for GNSS/cellular modules)
**Maturity:** Active (★ 50, 4 forks, updated 2026-07)
**Language:** Bilingual CN-EN
**Gitee:** https://gitee.com/EspressifSystems/esp-at
---
