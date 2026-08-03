---
## sophgo/fsbl
**Type:** Board Support Package
**Domain:** Embedded
**Relevance score:** 57/100
**Problem solved:** Provide a first-stage bootloader (FSBL) for CV18xx series SoCs that acts as an ARM Trusted Firmware (ATF) BL2 stage, enabling secure boot and firmware loading on Sophgo's processors.
**How it works:** FSBL is a bootloader written in C/assembly that initializes the CV18xx SoC hardware, sets up memory and clocks, and hands off control to the next boot stage (typically ATF BL31 or the main OS kernel). It operates at the lowest privilege level before any OS kernel runs. The project integrates with Sophgo's SoC-specific drivers and memory layout definitions. Dependencies and build system details are to be confirmed from the repository structure.
**Chinese specificity:** Sophgo is a Chinese semiconductor company specializing in AI accelerators and SoCs; the CV18xx series is their proprietary processor line. This bootloader is essential infrastructure for Sophgo's embedded and edge AI product ecosystem.
**Western equivalent:** ARM Trusted Firmware (ATF) BL2 stage, U-Boot SPL (Das U-Boot), Rockchip miniloader
**Maturity:** Active (★ 11, 24 forks, updated 2026-06)
**Language:** English
**GitHub:** https://github.com/sophgo/fsbl
---
