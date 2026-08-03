---
## Tencent/ncnn [MODIFIÉ]
**Type:** Library
**Domain:** Edge AI
**Relevance score:** 90/100
**Problem solved:** Deploy deep learning models (PyTorch, ONNX) to mobile, embedded, and edge devices with minimal runtime overhead and optimized inference latency. Eliminates dependency on heavy frameworks like TensorFlow Lite or CoreML by providing a self-contained C++ inference engine with ARM NEON and Vulkan GPU acceleration.
**How it works:** ncnn is a C++ inference framework with a Python binding and C API. Core components include a model loader for `.param` and `.bin` format files, CPU execution engine with ARM NEON optimizations and multi-core scheduling, optional Vulkan GPU backend, and pnnx tool for converting PyTorch and ONNX models. Supports fp16 storage, int8 quantization, and custom layer registration. No external BLAS, NNPACK, or runtime dependencies; direct memory-mapped model loading.
**Chinese specificity:** Developed by Tencent's Youtu Lab and deployed in production across Tencent applications (WeChat, QQ, Qzone, Pitu). No integration with Chinese cloud platforms or chipset vendors documented; specificity is primarily organizational rather than ecosystem-driven.
**Western equivalent:** TensorFlow Lite (Google), ONNX Runtime (Microsoft/Linux Foundation), CoreML (Apple)
**Maturity:** Active (★ 303, 3 forks, updated 2026-07)
**Language:** Bilingual CN-EN
**Gitee:** https://gitee.com/Tencent/ncnn
---
