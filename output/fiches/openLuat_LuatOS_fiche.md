---
## openLuat/LuatOS [MODIFIÉ]
**Type:** Framework
**Domain:** Embedded
**Relevance score:** 82/100
**Problem solved:** Enable rapid IoT application development on Hezhou cellular modules (Air8000/Air8101/Air780E series) using Lua scripting instead of C/C++, reducing firmware development cycles for industrial IoT devices.
**How it works:** LuatOS wraps Lua 5.3 VM with 74 core libraries and 55 extension libraries (totaling 1000+ APIs) compiled as C components. The architecture consists of: Lua interpreter core, LuatOS framework layer (luat folder), hardware-specific BSP implementations for Air8000/Air8101/Air780E modules, and Lua script libraries. Firmware is flashed onto Hezhou modules; development uses Lua scripts executed by the embedded VM with access to cellular, GPIO, UART, SPI, and sensor APIs.
**Chinese specificity:** Developed by openLuat (合宙's software division) specifically for Hezhou's proprietary cellular module lineup (Air8000/Air8101/Air780E series), which dominate Chinese industrial IoT deployments. Hezhou is a major cellular module vendor in China's IoT supply chain.
**Western equivalent:** MicroPython (Python Software Foundation), Espressif ESP-IDF with Lua bindings, NodeMCU (Lua on ESP8266)
**Maturity:** Stable (★ 1862, 514 forks, updated 2026-07)
**Language:** Bilingual CN-EN
**Gitee:** https://gitee.com/openLuat/LuatOS
---
