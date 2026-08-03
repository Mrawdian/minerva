---
## sophgo/cvi_mpi
**Type:** Library
**Domain:** Embedded
**Relevance score:** 66/100
**Problem solved:** Provide multimedia codec and image processing libraries (encoding, decoding, ISP pipeline) for the CV18xx series SoC, which is a family of low-power vision processors used in edge AI and IoT applications.
**How it works:** The project exposes a Media Processing Interface (MPI) layer written in C, wrapping hardware codecs and ISP blocks on CV18xx chips. It includes video encoding/decoding (H.264, H.265, JPEG), image scaling, color space conversion, and sensor interface drivers. Dependencies include the SoC's proprietary firmware and bootloader; the library is typically linked into applications running on the embedded Linux or RTOS kernel provided by the vendor.
**Chinese specificity:** Sophgo is a Chinese fabless semiconductor company specializing in edge AI and video processing SoCs. The CV18xx series is their proprietary architecture; this MPI library is the official multimedia abstraction layer for their chipsets, tightly coupled to Sophgo's hardware design and firmware ecosystem.
**Western equivalent:** Qualcomm Snapdragon Heterogeneous Compute SDK (for video/ISP on mobile SoCs), NVIDIA Tegra Multimedia API (for video encoding on embedded GPUs), MediaTek NeuroPilot (for edge AI SoCs with video support)
**Maturity:** Active (★ 2, 7 forks, updated 2026-06)
**Language:** English
**GitHub:** https://github.com/sophgo/cvi_mpi
---
