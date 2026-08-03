---
## unitreerobotics/unitree_slam
**Type:** Library
**Domain:** Edge AI
**Relevance score:** 61/100
**Problem solved:** Provide a C++ interface and example code for integrating Unitree's proprietary SLAM system with Unitree quadruped robots (H1 series) over Ethernet, enabling developers to access localization and mapping data from the robot's onboard SLAM module.
**How it works:** The project is a thin C++ wrapper and CMake-based build system that links against Unitree's precompiled SLAM library (located in unitree_robotics/lib/). It includes a demo application (demo_h1) that connects to the robot via a specified Ethernet interface (e.g., eth0 on subnet 123.x.x.x) and presumably exposes SLAM pose/map outputs. Build relies on standard CMake and requires LD_LIBRARY_PATH configuration to locate the closed-source Unitree SLAM binary.
**Chinese specificity:** Hosted on Gitee by unitreerobotics (Unitree Robotics, a Chinese quadruped robotics manufacturer). The project is tightly coupled to Unitree's proprietary H1 humanoid robot platform and its closed-source SLAM stack; no integration with HiSilicon, Rockchip, or other Chinese chipset vendors is evident.
**Western equivalent:** ROS 2 Nav2 SLAM stack (Open Robotics), Cartographer (Google), LOAM (Ji Zhang et al.) — though those are open-source and hardware-agnostic, whereas this is a proprietary interface to Unitree's closed SLAM.
**Maturity:** Active (updated 2026-07)
**Language:** English
**GitHub:** https://github.com/unitreerobotics/unitree_slam
---
