---
## bouffalolab/bouffalo_drivers
**Type:** Driver
**Domain:** Embedded
**Relevance score:** 76/100
**Problem solved:** Provide hardware abstraction layer (HAL), RF parameter management, and SoC-level drivers for Bouffalo Lab microcontrollers and wireless SoCs, enabling firmware developers to access peripheral interfaces (GPIO, UART, SPI, I2C, ADC, RF) without direct register manipulation.
**How it works:** The project bundles three driver components: lhal (low-level hardware abstraction), rfparam (radio frequency parameter configuration), and soc drivers (system-on-chip peripheral drivers). Written in C, it targets Bouffalo Lab's BL602, BL604, and related RISC-V based SoCs. Dependencies and exact module organization are not documented in accessible README; integration typically occurs at the firmware build stage via CMake or Make.
**Chinese specificity:** Bouffalo Lab is a Chinese semiconductor vendor specializing in low-power wireless SoCs (BLE, WiFi, Zigbee). This driver repository is the official HAL distribution for their chipset ecosystem, directly supporting their commercial product line.
**Western equivalent:** STMicroelectronics STM32Cube HAL, Nordic nRF5 SDK, Espressif ESP-IDF HAL layer
**Maturity:** Active (★ 6, 2 forks, updated 2026-07)
**Language:** English
**GitHub:** https://github.com/bouffalolab/bouffalo_drivers
---
