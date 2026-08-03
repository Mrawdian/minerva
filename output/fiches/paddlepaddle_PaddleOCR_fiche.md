---
## paddlepaddle/PaddleOCR [MODIFIÉ]
**Type:** Library
**Domain:** Embedded
**Relevance score:** 71/100
**Problem solved:** Convert PDF documents and images into structured, LLM-ready data (JSON/Markdown) with high accuracy. Provide multilingual OCR (100+ languages) and document layout parsing for RAG and agentic AI applications without relying on closed-source commercial solutions.
**How it works:** PaddleOCR comprises three main components: PP-OCRv6 (text detection and recognition engine supporting 50 languages in a unified model), PaddleOCR-VL-1.6 (0.9B lightweight vision-language model for document parsing achieving 96.3% accuracy on OmniDocBench), and PP-StructureV3 (structure-aware PDF/image-to-Markdown/JSON converter with fine-grained coordinate extraction). Built on PaddlePaddle deep learning framework (Python/C++), it supports inference on NVIDIA GPU, Intel CPU, Kunlunxin XPU, and other AI accelerators. Output formats include Markdown and JSON with table cell and text coordinates.
**Chinese specificity:** Developed by Baidu's PaddlePaddle team; PaddlePaddle is Baidu's open-source deep learning framework widely adopted in the Chinese AI ecosystem. Integration with Kunlunxin XPU (Chinese AI accelerator) is explicitly supported. No mandatory Chinese standard compliance cited.
**Western equivalent:** Tesseract (open-source OCR engine), EasyOCR (Python library), Docling (IBM, document parsing), PyMuPDF (PDF extraction)
**Maturity:** Stable (★ 4335, 1094 forks, updated 2026-06)
**Language:** Bilingual CN-EN
**Gitee:** https://gitee.com/paddlepaddle/PaddleOCR
---
