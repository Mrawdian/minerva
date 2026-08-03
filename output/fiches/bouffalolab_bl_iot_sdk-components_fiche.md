---
## bouffalolab/bl_iot_sdk-components
**Type:** Library
**Domain:** Embedded
**Relevance score:** 70/100
**Problem solved:** Provide modular, reusable components for IoT applications built on the BL602/BL604 SoC family, decoupling firmware logic from low-level hardware abstractions to reduce duplication across projects using Bouffalo Lab chipsets.
**How it works:** This is a component library repository that serves as a submodule for bl_iot_sdk_tiny, offering pre-built modules (likely including WiFi/BLE stack integration, peripheral drivers, and middleware) written in C/C++. The architecture separates hardware-specific code from application logic, allowing developers to import only needed components rather than the full SDK. Dependencies and exact module list are not documented in accessible README; verification of supported protocols (802.11b/g/n, BLE 5.x) and peripheral interfaces (UART, SPI, I2C, GPIO) requires repository inspection.
**Chinese specificity:** Bouffalo Lab is a subsidiary of Nanjing Xiaoxiongpai Intelligent Technology Co., Ltd., a Chinese fabless semiconductor company specializing in ultra-low-power WiFi and BLE SoCs (BL602, BL604, BL702 series). This component library directly supports Bouffalo's proprietary chipset ecosystem and is part of the official IoT SDK distribution for Chinese IoT manufacturers.
**Western equivalent:** ESP-IDF component registry (Espressif), Zephyr module ecosystem (Linux Foundation), STM32CubeMX HAL libraries (STMicroelectronics)
**Maturity:** Active (★ 3, 3 forks, updated 2026-06)
**Language:** English
**GitHub:** https://github.com/bouffalolab/bl_iot_sdk-components
---
