---
## unitreerobotics/kinect_teleoperate
**Type:** Application
**Domain:** Robotics
**Relevance score:** 70/100
**Problem solved:** Enable teleoperation of Unitree H1/G1 humanoid robots using Azure Kinect DK camera for skeleton tracking and motion capture, bridging Microsoft's depth-sensing hardware with Unitree's robot control stack.
**How it works:** The system integrates Azure Kinect SDK (camera SDK v1.4.1 and body tracking SDK v1.1.2) running on Ubuntu 20.04 to capture RGB-D video and skeletal joint positions via k4abt_simple_3d_viewer. It translates detected human poses into robot joint commands for the H1/G1 platform. Dependencies include libk4a1.4, libk4abt1.1, CMake configuration files (k4abtConfig.cmake), and udev rules for USB 3.0 device access. The codebase is written in C++ with ROS integration (to be confirmed).
**Chinese specificity:** Hosted on Gitee/GitHub by unitreerobotics; no particular Chinese specificity beyond the author. Unitree Robotics is a Chinese manufacturer of quadruped and humanoid robots, but this project uses Microsoft Azure Kinect hardware and does not integrate Chinese-specific sensors, chipsets, or cloud platforms.
**Western equivalent:** Microsoft Azure Kinect samples (Microsoft), OpenPose + ROS teleoperation stacks (CMU/Facebook), Kinect v2 teleoperation frameworks (academic research)
**Maturity:** Experimental (★ 117, 28 forks, updated 2024-08)
**Language:** English
**GitHub:** https://github.com/unitreerobotics/kinect_teleoperate
---
