# 🤖 Autonomous Navigation Mini Challenge

Welcome to the Autonomous Navigation Mini Challenge! In this repository, you will find the base workspace required to complete the integration of an Action Server with the Nav2 stack. 

Your mission is to act as the systems integrator: build the "brain" of the robot to bridge high-level command requests with low-level navigation and mapping, utilizing a provided path-optimization algorithm.



## 📑 Table of Contents
- [Overview](#-overview)
- [System Architecture & Rules](#-system-architecture--rules)
- [Your Mission](#-your-mission)
- [Provided Tools](#-provided-tools)
- [Getting Started](#-getting-started)
- [How to Run](#-how-to-run)

---

## 📋 Overview

You are provided with three ROS2 packages, including an Action Client, an Action Server, and a predefined Action Interface. You need to put these three packages into the existing [Linorobot2 Repo](https://github.com/linorobot/linorobot2/tree/jazzy) src to start.

Your goal is to implement the **Action Server**, integrate the waypoint optimizer, and tune the **SLAM/Nav2 stack** so the robot can smoothly and efficiently execute the optimized route without violating physical constraints.

---

## 🏗️ System Architecture & Rules

To ensure a level playing field, certain parts of the system are strictly locked (Do Not Modify). Focus your engineering efforts entirely on the Action Server logic and navigation tuning.

### Modifiability Matrix

| Component | Status | Description |
| :--- | :---: | :--- |
| **Action Client** | 🔒 **LOCKED** | Initiates the task and sends the goal. Do not modify. |
| **Action Interfaces** | 🔒 **LOCKED** | The `.action` files defining the structure of the goal, feedback, and result. |
| **Robot Physics/Kinematics** | 🔒 **LOCKED** | Start point, max/min velocity, acceleration, mass, inertia, and any other physics properties. |
| **Action Server** | 🛠️ **MODIFIABLE** | **Your core deliverable.** Implement your state machine and logic here. |
| **SLAM & Nav2 Stack** | 🛠️ **MODIFIABLE** | Tune parameters (costmaps, planners, inflation radii) to ensure efficient movement. |

> **⚠️ STRICT RULE:** You may not "cheat" the physics. Altering the robot's physical constraints (e.g., cranking up max velocity, modifying inertia) or manually changing the starting pose is strictly prohibited and will result in a failed evaluation. Your performance relies purely on efficient software integration and parameter tuning.

---

## 🚀 Your Mission

Your primary task is to modify the Action Server node (navwaypoints_server) and tune the navigation stack configurations. 

Your Action Server must successfully:
1. **Receive Goal & Send Feedback, Result:** Accept the goal from the fixed Action Client, and send back feedback and result.
2. **Optimize the Route:** Pass the necessary target data into the provided **Waypoint Optimizer Function** to calculate the best sequence of waypoints.
3. **Execute the Sequence:** Communicate the waypoints sequentially to the Nav2 stack.
4. **Return Feedback & Result:** Pipe standard progress feedback and the final completion result back to the Action Client using the locked Action Interfaces.

Below is the structure of the action interface:
- Request: geometry_msgs/Point[4] waypoints (Array of exactly 4 coordinates for the 2D map)
- Feedback: geometry_msgs/Point last_passed_waypoint (The latest coordinate the robot just passed through)
- Result: int32 status (Server should send 1 when all coordinates are successfully completed)

---

## 💻 Getting Started

### Installation

1. Create a workspace and clone the repository
   ```bash
   cd ~/linorobot2  # navigate to linorobot2 directory
   git clone https://github.com/linorobot/academy.git 
   cd ~/linorobot2/academy/challenges  # you can see the provided packages here
   ```

2. Make your modification
   ```bash
   cd ~/linorobot2/academy/challenges/navigation_waypoints_action/
   ```

4. Build and run (do it in your docker!)
   ```bash
   cd ~/linorobot2
   colcon build
   source install/setup.bash
   # Run your tasks
   ```
