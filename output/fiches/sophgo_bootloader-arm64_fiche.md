---
## sophgo/bootloader-arm64
**Type:** Board Support Package
**Domain:** Embedded
**Relevance score:** 61/100
**Problem solved:** Provide a bootloader for Sophon AI accelerator chips (BM1684 SoC) that initializes ARM64 hardware, loads the Linux kernel, and bridges proprietary Sophon firmware with open-source OS boot flow.
**How it works:** The project is a U-Boot-based bootloader (ARM64 architecture) that integrates with a custom Linux kernel port (linux-arm64) and Sophon middleware stack. Build process uses GCC Linaro 6.3.1 toolchain, device-tree-compiler, and u-boot-tools; it generates Debian packages (sophon-soc-libsophon, sophon-mw-soc-sophon-ffmpeg, sophon-mw-soc-sophon-opencv) that are staged into a rootfs via debootstrap. The bootloader depends on libsophon (separate repository) for hardware abstraction and links against Sophon's proprietary middleware libraries.
**Chinese specificity:** Hosted by Sophgo (算能), a Chinese AI chip design company that manufactures the Sophon BM1684 TPU accelerator. The bootloader is specific to Sophgo's SoC ecosystem and integrates with their proprietary firmware and middleware stack, which is not available in Western open-source projects.
**Western equivalent:** U-Boot (DENX), Arm Trusted Firmware (Arm), Barebox — but none target Sophon chips; this is a vendor-specific BSP for a Chinese accelerator SoC.
**Maturity:** Active (★ 12, 26 forks, updated 2026-06)
**Language:** English
**GitHub:** https://github.com/sophgo/bootloader-arm64
---
