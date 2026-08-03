---
## sophgo/LLM-TPU [MODIFIÉ]
**Type:** Tool
**Domain:** Embedded
**Relevance score:** 67/100
**Problem solved:** Deploy large language models (LLM) and vision-language models (VLM) with quantization and multi-chip parallelism on SOPHGO BM1684X/BM1688 TPU accelerators, converting HuggingFace weights directly to bmodel format without manual optimization.
**How it works:** The project provides llm_convert.py, a Python-based compiler that ingests quantized models (AWQ/GPTQ) from HuggingFace and generates bmodel binaries for SOPHGO TPUs via the TPU-MLIR toolchain. Inference is executed through C++ and Python runtime bindings that manage KV cache, dynamic shape compilation, and multi-chip distribution. Pre-compiled bmodels are hosted for rapid deployment; supported models include Qwen, Llama, DeepSeek, InternVL, MiniCPM, and Phi families with multimodal support (text, image, video, audio).
**Chinese specificity:** SOPHGO is a Chinese semiconductor vendor specializing in AI accelerators; the BM1684X and BM1688 are proprietary SOPHGO TPU chips. The project is officially maintained by SOPHGO and targets their domestic TPU product line, representing a key deployment pathway for generative AI on Chinese-designed accelerators.
**Western equivalent:** TensorRT (NVIDIA), OpenVINO (Intel), ONNX Runtime (Microsoft/Linux Foundation) — though these target different accelerator ecosystems; no direct Western equivalent for SOPHGO TPU deployment exists.
**Maturity:** Active (★ 297, 49 forks, updated 2026-07)
**Language:** Bilingual CN-EN
**GitHub:** https://github.com/sophgo/LLM-TPU
---
