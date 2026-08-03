---
## unitreerobotics/xr_teleoperate [MODIFIÉ]
**Type:** Application
**Domain:** Robotics
**Relevance score:** 88/100
**Problem solved:** Enable real-time teleoperation of Unitree humanoid robots (H2, R1, G1 series) from XR headsets (Apple Vision Pro, Meta Quest, PICO) by mapping hand/arm pose from XR controllers to robot joint commands via a Python-based control stack.
**How it works:** The system runs on Ubuntu 20.04/22.04 with a Python 3.10 conda environment, using pinocchio for inverse kinematics and unitree_sdk2_python for robot communication. Core modules include teleimager (vision/pose estimation), teleop_hand_and_arm.py (main control loop), and support for multiple input modes (hand tracking, BrainCo controller). Supports both hardware robots and Isaac Lab simulation with configurable end-effectors (dex3, dex5) and arm types (G1_29, G1_23, H2, R1_A5, R1_A7).
**Chinese specificity:** Hosted on GitHub by unitreerobotics (Unitree Robotics, a Chinese humanoid robot manufacturer); the project is tightly coupled to Unitree's proprietary robot models and SDK ecosystem, with no broader Chinese standards or chipset vendor integration evident.
**Western equivalent:** OpenTeleVision (open-source teleoperation framework), Boston Dynamics' Spot teleoperation APIs (proprietary), Shadow Robot teleoperation stack
**Maturity:** Stable (★ 1585, 306 forks, updated 2026-07)
**Language:** Bilingual CN-EN
**GitHub:** https://github.com/unitreerobotics/xr_teleoperate
---
