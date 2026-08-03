---
## sophgo/TPU-Megatron-Patch
**Type:** Framework
**Domain:** Embedded
**Relevance score:** 54/100
**Problem solved:** Adapt the Megatron distributed training framework to run on SOPHGO TPU accelerators for large language model (LLM) and visual language model (VLM) training, replacing GPU-centric training pipelines with TPU-optimized distributed training.
**How it works:** TPU-Megatron-Patch extends the Megatron-LM framework (originally designed for NVIDIA GPUs) to support SOPHGO TPU hardware via the torch_tpu binding layer. The toolkit is written in Python and integrates with PyTorch, providing distributed training utilities for model parallelism and data parallelism. Currently documented support includes Qwen2-7B fine-tuning; the codebase is derived from Alibaba's Pai-Megatron-Patch and adds TPU-specific optimizations and device driver integration.
**Chinese specificity:** Maintained by SOPHGO, a Chinese semiconductor company specializing in AI accelerators and TPU design. The project directly targets SOPHGO's TPU product line and integrates with the Chinese AI training ecosystem, though it does not reference specific Chinese standards or cloud platforms.
**Western equivalent:** Megatron-LM (NVIDIA), DeepSpeed (Microsoft), Hugging Face Transformers with distributed training backends
**Maturity:** Experimental (updated 2024-12)
**Language:** Bilingual CN-EN
**GitHub:** https://github.com/sophgo/TPU-Megatron-Patch
---
