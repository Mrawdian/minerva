---
## rtthread/smart-build
**Type:** Board Support Package
**Domain:** Embedded
**Relevance score:** 71/100
**Problem solved:** Automate cross-compilation of the RT-Thread kernel, rootfs (busybox), and bootloader for ARM targets (qemuarm64, etc.) via a Bitbake/OpenEmbedded toolchain, avoiding repetitive manual configuration of toolchains and build steps.
**How it works:** Smart-build is an OpenEmbedded/Bitbake layer that orchestrates compilation via Bitbake recipes. The workflow downloads smart-gcc (cross toolchain), compiles busybox into ext4 rootfs, then compiles the RT-Thread kernel into rtthread.bin. Dependencies include openembedded-core, bitbake, Python 3 (scons, kconfiglib, tqdm), and host tools (bison, flex, cpio, qemu-system-arm). Supported targets include qemuarm64 and other ARM architectures via the MACHINE variable.
**Chinese specificity:** Hosted on Gitee by rtthread (RT-Thread Microsystems, Chinese publisher of the RT-Thread RTOS); no particular Chinese specificity beyond the author — no Chinese chipset vendor cited, no local ecosystem integration detected.
**Western equivalent:** Yocto Project (Linux Foundation), Buildroot, OpenWrt (for embedded Linux systems)
**Maturity:** Experimental (updated 2025-08)
**Language:** Bilingual CN-EN
**Gitee:** https://gitee.com/rtthread/smart-build
---
