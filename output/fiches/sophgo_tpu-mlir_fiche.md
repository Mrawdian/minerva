---
## sophgo/tpu-mlir
**Type:** Tool
**Domain:** Embedded
**Relevance score:** 78/100
**Problem solved:** Compiling pre-trained neural network models (PyTorch, ONNX, TFLite, Caffe, HuggingFace) into optimized binaries (bmodel) executable on Sophgo TPU, with full support for quantization (INT8, BF16, F16) and LLM.
**How it works:** Two-stage MLIR pipeline: import front-end (model_transform.py) converts standard formats to MLIR Top dialect, then back-end (model_deploy.py) lowers to Tpu dialect with optimizations (layer-group memory planning, pattern rewrites, symmetric/asymmetric quantization, AWQ/GPTQ/AutoRound). Complementary tools: model_runner (inference), model_tool (inspection), simulator, visualizer. Deployment via Docker (sophgo/tpuc_dev) with Python ≥3.10 on Ubuntu 22.04.
**Chinese specificity:** Sophgo is a Chinese fabless company specializing in TPU SoCs; this compiler directly targets its TPU architectures (bm1684x cited). Native integration of popular HuggingFace models in China (Qwen, MiniCPM-V). Bilingual CN-EN documentation and active community on Gitee.
**Western equivalent:** TVM (Apache), ONNX Runtime (Microsoft), TensorFlow Lite Converter (Google), PyTorch Export (Meta) — but none offer the same MLIR compiler integration + quantization + proprietary TPU targeting.
**Maturity:** Stable (★ 954, 226 forks, updated 2026-07)
**Language:** Bilingual CN-EN
**GitHub:** https://github.com/sophgo/tpu-mlir
---
