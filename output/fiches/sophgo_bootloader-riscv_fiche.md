---
## sophgo/bootloader-riscv [MODIFIÉ]
**Type:** Board Support Package
**Domain:** Embedded
**Relevance score:** 55/100
**Problem solved:** Bootstrap RISC-V systems by providing a bootloader implementation for RISC-V-based SoCs. Enables firmware loading and system initialization on RISC-V architectures where vendor bootloaders may be proprietary or unavailable.
**How it works:** A RISC-V bootloader written in C and assembly, responsible for early-stage hardware initialization, memory setup, and handoff to the kernel or next-stage bootloader. Targets RISC-V instruction set architecture; likely supports common RISC-V SoCs. Dependencies and specific hardware targets to be confirmed from source code inspection.
**Chinese specificity:** Hosted by SOPHGO (a Chinese semiconductor company specializing in AI and edge computing SoCs with RISC-V cores). SOPHGO's BM1684, BM1688, and other processors use RISC-V or RISC-V-compatible cores, making this bootloader relevant to their product ecosystem.
**Western equivalent:** U-Boot (RISC-V port), OpenSBI (RISC-V Supervisor Binary Interface), Coreboot (RISC-V support)
**Maturity:** Active (★ 26, 44 forks, updated 2026-07)
**Language:** English
**GitHub:** https://github.com/sophgo/bootloader-riscv
---
