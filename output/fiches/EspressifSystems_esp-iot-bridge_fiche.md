---
## EspressifSystems/esp-iot-bridge [MODIFIÉ]
**Type:** Framework
**Domain:** IoT
**Relevance score:** 79/100
**Problem solved:** Enable ESP32 and similar Espressif SoCs to bridge multiple network interfaces (Wi-Fi, Ethernet, USB, SPI, SDIO) and act as network gateways or wireless/wired network adapters, supporting use cases such as Wi-Fi routers, cellular hotspots, and network interface emulation for PCs and MCUs.
**How it works:** The solution provides a component-based framework (iot_bridge) that abstracts protocol translation and packet forwarding between heterogeneous network interfaces. It includes reference implementations in C for common scenarios: Wi-Fi router (SoftAP bridging), wireless NIC (USB/ETH/SPI/SDIO to network card), wired NIC (Ethernet ingress with multiple egress interfaces), 4G hotspot (cellular module to Wi-Fi), and 4G NIC (cellular to wired/wireless). Built on ESP-IDF (Espressif IoT Development Framework) and integrates with optional components like Wi-Fi Mesh Lite and Rainmaker.
**Chinese specificity:** Hosted on Gitee/GitHub by EspressifSystems; no particular Chinese specificity beyond the author. Espressif Systems is a Shanghai-based SoC vendor; this project is a reference implementation for their ESP32 family.
**Western equivalent:** OpenWrt (Linux Foundation, router/gateway focus), Home Assistant (network bridge for IoT), Tasmota (ESP8266/ESP32 firmware with network bridging)
**Maturity:** Active (★ 10, updated 2026-07)
**Language:** Bilingual CN-EN
**Gitee:** https://gitee.com/EspressifSystems/esp-iot-bridge
---
