---
## alibaba/AliOS-Things
**Type:** RTOS
**Domain:** IoT
**Relevance score:** 75/100
**Problem solved:** Provide a scalable and modular real-time operating system specifically designed for IoT devices with limited resources, supporting multiple CPU architectures and natively integrating network connectivity and security.
**How it works:** AliOS Things uses a layered architecture composed of a Rhino RTOS kernel, a HAL layer abstracting hardware (WiFi, Bluetooth, I2C, SPI, UART, Flash), a lightweight network stack (LwIP, BLE, LoRaWAN) and a security layer (TLS, ID2, TEE). Components are managed via YAML configuration enabling modular selection of features, with unified VFS support for drivers and standardized APIs for applications.
**Chinese specificity:** Native integration with Alibaba Cloud ecosystem (LinkSDK, diagnostic and bootstrap services), support for Chinese standards via LoRaWAN components and WiFi configuration solutions adapted to the local market, with documentation and examples oriented toward Alibaba hardware platforms (HaaS100, HaaS EDU K1, HaaS200).
**Western equivalent:** FreeRTOS, Zephyr Project, RIOT OS
**Maturity:** Experimental (★ 1, 2 forks, updated 2024-11)
**Language:** Bilingual CN-EN
**Gitee:** https://gitee.com/alibaba/AliOS-Things
---
