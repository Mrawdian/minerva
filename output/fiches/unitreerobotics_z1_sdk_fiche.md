---
## unitreerobotics/z1_sdk
**Type:** Framework
**Domain:** Robotics
**Relevance score:** 56/100
**Problem solved:** Provide a software development kit for controlling the Unitree Z1 robot arm, enabling users to interface with the robot's actuators, sensors, and kinematics through a standardized API rather than reverse-engineering proprietary communication protocols.
**How it works:** The SDK exposes control interfaces for the Z1 robot arm (a 6-DOF manipulator) through C++ and Python bindings. It abstracts low-level motor control, joint feedback, and inverse kinematics computation. The project references official Unitree documentation (English and Chinese) but the README excerpt does not detail specific dependencies, communication protocols (CAN/Ethernet/proprietary), or whether it wraps a closed-source firmware layer.
**Chinese specificity:** Hosted on Gitee by unitreerobotics (Unitree Robotics, a Chinese robotics manufacturer based in Hangzhou). Unitree is known for quadruped and manipulator platforms in the Chinese robotics ecosystem; no explicit integration with Chinese cloud platforms or chipset vendors is documented.
**Western equivalent:** MoveIt (ROS-based manipulation planning), Universal Robots URScript (proprietary UR arm SDK), FANUC ROBOGUIDE SDK
**Maturity:** Experimental (★ 45, 39 forks, updated 2025-09)
**Language:** English
**GitHub:** https://github.com/unitreerobotics/z1_sdk
---
