---
## unitreerobotics/point_lio_unilidar
**Type:** Application
**Domain:** Edge AI
**Relevance score:** 71/100
**Problem solved:** Adapt the Point-LIO lidar-inertial odometry algorithm to work with Unitree's L1 and L2 LiDAR sensors (360° × 90° FOV, non-repetitive scanning) for low-speed mobile robot localization and mapping under vibration and aggressive motion.
**How it works:** ROS Noetic application wrapping the Point-LIO algorithm with sensor drivers for Unitree L1 (via unilidar_sdk) and L2 (via unilidar_sdk2). Uses Eigen for linear algebra, PCL for point cloud processing, and IMU fusion for odometry estimation. Outputs pose estimates and 3D maps (PCD format) via ROS topics; tested on Ubuntu 20.04 with provided rosbag datasets for offline validation.
**Chinese specificity:** Hosted on GitHub by unitreerobotics (Unitree Robotics, a Chinese quadruped robot and sensor manufacturer); integrates proprietary Unitree LiDAR hardware (L1, L2) and their SDKs, but no compliance with Chinese standards or domestic cloud services documented.
**Western equivalent:** Fast-LIO2 (HKU-MARS), LOAM (Ji Zhang), Cartographer (Google)
**Maturity:** Experimental (★ 505, 94 forks, updated 2025-06)
**Language:** English
**GitHub:** https://github.com/unitreerobotics/point_lio_unilidar
---
