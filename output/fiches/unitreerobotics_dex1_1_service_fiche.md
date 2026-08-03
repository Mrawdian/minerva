---
## unitreerobotics/dex1_1_service
**Type:** Driver
**Domain:** Embedded
**Relevance score:** 62/100
**Problem solved:** Provides a serial-to-DDS bridge for the Unitree Dex1-1 parallel gripper (dual M4010 motors), enabling ROS 2 applications to command and monitor left/right finger positions via standardized DDS topics (rt/dex1/left/cmd, rt/dex1/right/cmd, etc.) instead of raw serial protocols.
**How it works:** C++ application that wraps libserialport (serial communication library) to interface with two M4010 motor controllers over UART, translating incoming DDS command messages into motor control frames and publishing motor state feedback as DDS topics. Includes calibration utility (dex1_1_gripper_server) for zero-point detection and systemd integration for automatic startup. Dependencies: libserialport 0.1.1, ROS 2 DDS middleware, C++17 compiler.
**Chinese specificity:** Hosted on Gitee by unitreerobotics, the robotics division of Unitree Robotics (Chinese quadruped/humanoid robot manufacturer). The Dex1-1 gripper and M4010 motor are proprietary Unitree hardware components; no integration with Chinese cloud platforms or standards detected.
**Western equivalent:** No known direct equivalent — specific to Unitree's proprietary gripper hardware and motor protocol; comparable in scope to vendor-supplied ROS 2 drivers for industrial grippers (e.g., Schunk, OnRobot) but not a general-purpose framework.
**Maturity:** Active (★ 19, 5 forks, updated 2026-07)
**Language:** Bilingual CN-EN
**GitHub:** https://github.com/unitreerobotics/dex1_1_service
---
