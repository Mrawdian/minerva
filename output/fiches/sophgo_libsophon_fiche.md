---
## sophgo/libsophon
**Type:** Driver
**Domain:** Embedded
**Relevance score:** 71/100
**Problem solved:** Provide Linux kernel drivers and runtime libraries for Sophgo AI accelerator chips (TPU, VPU, JPU, VPP modules), enabling host systems to offload inference and media processing workloads to these specialized processors.
**How it works:** libsophon comprises Linux kernel drivers (sg_x86_pcie_device module for PCIe), bmlib runtime library, TPU runtime with static quantization support (int8), bmcv media processing library, and bm-smi monitoring tool. Written in C/C++, built with CMake/Ninja, supports x86_64 PCIe, ARM64 (aarch64), and LoongArch64 architectures via cross-compilation toolchains. Firmware loading via /lib/firmware and kernel module insertion (insmod) required for operation.
**Chinese specificity:** Sophgo is a Chinese AI chip vendor; libsophon is the official driver and runtime stack for their BM1684x and related processors. No integration with Chinese cloud platforms or standards documented in the README.
**Western equivalent:** NVIDIA CUDA (proprietary, x86/ARM), Intel OpenVINO (inference runtime), Qualcomm Hexagon SDK (DSP/NPU drivers)
**Maturity:** Active (★ 26, 16 forks, updated 2026-07)
**Language:** Bilingual CN-EN
**GitHub:** https://github.com/sophgo/libsophon
---
