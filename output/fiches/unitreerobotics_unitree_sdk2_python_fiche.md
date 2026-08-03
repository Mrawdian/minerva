---
## unitreerobotics/unitree_sdk2_python
**Type:** Library
**Domain:** Robotics
**Relevance score:** 72/100
**Problem solved:** Provides a Python binding layer for Unitree's quadruped robot control SDK2, enabling high-level (sport mode, trajectory tracking, attitude control) and low-level (joint PID, motor torque) motor commands over Ethernet via CycloneDDS middleware, eliminating the need to write C++ bindings manually.
**How it works:** Python 3.8+ wrapper around unitree_sdk2 using CycloneDDS 0.10.2 as the DDS middleware for inter-process communication. Core dependencies: numpy, opencv-python. Exposes two control layers: high-level API (StandUpDown, VelocityMove, BalanceAttitude, TrajectoryFollow, SpecialMotions) and low-level API (joint state readout, motor PID control with kp/kd gains, IMU/battery telemetry). Examples include publisher/subscriber patterns, wireless controller status polling, and front camera frame capture via OpenCV.
**Chinese specificity:** Hosted on GitHub by unitreerobotics (Unitree Robotics, a Chinese quadruped robotics manufacturer). No particular Chinese chipset vendor or standard compliance cited; the project is a Python interface to Unitree's proprietary SDK2 for their Go1/Go2 robot platforms.
**Western equivalent:** Boston Dynamics' Spot SDK (Python), ANYmal ROS2 driver stack, Clearpath Robotics Warthog SDK
**Maturity:** Stable (★ 750, 312 forks, updated 2026-07)
**Language:** English
**GitHub:** https://github.com/unitreerobotics/unitree_sdk2_python
---
