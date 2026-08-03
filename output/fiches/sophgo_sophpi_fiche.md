---
## sophgo/sophpi
**Type:** Board Support Package
**Domain:** Embedded
**Relevance score:** 64/100
**Problem solved:** Provide an open-source SDK and BSP for the CV18xx and SG200x series SoCs (SOPHGO's computer vision processors), enabling firmware development, kernel porting, sensor/panel driver integration, and edge AI inference without reliance on proprietary toolchains.
**How it works:** The project is a monorepo-style SDK combining Linux kernel (5.10), U-Boot bootloader, RT-Thread RTOS option, device drivers (sensors: GC2053, GC2093, GC4683, SC535HAI, etc.; panels: MS7024, GC9307, ST7789P3; storage: SPI-NOR, SPI-NAND, eMMC), build system (defconfig-based), and TDL SDK (SOPHGO's inference framework with YOLO v8/v11, face detection, LLM support). Languages: C, shell scripts. Dependencies include musl/glibc toolchains, OpenSBI, and vendor-specific DDR/FSBL firmware. Targets CV180x, CV181x, CV1812, CV1815, CV1842, SG200x variants with different storage and memory configurations.
**Chinese specificity:** SOPHGO is a Chinese fabless semiconductor company specializing in edge AI and computer vision SoCs; this SDK is the official open-source development platform for their CV18xx/SG200x product line. The project integrates SOPHGO's proprietary TDL (Tensor Deep Learning) inference SDK and supports Chinese ecosystem components (AIC8800 WiFi chipset, GT9xx touchscreen drivers, DNSMASQ for IoT gateways).
**Western equivalent:** Yocto/OpenEmbedded (generic Linux BSP framework), Buildroot (embedded Linux build system), Zephyr (RTOS alternative), NXP i.MX SDK (vendor-specific SoC BSP)
**Maturity:** Active (★ 59, 35 forks, updated 2026-07)
**Language:** Bilingual CN-EN
**GitHub:** https://github.com/sophgo/sophpi
---
