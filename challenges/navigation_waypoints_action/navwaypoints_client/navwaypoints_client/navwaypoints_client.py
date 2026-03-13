import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from geometry_msgs.msg import Point

from navwaypoints_interfaces.action import NavigateWaypoints

class WaypointClient(Node):
    def __init__(self):
        super().__init__('waypoint_client')
        
        # Initialize Action Client
        self._action_client = ActionClient(self, NavigateWaypoints, 'navigate_waypoints')
        
        # Timing and Tracking variables
        self.start_time = None
        self.tracked_waypoints = []

    def send_goal(self, waypoints):
        self.get_logger().info('Waiting for action server...')
        self._action_client.wait_for_server()

        # Create the goal message
        goal_msg = NavigateWaypoints.Goal()
        goal_msg.waypoints = waypoints

        self.get_logger().info('Sending goal with 4 waypoints...')
        
        # Record the exact start time
        self.start_time = self.get_clock().now()

        # Send the goal asynchronously
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Goal rejected by server!')
            return

        self.get_logger().info('Goal accepted! Robot is moving...')
        
        # Wait for the final result
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        p = feedback_msg.feedback.last_passed_waypoint
        point_tuple = (round(p.x, 3), round(p.y, 3)) # Round to avoid float precision issues
        
        # Only record time if this is the FIRST time we've seen this waypoint in feedback
        if point_tuple not in self.tracked_waypoints:
            self.tracked_waypoints.append(point_tuple)
            
            current_time = self.get_clock().now()
            duration = (current_time - self.start_time).nanoseconds / 1e9
            
            self.get_logger().info(
                f'--> Waypoint Reached at [X: {p.x:.2f}, Y: {p.y:.2f}]! Time elapsed: {duration:.2f}s'
            )

    def get_result_callback(self, future):
        result = future.result().result
        
        # Record final time
        end_time = self.get_clock().now()
        total_duration = (end_time - self.start_time).nanoseconds / 1e9
        
        self.get_logger().info(f'=== Navigation Complete! Server Status: {result.status} ===')
        self.get_logger().info(f'=== Total Mission Time: {total_duration:.2f} seconds ===')
        
        # Shut down node after completion
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    action_client = WaypointClient()
    
    # Define 4 target coordinates for the 2D map
    target_coords = [(1.0, 1.0), (2.0, -1.0), (0.0, 3.0), (0.0, 0.0)]
    
    # Convert tuples into geometry_msgs/Point objects
    waypoints = []
    for x, y in target_coords:
        p = Point()
        p.x = x
        p.y = y
        p.z = 0.0
        waypoints.append(p)
        
    action_client.send_goal(waypoints)
    rclpy.spin(action_client)

if __name__ == '__main__':
    main()