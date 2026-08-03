---
## sophgo/cvibuilder
**Type:** Library
**Domain:** Embedded
**Relevance score:** 43/100
**Problem solved:** Define and parse the binary format of CVIMODEL files used by Sophgo's CV18xx TPU accelerators, enabling third-party tools and frameworks to serialize and deserialize neural network models for deployment on these SoCs.
**How it works:** The library provides data structure definitions and serialization/deserialization routines for CVIMODEL, the proprietary model container format for Sophgo's CV18xx TPU inference accelerators. Written in C/C++, it abstracts the binary layout of compiled neural networks, allowing integration with model conversion pipelines and runtime inference engines. The project targets Sophgo's CV18xx SoC family (CV1835, CV1838, etc.) and serves as a bridge between training frameworks and on-device TPU execution.
**Chinese specificity:** Sophgo is a Chinese semiconductor company specializing in edge AI and video processing SoCs; CV18xx is their proprietary TPU-equipped processor line. The CVIMODEL format is Sophgo's internal standard for neural network deployment on their hardware ecosystem.
**Western equivalent:** TensorFlow Lite schema (Google), ONNX Runtime model format (Microsoft/Facebook), TVM compiler intermediate representation — all provide model serialization for edge inference, but CVIMODEL is specific to Sophgo's TPU ISA.
**Maturity:** Experimental (★ 2, 7 forks, updated 2024-10)
**Language:** English
**GitHub:** https://github.com/sophgo/cvibuilder
---
