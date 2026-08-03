---
## Sipeed/MaixCDK
**Type:** Framework
**Domain:** Edge AI
**Relevance score:** 63/100
**Problem solved:** Provide a unified C/C++ SDK for rapid development of AI inference, machine vision, and IoT applications on Sipeed Maix series boards and Linux platforms, eliminating the need to integrate separate libraries for neural network acceleration, OpenCV, and peripheral I/O.
**How it works:** MaixCDK is a C/C++ wrapper library that abstracts hardware-accelerated AI execution (classification, detection, segmentation), vision algorithms (color detection, QR/AprilTag recognition, line following), OpenCV integration, and peripheral interfaces (UART, I2C, SPI, GPIO, PWM, ADC, camera, display). It targets Sipeed MaixCAM and MaixCAM-Pro boards (based on unspecified SoCs) and generic Linux. Build system uses one-click compilation; online debugging is supported. A Python counterpart (MaixPy) maintains synchronized APIs.
**Chinese specificity:** Sipeed is a Chinese embedded systems vendor specializing in RISC-V and AI accelerator boards; MaixCDK is their primary C/C++ development framework for the Maix product line. The project integrates with MaixVision (IDE) and MaixHub (application marketplace), forming a closed ecosystem around Sipeed hardware.
**Western equivalent:** OpenCV (computer vision), TensorFlow Lite (inference), Arduino/mbed (peripheral abstraction), but no single Western project combines all three with hardware acceleration for a specific board family.
**Maturity:** Active (★ 1, updated 2026-07)
**Language:** Bilingual CN-EN
**Gitee:** https://gitee.com/Sipeed/MaixCDK
---
