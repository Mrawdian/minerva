---
## Embedfire/linux-firmware
**Type:** Documentation
**Domain:** Embedded
**Relevance score:** 67/100
**Problem solved:** Provide firmware blobs and device tree binaries required by the Linux kernel to initialize and operate hardware peripherals (WiFi, Bluetooth, GPU, modem, etc.) on various SoCs and embedded boards.
**How it works:** This is a mirror/distribution of the upstream linux-firmware repository from kernel.org, containing pre-compiled firmware files (typically .bin, .fw, .ucode formats) and device tree source files organized by hardware vendor (Broadcom, Qualcomm, Intel, AMD, Marvell, etc.). The repository is language-agnostic; it serves as a binary artifact store indexed by hardware identifiers. Installation typically involves copying firmware files to /lib/firmware on a Linux system during kernel boot or module loading.
**Chinese specificity:** Hosted on Gitee by Embedfire, a Chinese educational electronics brand; no particular Chinese specificity beyond the author. The repository itself is a direct mirror of upstream kernel.org firmware and contains no Embedfire-specific modifications or Chinese chipset vendor integrations.
**Western equivalent:** linux-firmware (kernel.org upstream), firmware-nonfree (Debian), linux-firmware-git (Arch Linux)
**Maturity:** Active (updated 2026-07)
**Language:** English
**Gitee:** https://gitee.com/Embedfire/linux-firmware
---
