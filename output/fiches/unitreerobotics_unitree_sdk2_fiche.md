---
## unitreerobotics/unitree_sdk2
**Type:** Library
**Domain:** Edge AI
**Relevance score:** 75/100
**Problem solved:** Provide a unified C++ SDK for controlling Unitree quadruped robots (Go1, Go2, B1, H1 series) across heterogeneous compute platforms (aarch64, x86_64) without requiring proprietary closed-source libraries or vendor-specific toolchains.
**How it works:** The SDK is a C++ library built on CMake, depending on libyaml-cpp, Eigen3, Boost, spdlog, and libfmt. It abstracts robot hardware interfaces (motor control, IMU, joint feedback) and provides high-level APIs for locomotion, state queries, and sensor access. Targets Ubuntu 20.04 LTS with GCC 9.4.0; examples show integration via CMake's find_package() mechanism. No RTOS kernel is embedded; the library runs on standard Linux.
**Chinese specificity:** Unitree Robotics is a Chinese manufacturer of quadruped robots (Go1, Go2, B1, H1) headquartered in Hangzhou; this SDK is the official second-generation control interface for their product line. No integration with Chinese cloud platforms (Baidu, Alibaba) or cellular standards (NB-IoT, 5G) is documented.
**Western equivalent:** Boston Dynamics Spot SDK (proprietary), ANYmal ROS2 driver stack (ETH Zurich), Clearpath Robotics Warthog SDK
**Maturity:** Stable (★ 1258, 367 forks, updated 2026-07)
**Language:** English
**GitHub:** https://github.com/unitreerobotics/unitree_sdk2
---
