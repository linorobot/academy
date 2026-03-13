#!/usr/bin/env python3

import time
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from geometry_msgs.msg import Point
from navwaypoints_interfaces.action import NavigateWaypoints

class WaypointServer(Node):
    def __init__(self):
        super().__init__('waypoint_server')
        
        # Initialize the Action Server
        self._action_server = ActionServer(
            self,
            NavigateWaypoints,
            'navigate_waypoints',
            self.execute_callback
        )
        self.get_logger().info('Waypoint Action Server is up and waiting for goals...')

    def execute_callback(self, goal_handle):
        self.get_logger().info('Received new navigation goal!')
        
        # Extract the array of 4 waypoints from the request
        waypoints = goal_handle.request.waypoints
        
        feedback_msg = NavigateWaypoints.Feedback()
        
        # Loop through each of the 4 waypoints
        for i, target_point in enumerate(waypoints):
            self.get_logger().info(f'Navigating to Waypoint {i+1}: [X: {target_point.x:.2f}, Y: {target_point.y:.2f}]')
            
            # --- REPLACE THIS BLOCK LATER ---
            # Simulate the time it takes the robot to drive to the point
            time.sleep(3.0) 
            # --------------------------------
            
            self.get_logger().info(f'Reached Waypoint {i+1}!')
            
            # Populate and send the feedback back to the client
            feedback_msg.last_passed_waypoint = target_point
            goal_handle.publish_feedback(feedback_msg)

        # Once all 4 waypoints are completed, mark the goal as successful
        goal_handle.succeed()
        
        # Populate and return the final result
        result = NavigateWaypoints.Result()
        result.status = 1  # 1 indicates success based on your design
        
        self.get_logger().info('All waypoints reached. Sending final result.')
        return result

def main(args=None):
    rclpy.init(args=args)
    action_server = WaypointServer()
    
    try:
        rclpy.spin(action_server)
    except KeyboardInterrupt:
        pass
    finally:
        action_server.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()