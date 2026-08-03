---
## unitreerobotics/unitree_actuator_sdk
**Type:** Library
**Domain:** Edge AI
**Relevance score:** 64/100
**Problem solved:** Provide a C++/Python SDK for controlling Unitree actuators (GO-M8010-6, A1, B1 motors) over serial communication, handling motor-side vs. output-side coordinate transformations and gear ratio conversions that are non-trivial for robotics applications.
**How it works:** The SDK exposes motor control via C++ classes and Python bindings, supporting serial communication with Unitree motors. Core components include motor type enumerations (MotorType::A1, MotorType::B1), control modes (FOC), and command structures (cmd, data) with fields for proportional/derivative gains (kp, kd), position (q), velocity (dq), and torque (tau). Build system uses CMake; requires gcc ≥5.4.0 (x86) or ≥7.5.0 (ARM). Examples demonstrate rotor-to-output coordinate conversion using gear ratio scaling formulas.
**Chinese specificity:** Hosted on Gitee/GitHub by unitreerobotics; no particular Chinese specificity beyond the author. Unitree Robotics is a Chinese robotics company, but the SDK targets their proprietary motor hardware rather than a Chinese chipset vendor or standard.
**Western equivalent:** No known direct equivalent — specific combination of serial-based motor control SDK with rotor/output-side coordinate transformation for quadruped/legged robot actuators.
**Maturity:** Experimental (★ 132, 39 forks, updated 2025-01)
**Language:** English
**GitHub:** https://github.com/unitreerobotics/unitree_actuator_sdk
---
