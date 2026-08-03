---
## unitreerobotics/z1_ros
**Type:** Driver
**Domain:** Robotics
**Relevance score:** 62/100
**Problem solved:** Provide a ROS driver stack for the Unitree Z1 robotic arm, bridging the gap between the proprietary Z1 SDK (UDP-based communication) and MoveIt motion planning middleware through a hardware abstraction layer.
**How it works:** The package suite consists of z1_hw (MoveIt hardware interface exposing joint_trajectory_controller and gripper action server), z1_controller (direct arm control and SDK integration), z1_moveit_config (MoveIt configuration), z1_rviz (visualization), and z1_examples (usage demonstrations). Written in C++ and Python, it depends on ROS (unspecified version), MoveIt, and communicates with the Z1 arm via UDP. The z1_sdk package provides low-level UDP communication examples.
**Chinese specificity:** Hosted on Gitee/GitHub by unitreerobotics; no particular Chinese specificity beyond the author. Unitree Robotics is a Chinese robotics company, but this is a standard ROS integration package without ties to Chinese chipset vendors or standards.
**Western equivalent:** Universal Robots ROS driver, ABB ROS Industrial packages, Franka Emika Panda ROS interface
**Maturity:** Experimental (★ 43, 31 forks, updated 2024-12)
**Language:** English
**GitHub:** https://github.com/unitreerobotics/z1_ros
---
