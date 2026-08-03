---
## kendryte/nncase
**Type:** Tool
**Domain:** Edge AI
**Relevance score:** 82/100
**Problem solved:** Compiling neural network models (TensorFlow, ONNX, etc.) into optimized code for Kendryte AI accelerators (K210, K510, K230), handling quantization and operation scheduling on specialized compute units (KPU).
**How it works:** nncase is a neural network compiler written in C++ that takes ONNX or TensorFlow format models as input, applies optimization passes (operator fusion, post-training quantization), and generates executable bytecode for the KPU (Kendryte Processing Unit). The Python runtime (pip install nncase nncase-kpu) exposes a compilation and inference API. Supported targets are K210, K510, and K230; compilation is performed via CMake (Ninja or make) on Linux/Windows, with integration into K230_SDK for embedded deployment.
**Chinese specificity:** Developed by Canaan Creative (creator of the Kendryte chipset), this compiler is the official deployment tool for the K2xx product line. The ecosystem includes Canaan resources (pre-trained models, SDK images, Bilibili tutorials) and native integration with K230_SDK and Canmv (MicroPython for Kendryte).
**Western equivalent:** TVM (Apache), ONNX Runtime (Microsoft), TensorFlow Lite Converter (Google) — but none are specialized for Kendryte accelerators; nncase combines compilation + quantization + KPU-specific scheduling.
**Maturity:** Stable (★ 898, 209 forks, updated 2026-07)
**Language:** Bilingual CN-EN
**GitHub:** https://github.com/kendryte/nncase
---
