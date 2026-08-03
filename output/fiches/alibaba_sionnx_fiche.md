---
## alibaba/sionnx
**Type:** Tool
**Domain:** Edge AI
**Relevance score:** 64/100
**Problem solved:** Automate the generation of ONNX conformance tests to validate operator implementation in heterogeneous runtimes.
**How it works:** SIONNX uses a DSL (Domain Specific Language) describing ONNX instructions, processed by a custom LLVM TableGen pipeline to generate Python unit tests. Generated tests can be exported in protobuf format for compatibility with multiple ONNX runtime frameworks. The system supports configurable profiling levels (smoke tests vs. full tests) and allows operator addition via .td files and numpy algorithms.
**Chinese specificity:** Originating from Alibaba's Sinian platform, a heterogeneous hardware acceleration infrastructure optimized for ML inference on cloud, edge computing, and Chinese IoT devices. Direct integration with Alibaba's performance optimization ecosystem for AI and big data applications.
**Western equivalent:** ONNX Model Zoo test generation, ONNX Runtime test suite, but without equivalent DSL/TableGen approach
**Maturity:** Experimental (★ 7, updated 2024-11)
**Language:** EN
**Gitee:** https://gitee.com/alibaba/sionnx
---
