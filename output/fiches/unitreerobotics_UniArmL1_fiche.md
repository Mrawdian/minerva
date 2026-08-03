---
## unitreerobotics/UniArmL1
**Type:** Framework
**Domain:** Edge AI
**Relevance score:** 71/100
**Problem solved:** Provide a lightweight 6-DOF robotic arm teleoperation framework with standardized data collection for imitation learning. Enables seamless integration of VR controller, keyboard, and leader-follower control modes with synchronized multi-camera recording at fixed frequency for downstream training pipelines.
**How it works:** Python-based teleoperation stack supporting three input modes (VR via XRoboToolkit, keyboard, leader-follower) communicating with arm firmware over serial (default /dev/ttyACM1). Data collection records joint angles and camera frames at configurable Hz (default 50 Hz) in standardized format compatible with unitree_lerobot (HuggingFace LeRobot fork). Uses URDF for kinematics, Meshcat for optional visualization, and conda for dependency management. Requires hardware BOM and 3D-printed components documented separately.
**Chinese specificity:** Hosted on GitHub by unitreerobotics (Unitree Robotics, a Chinese quadruped/robotic systems company). No specific chipset vendor or Chinese standard compliance documented; the project is a software framework for a custom 6-DOF arm design derived from open-source SO-ARM100 hardware.
**Western equivalent:** LeRobot (HuggingFace), DOPE (NVIDIA), Mobile ALOHA (Stanford)
**Maturity:** Active (★ 11, 4 forks, updated 2026-05)
**Language:** Bilingual CN-EN
**GitHub:** https://github.com/unitreerobotics/UniArmL1
---
