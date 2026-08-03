---
## unitreerobotics/unilidar_sdk2
**Type:** Library
**Domain:** Embedded
**Relevance score:** 62/100
**Problem solved:** Provide a unified C++ SDK and ROS/ROS2 integration layer for the Unitree L2 LiDAR to acquire point cloud and IMU data, configure sensor parameters, and publish data to robotics middleware without proprietary closed-source drivers.
**How it works:** The SDK consists of three main components: a core C++ library (unitree_lidar_sdk) that communicates with the L2 LiDAR over UDP or serial port to retrieve point cloud frames and IMU samples, a ROS wrapper (unitree_lidar_ros) that publishes sensor_msgs/PointCloud2 and sensor_msgs/Imu topics, and a ROS2 equivalent (unitree_lidar_ros2) for ROS2 environments. The library exposes interfaces for setting working modes (FOV switching, IMU enable/disable), retrieving calibration parameters, and handling coordinate frame transformations between the LiDAR and IMU coordinate systems. Dependencies include CMake, ROS/ROS2 core libraries, and standard C++11.
**Chinese specificity:** Hosted on Gitee/GitHub by unitreerobotics; no particular Chinese specificity beyond the author. Unitree Robotics is a Chinese robotics company, but the L2 LiDAR and SDK follow standard sensor interfaces (UDP/serial, ROS/ROS2 middleware) without integration to Chinese cloud platforms or proprietary standards.
**Western equivalent:** ROS drivers for Velodyne/Ouster LiDARs, livox_ros_driver (DJI), SICK LiDAR ROS packages
**Maturity:** Experimental (★ 93, 58 forks, updated 2025-03)
**Language:** Bilingual CN-EN
**GitHub:** https://github.com/unitreerobotics/unilidar_sdk2
---
