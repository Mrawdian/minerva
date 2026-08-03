---
## alibaba/iot_remote_access
**Type:** Application
**Domain:** IoT
**Relevance score:** 71/100
**Problem solved:** Provides secure remote access to IoT devices without public IP address, enabling SSH, web shell, file access, and network tunneling across the Internet.
**How it works:** The device-side daemon establishes a persistent WebSocket connection to Alibaba Cloud IoT servers to create a bidirectional communication channel. The architecture supports remote SSH, a browser-based web shell, file navigation with upload/download, and Windows RDP tunneling via this encrypted channel. The system compiles into static or dynamic binaries for multiple architectures (x86_64, ARM v7, macOS) with cloud control support to enable/disable maintenance channels.
**Chinese specificity:** Native integration with Alibaba Cloud IoT ecosystem and Link IoT Edge, proprietary Chinese IoT management platform. Designed for devices deployed in China without direct access to public Internet, using Alibaba cloud infrastructure as central relay point.
**Western equivalent:** No known direct equivalent - combines ngrok/Cloudflare Tunnel functionality with a proprietary IoT daemon, but without a Western open-source equivalent offering this complete cloud integration for IoT
**Maturity:** Experimental (updated 2024-11)
**Language:** Bilingual CN-EN
**Gitee:** https://gitee.com/alibaba/iot_remote_access
---
