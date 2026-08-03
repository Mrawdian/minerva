---
## sophgo/cviruntime
**Type:** Library
**Domain:** Embedded
**Relevance score:** 59/100
**Problem solved:** Provide a runtime library and SDK for developing applications targeting SOPHGO TPU accelerators (CV181x, BM1880v2 series). Enables inference execution on TPU hardware with model loading, execution, and profiling capabilities.
**How it works:** C/C++ runtime library that loads and executes neural network models (via cvimodel format, using FlatBuffers serialization) on SOPHGO TPU hardware. Core dependencies: cvibuilder (model compilation), cvikernel (TPU kernel library), flatbuffers (model format), cnpy (NumPy interop). Builds as libcviruntime.so and libcviruntime-static.a. Supports multiple execution modes: SOC (on-device), CMODEL (simulation). Includes test_cvimodel tool for validation and benchmarking.
**Chinese specificity:** SOPHGO is a Chinese semiconductor company specializing in AI accelerators and TPU design. cviruntime is the official runtime stack for SOPHGO's CV-series and BM-series TPU chips, integral to their edge AI inference ecosystem.
**Western equivalent:** TensorFlow Lite (Google), NCNN (Tencent), TVM runtime (Apache), ONNX Runtime (Microsoft)
**Maturity:** Experimental (★ 5, 11 forks, updated 2025-11)
**Language:** Bilingual CN-EN
**GitHub:** https://github.com/sophgo/cviruntime
---
