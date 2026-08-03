---
## sophgo/torch-tpu
**Type:** Library
**Domain:** Embedded
**Relevance score:** 56/100
**Problem solved:** Enable execution of PyTorch models on Sophgo TPU devices (SG2260, TPU1686) with support for distributed training frameworks (DeepSpeed, Megatron) and large language models, bridging the gap between PyTorch's CPU/GPU ecosystem and Sophgo's proprietary TPU hardware.
**How it works:** Torch-TPU is a PyTorch C++ extension that provides JIT and Eager execution modes for Sophgo TPU inference and training. It integrates with tpuv7-runtime (Sophgo's TPU runtime), firmware_core (kernel compilation for SG2260/TPU1686), and tpu-train (distributed training support). The project uses Docker for environment isolation, CMake for builds, and supports DeepSpeed Zero Stage 1/2 with CPU offloading and Megatron tensor parallelism for models like Qwen2.
**Chinese specificity:** Sophgo is a Chinese semiconductor company specializing in AI accelerators and TPU design. Torch-TPU directly targets Sophgo's proprietary TPU devices (SG2260, TPU1686) and integrates with Sophgo's closed-source runtime and firmware stack, making it essential infrastructure for deploying PyTorch workloads on Sophgo hardware in the Chinese AI ecosystem.
**Western equivalent:** PyTorch XPU (Intel), PyTorch CUDA/ROCm backends, TensorRT (NVIDIA), OpenVINO (Intel) — though none directly target Sophgo TPUs; closest functional analogue is PyTorch's device abstraction layer for custom accelerators.
**Maturity:** Experimental (★ 12, updated 2026-01)
**Language:** English
**GitHub:** https://github.com/sophgo/torch-tpu
---
