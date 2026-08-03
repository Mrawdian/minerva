---
## bouffalolab/bouffalo_sdk
**Type:** Board Support Package
**Domain:** Embedded
**Relevance score:** 76/100
**Problem solved:** Provide a unified SDK supporting the entire range of Bouffalo microcontrollers (BL602, BL702/L, BL616, BL618) with a common HAL API (LHAL) to avoid fragmentation between previous bl_mcu_sdk and bl_iot_sdk. This enables developers to use a single codebase for various devices (ADC, SPI, UART, cryptography, camera, Ethernet) without rewriting drivers.
**How it works:** Modular C architecture with layers: BSP (clock, pinmux, heap, console), LHAL drivers (generic peripherals supporting all chips), SOC drivers (chip-specific peripherals), components (network stacks, security), and examples. Peripheral support: UART, SPI, I2C, I2S, GPIO, ADC, DAC, DMA, FLASH, RTC, timers, AES/SHA/TRNG/PKA, camera (CAM), MJPEG (BL616/618), Ethernet (EMAC). Includes unit tests and build tools.
**Chinese specificity:** Bouffalo Lab is the manufacturer of Bouffalo chipsets (BL602, BL702, BL616, BL618); this SDK is the official development kit for this proprietary Chinese product line. No integration with specific Chinese cloud services (WeChat, Alipay, Baidu) detected in the README.
**Western equivalent:** Zephyr Project (Linux Foundation, multi-vendor), FreeRTOS + vendor-specific HAL (Amazon/Texas Instruments), STM32CubeSDK (STMicroelectronics)
**Maturity:** Active (★ 486, 178 forks, updated 2026-07)
**Language:** Bilingual CN-EN
**GitHub:** https://github.com/bouffalolab/bouffalo_sdk
---
