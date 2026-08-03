---
## bouffalolab/bouffalo_isp
**Type:** Tool
**Domain:** Embedded
**Relevance score:** 65/100
**Problem solved:** Provide a Linux-hosted ISP (In-System Programming) tool to flash firmware into BouffaloLab RISC-V and ARM MCUs (BL602, BL702, BL616 series) via serial interface, replacing vendor-proprietary Windows-only flashing utilities.
**How it works:** C-based command-line utility that communicates with BouffaloLab chips over UART at configurable baud rates (e.g., 2 Mbps). Accepts pre-built binary firmware images (combined bootloader + application + auxiliary binaries) and writes them via the chip's built-in ISP protocol. Requires cross-compilation for the target Linux platform (x86, ARM) via CMake; boot and reset pin configuration is user-editable in user_config.h. No external dependencies beyond standard C library and serial I/O.
**Chinese specificity:** BouffaloLab is a subsidiary of Nantong Bouffalo Technology, a Chinese fabless semiconductor company specializing in RISC-V and ARM-based IoT/edge MCUs. The project directly supports BouffaloLab's proprietary chip families (BL602, BL702, BL616, BL808), which are widely used in Chinese IoT and edge AI applications.
**Western equivalent:** esptool.py (Espressif, for ESP32 flashing), openocd (ARM/RISC-V debugging and flashing), pyocd (ARM Cortex-M flashing)
**Maturity:** Experimental (★ 4, 1 forks, updated 2025-03)
**Language:** English
**GitHub:** https://github.com/bouffalolab/bouffalo_isp
---
