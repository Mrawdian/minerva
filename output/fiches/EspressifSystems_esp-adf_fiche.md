---
## EspressifSystems/esp-adf [MODIFIÉ]
**Type:** Framework
**Domain:** Embedded
**Relevance score:** 73/100
**Problem solved:** Provide a product-oriented application framework for ESP32/ESP32-S2 audio and video development, abstracting away low-level IDF complexity. ADF v3.0 restructures the media pipeline using ESP-GMF and modularizes services (audio playback, video playback, battery monitoring) callable via Model Context Protocol.
**How it works:** ADF v3.0 is built on top of ESP-IDF (v5.5.2+) and integrates ESP-GMF as the core multimedia framework. It provides standalone functional components (playlist, board manager) and modular product services accessible through MCP. Supports development in C/C++, MicroPython, and Arduino. The architecture separates low-level drivers (handled by ESP-IDF) from high-level services (audio/video playback, OTA, battery service) with emphasis on low memory and CPU footprint.
**Chinese specificity:** Espressif Systems (乐鑫, Shanghai) is the manufacturer of ESP32/ESP32-S2 SoCs and maintains this official framework. The Gitee repository is an official mirror synchronized from GitHub; no particular Chinese standard compliance or domestic platform integration mentioned.
**Western equivalent:** Zephyr (Linux Foundation, multimedia extensions), FreeRTOS with audio libraries (Amazon), TinyOS with media components
**Maturity:** Active (★ 72, 9 forks, updated 2026-07)
**Language:** Bilingual CN-EN
**Gitee:** https://gitee.com/EspressifSystems/esp-adf
---
