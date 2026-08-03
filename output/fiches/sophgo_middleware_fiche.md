---
## sophgo/middleware
**Type:** Library
**Domain:** Embedded
**Relevance score:** 62/100
**Problem solved:** Provide multimedia codec and image processing libraries for the CV18xx series SoC (CVITEK/SOPHGO processors), enabling video encoding/decoding, image scaling, and color space conversion without relying solely on vendor-proprietary closed-source implementations.
**How it works:** The middleware stack includes video codec libraries (H.264, H.265, JPEG), image processing modules (ISP, scaler, color conversion), and audio codec support. Written primarily in C with hardware abstraction layers for the CV18xx SoC family. Dependencies include kernel drivers and bootloader components specific to the CVITEK/SOPHGO platform. Targets embedded Linux deployments on CV1800, CV1812, and related variants.
**Chinese specificity:** SOPHGO (formerly CVITEK) is a Chinese fabless semiconductor company specializing in edge AI and multimedia SoCs. This middleware is the official support library for their CV18xx processor family, which is widely used in Chinese IoT, surveillance, and robotics applications.
**Western equivalent:** FFmpeg (multimedia codecs), GStreamer (multimedia framework), libx264/libx265 (video encoding) — though those are generic; no direct equivalent for CV18xx-specific hardware acceleration.
**Maturity:** Active (★ 6, 13 forks, updated 2026-04)
**Language:** English
**GitHub:** https://github.com/sophgo/middleware
---
