---
## unitreerobotics/unitree_ros
**Type:** Framework
**Domain:** Robotics
**Relevance score:** 94/100
**Problem solved:** Provide ROS packages for simulation and low-level control (torque, position, angular velocity) of joint articulations for Unitree quadruped and humanoid robots (A1, B1, B2, G1, GO1, GO2, H1, H2, R1, Z1, etc.) via Gazebo, as well as a control interface compatible with real robots via unitree_ros_to_real.
**How it works:** ROS Melodic/Kinetic architecture with Gazebo8 simulation: URDF description packages for 19 robot models, joint controllers (unitree_controller, z1_controller) using ros-control (controller-interface, effort-controllers, joint-trajectory-controller), and simulation modules (unitree_gazebo, unitree_legged_control). Depends on unitree_legged_msgs (from unitree_ros_to_real) for communication. No NPU support or embedded inference — simulation and low-level control only.
**Chinese specificity:** Hosted on Gitee by unitreerobotics (Chinese manufacturer of quadruped and humanoid robots); no particular Chinese specificity beyond the author. No Chinese chipset vendor cited, no Chinese cloud integration (Baidu, Aliyun, etc.), no Chinese standard compliance detected.
**Western equivalent:** ROS Navigation Stack (Open Robotics), Gazebo (Open Robotics), Boston Dynamics Spot SDK (proprietary), ANYmal ROS packages (ANYbotics)
**Maturity:** Stable (★ 1494, 442 forks, updated 2026-07)
**Language:** EN
**GitHub:** https://github.com/unitreerobotics/unitree_ros
---
