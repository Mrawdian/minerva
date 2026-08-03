---
## sophgo/ramdisk
**Type:** Board Support Package
**Domain:** Embedded
**Relevance score:** 47/100
**Problem solved:** Generate root filesystem images and device tree binaries (ITB) for CV18xx SoC series, with support for platform-independent and platform-specific file overlays during build.
**How it works:** The project organizes rootfs components into prebuild (cross-compilation headers/libraries), target (common and overlay directories merged at build time), tools (scripts for ITB generation), and configs (txt file lists and ITS device tree source files). Build process merges overlay files into common base, then generates final rootfs and ITB artifacts. Written in shell/build scripts; depends on device tree compiler and cross-compilation toolchain.
**Chinese specificity:** Sophgo is a Chinese semiconductor company specializing in AI accelerators and SoCs; CV18xx is their proprietary embedded processor series. This project is the official rootfs configuration for Sophgo's CV18xx platform.
**Western equivalent:** Buildroot (Linux Foundation), Yocto Project (Linux Foundation) — both provide rootfs generation and overlay mechanisms for embedded Linux systems.
**Maturity:** Active (★ 1, 12 forks, updated 2026-06)
**Language:** English
**GitHub:** https://github.com/sophgo/ramdisk
---
