---
## unitreerobotics/digital_servo
**Type:** Documentation
**Domain:** Embedded
**Relevance score:** 65/100
**Problem solved:** Provide reference implementations for communicating with Unitree J288/S288 brushless joint servos over a half-duplex TTL bus (6 Mbps, 8N1). Enables both PC-based testing via serial terminal and embedded integration on STM32 microcontrollers without relying on proprietary closed-source drivers.
**How it works:** Two independent implementations share a common protocol specification (20-byte control packets, 26-byte feedback packets, CRC32 validation, fixed-point conversion). Python implementation provides an interactive serial terminal for debugging on PC; STM32 implementation is a Keil MDK project targeting STM32F413RGT6 with HAL integration. Protocol defines 16-node bus addressing (0–15), fixed 6 Mbps baudrate, and 288.35:1 gear ratio conversion formulas.
**Chinese specificity:** Hosted on Gitee by unitreerobotics, the robotics division of Unitree Robotics (Chinese quadruped robot manufacturer). Targets Unitree's proprietary digital servo hardware; no integration with Chinese cloud platforms or standards bodies detected.
**Western equivalent:** No known direct equivalent — specific to Unitree servo protocol; comparable in scope to vendor-supplied communication libraries for proprietary actuators (e.g., Dynamixel protocol documentation by Robotis).
**Maturity:** Active (★ 1, updated 2026-07)
**Language:** Bilingual CN-EN
**GitHub:** https://github.com/unitreerobotics/digital_servo
---
