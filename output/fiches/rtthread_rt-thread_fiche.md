---
## rtthread/rt-thread [MODIFIÉ]
**Type:** RTOS
**Domain:** Embedded
**Relevance score:** 100/100
**Problem solved:** Provide a scalable real-time operating system that runs on resource-constrained microcontrollers (ARM Cortex-M0 with 3 KB Flash / 1.2 KB RAM) while supporting larger IoT devices (ARM Cortex-A, MIPS32/64 multicore). Unifies kernel, BSP, device drivers, and a modular component ecosystem (VFS, FinSH CLI, network stack) under a single C-based RTOS.
**How it works:** RT-Thread is a monolithic RTOS kernel written in C, with a layered architecture: kernel layer (threading, scheduling, semaphores, mailbox, message queue, memory management, timers), libcpu/BSP layer (CPU porting and peripheral drivers), and components/services layer (VFS, FinSH command-line interface, network frameworks, device framework). Supports GCC, Keil, and IAR toolchains. Includes a package manager (450+ packages) for modular software composition. Ported to STM32F103 and other mainstream MCUs.
**Chinese specificity:** Hosted on Gitee/GitHub by rtthread; no particular Chinese specificity beyond the author. Founded in 2006 as a community-driven open-source project; no documented affiliation with HiSilicon, Rockchip, Espressif, or other Chinese chipset vendors.
**Western equivalent:** FreeRTOS (Amazon), Zephyr (Linux Foundation), RIOT OS
**Maturity:** Stable (★ 5527, 2264 forks, updated 2026-07)
**Language:** Bilingual CN-EN
**Gitee:** https://gitee.com/rtthread/rt-thread
---
