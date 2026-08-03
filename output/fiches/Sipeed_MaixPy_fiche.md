---
## Sipeed/MaixPy
**Type:** Framework
**Domain:** Edge AI
**Relevance score:** 63/100
**Problem solved:** Provide a Python-based development framework for edge AI vision and audio inference on resource-constrained embedded systems (MaixCAM series), eliminating the need to write low-level C/C++ for common tasks like camera capture, neural network inference, and peripheral I/O.
**How it works:** MaixPy is a Python binding layer wrapping C/C++ SDK for Sipeed's MaixCAM hardware (based on SG200 or similar SoC). Core modules include `maix.camera` (video capture), `maix.nn` (model inference via on-device NPU), `maix.display` (framebuffer output), `maix.uart` and other peripherals. Models are packaged in `.mud` format. The framework also includes MaixVision IDE (desktop workstation for live debugging) and MaixHub (cloud-based model training and conversion service). Supports both Python scripting and C/C++ SDK with identical APIs.
**Chinese specificity:** Sipeed is a Chinese semiconductor design company specializing in RISC-V and edge AI SoCs. MaixCAM hardware integrates Sipeed's own SG200 processor or similar proprietary silicon. The MaixHub platform provides free cloud-based AI model training and quantization, reducing dependency on external cloud providers for model preparation.
**Western equivalent:** OpenMV (STM32H7 + MicroPython), TensorFlow Lite for Microcontrollers, MediaPipe (Google), PyTorch Mobile
**Maturity:** Active (★ 2, updated 2026-07)
**Language:** Bilingual CN-EN
**Gitee:** https://gitee.com/Sipeed/MaixPy
---
