---
## sophgo/sophon-sail
**Type:** Library
**Domain:** Embedded
**Relevance score:** 54/100
**Problem solved:** Streamline deployment of deep-learning inference models and image/video processing on SOPHON TPU accelerators by providing unified hardware-accelerated pipelines for decoding, preprocessing, and inference with C++ and Python bindings.
**How it works:** SAIL wraps low-level SOPHON libraries (libsophon, bmruntime, bmcv, bmdecoder) and integrates sophon-ffmpeg and sophon-opencv for end-to-end video/image processing. Offers C++ and Python APIs; C++ targets native performance while Python prioritizes ease of prototyping. Supports multiple deployment modes: PCIe (x86 host with BM168x card), SoC (ARM-based SOPHON chips via cross-compilation), and ARM+PCIe. Tensor memory is auto-managed. Dependencies include pybind11 (Python bindings), spdlog (logging), and CMake-based build system with configurable compilation flags (BUILD_TYPE, ONLY_RUNTIME, LIBSOPHON_BASIC_PATH, etc.).
**Chinese specificity:** SOPHON is a TPU product line from Bitmain (算能), a major Chinese AI chip manufacturer. SAIL is the official deployment framework for SOPHON accelerators, tightly integrated with Bitmain's hardware ecosystem and proprietary runtime stack.
**Western equivalent:** TensorRT (NVIDIA), OpenVINO (Intel), MediaPipe (Google) — each provides hardware-accelerated inference and preprocessing, though SOPHON-SAIL is specific to Bitmain TPUs.
**Maturity:** Active (★ 20, 2 forks, updated 2026-07)
**Language:** Bilingual CN-EN
**GitHub:** https://github.com/sophgo/sophon-sail
---
