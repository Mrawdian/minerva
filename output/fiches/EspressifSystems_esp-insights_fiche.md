---
## EspressifSystems/esp-insights [MODIFIÉ]
**Type:** Framework
**Domain:** Edge AI
**Relevance score:** 77/100
**Problem solved:** Capture and remotely transmit device diagnostics (error/warning logs, crashes, metrics, reset reasons) from ESP32/ESP8266 devices in the field to a cloud dashboard, enabling developers to diagnose issues that only occur in specific deployment environments without physical access.
**How it works:** The Insights agent is a firmware component (C/C++) integrated into ESP-IDF that hooks into the logging system (ESP_LOGE, ESP_LOGW macros), captures coredumps, heap metrics, and custom events via ESP_DIAG_EVENT calls, then uploads this data over HTTPS to the ESP Insights cloud backend. Configuration is managed via menuconfig (Component config → ESP Insights) and requires an authentication key embedded in firmware. The cloud processes and visualizes the collected data in a web dashboard showing error logs, warnings, reset reasons, stack backtraces, metrics over time, and group analytics.
**Chinese specificity:** Hosted on Gitee/GitHub by EspressifSystems; no particular Chinese specificity beyond the author. Espressif Systems (乐鑫, Shanghai) is the manufacturer of ESP8266 and ESP32 SoCs, and this project is their official remote diagnostics framework for their own chipset ecosystem.
**Western equivalent:** AWS IoT Device Defender (AWS), Azure IoT Hub diagnostics (Microsoft), Google Cloud IoT Core logging, Memfault (independent SaaS for embedded diagnostics)
**Maturity:** Active (★ 2, updated 2026-07)
**Language:** English
**Gitee:** https://gitee.com/EspressifSystems/esp-insights
---
