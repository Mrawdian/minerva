---
## sophgo/cvikernel
**Type:** Library
**Domain:** Embedded
**Relevance score:** 51/100
**Problem solved:** Generate TPU instructions for SOPHGO's tensor processing units without writing raw assembly. Provides a C/C++ API to programmatically construct and emit TPU instruction sequences, replacing manual assembly coding.
**How it works:** cvikernel is a C/C++ library that translates high-level instruction definitions into TPU machine code for SOPHGO chips (cv181x and bm1880v2 families). Built with CMake and Ninja, it outputs a shared library (libbmkernel.so) and static archive (libbmkernel-static.a), plus a readcmdbuf utility for command buffer inspection. The library exposes headers (bm_kernel.h, chip-specific variants) and serves as an intermediate layer between application code and TPU hardware execution.
**Chinese specificity:** SOPHGO is a Chinese semiconductor company specializing in AI accelerators and edge computing SoCs. cvikernel directly supports SOPHGO's TPU instruction set architecture (cv181x, bm1880v2), making it integral to the SOPHGO embedded AI ecosystem.
**Western equivalent:** NVIDIA CUDA (GPU kernel compilation), Qualcomm Hexagon SDK (DSP instruction generation), TensorFlow Lite Micro code generation — no single direct equivalent for TPU-specific instruction assembly.
**Maturity:** Experimental (★ 2, 8 forks, updated 2024-10)
**Language:** Bilingual CN-EN
**GitHub:** https://github.com/sophgo/cvikernel
---
