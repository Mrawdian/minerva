---
## sophgo/zsbl
**Type:** Board Support Package
**Domain:** Embedded
**Relevance score:** 52/100
**Problem solved:** Provide a RISC-V bootloader for SOPHGO SoCs that initializes the processor, loads the next stage bootloader or kernel, and handles early hardware setup before the main OS takes control.
**How it works:** ZSBL (Zero Stage BootLoader) is a minimal first-stage bootloader written for SOPHGO RISC-V processors. It performs CPU initialization, memory setup, and handoff to a secondary bootloader or kernel image. The project is written in C and assembly, targeting SOPHGO's RISC-V SoC lineup. Dependencies and specific hardware initialization sequences are to be confirmed from the source code.
**Chinese specificity:** SOPHGO is a Chinese fabless semiconductor company specializing in AI accelerators and RISC-V SoCs; this bootloader is part of their open-source software stack for their proprietary RISC-V processor family.
**Western equivalent:** U-Boot (Denx), coreboot (Linux Foundation), OpenSBI (RISC-V Foundation)
**Maturity:** Active (★ 33, 35 forks, updated 2026-07)
**Language:** English
**GitHub:** https://github.com/sophgo/zsbl
---
