---
## sophgo/vllm-tpu
**Type:** Framework
**Domain:** Embedded
**Relevance score:** 57/100
**Problem solved:** Enable inference of large language models (LLaMa, Qwen, DeepSeek) on Sophon TPU SG2260 accelerators by porting vLLM v0.11.0 to support TPU-specific execution paths, quantization formats (w4a16, FP8, BF16), and multi-chip topologies.
**How it works:** Fork of vLLM v0.11.0 with TPU backend integration for Sophon SG2260 hardware. Supports model inference in both Cmodel (CPU-emulated) and Device (native TPU) modes via Docker containers. Includes Torch-TPU wheel package for tensor operations, tpuv7 runtime/driver stack (v1.1.3), and weight reordering cache for quantized models. Tested on Llama2/3.1, Qwen2/2.5, QwQ, LLaVa, and DeepSeek model families with FP16, BF16, FP8, and w4a16 quantization.
**Chinese specificity:** Sophgo is a Chinese semiconductor company specializing in AI accelerators; the SG2260 is their TPU product line. Project integrates with Sophgo's proprietary tpuv7 runtime and driver ecosystem. Model weights sourced from Chinese platforms (ModelScope, Gitee AI) alongside HuggingFace.
**Western equivalent:** vLLM (Meta/LLM community), TensorRT-LLM (NVIDIA), Ollama (local inference), MLX (Apple Silicon)
**Maturity:** Experimental (★ 6, 1 forks, updated 2025-12)
**Language:** Bilingual CN-EN
**GitHub:** https://github.com/sophgo/vllm-tpu
---
