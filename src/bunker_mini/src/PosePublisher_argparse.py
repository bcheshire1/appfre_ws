import rclpy
from rclpy.node import Node
import argparse
import math
import time
from transformations import quaternion_from_euler


from geometry_msgs.msg import PoseStamped
from action_msgs.msg import GoalStatusArray

class PosePublisher(Node):
    def __init__(self, x_pos, y_pos, yaw):
        super().__init__('pose_publisher')
        self.publisher = self.create_publisher(PoseStamped, '/goal_pose', 10)
        self.timer = self.create_timer(3, self.timer_callback)

        # Set the orientation using Euler angles
        # yaw_angle = math.radians(yaw)
        self.quaternion = quaternion_from_euler(0.0, 0.0, yaw)

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = 0.0

        self.goal_status_subscriber = self.create_subscription(
            GoalStatusArray,
            '/follow_path/_action/status',
            self.goal_status_callback,
            10
        )

    def timer_callback(self):
        pose_msg = PoseStamped()
        pose_msg.header.stamp = self.get_clock().now().to_msg()
        pose_msg.header.frame_id = 'map'
        pose_msg.pose.position.x = self.x_pos
        pose_msg.pose.position.y = self.y_pos
        pose_msg.pose.position.z = self.z_pos
        pose_msg.pose.orientation.x = 0.0
        pose_msg.pose.orientation.y = 0.0
        pose_msg.pose.orientation.z = self.quaternion[3]
        pose_msg.pose.orientation.w = 1.0

        # Log quaternion components
        # self.get_logger().info(f'Quaternion components: x={self.quaternion[0]}, y={self.quaternion[1]}, z={self.quaternion[2]}, w={self.quaternion[3]}')


        # Publish the data
        self.publisher.publish(pose_msg)
        position_data = f'x: {pose_msg.pose.position.x}, y: {pose_msg.pose.position.y}, yaw: {pose_msg.pose.orientation.z}'
        self.get_logger().info(f'Published PoseStamped message at position: {position_data}')
    
    def goal_status_callback(self, msg):
        # Code from here until the main function is the goal status subscriber
        # msg is the GoalStatusArray message type
        status_list = msg.status_list
        if status_list:
            final_goal_status = status_list[-1]

            # Get the status attribute of the message
            if hasattr(final_goal_status, 'status'):
                status_string = int(final_goal_status.status)

                # If the robot has reached the goal, stop publishing
                if status_string == 4 or status_string == 6:
                    print("Goal reached, stopping publisher")
                    Node.destroy_node(self)
                    rclpy.shutdown()
            else:
                print("The 'status' attribute is not present in the final GoalStatus object.")
        else:
            print("The status_list is empty.")

def main(args=None):
    parser = argparse.ArgumentParser(description='Pose Publisher Script')
    parser.add_argument('--x', type=float, default=0.0, help='X coordinate of the pose')
    parser.add_argument('--y', type=float, default=0.0, help='Y coordinate of the pose')
    parser.add_argument('--a', type=float, default=0.0, help='Angle of the pose in degrees (0 degrees is up)')

    args = parser.parse_args()

    # Convert the angle from degrees to radians
    args.a = math.radians(args.a)

    rclpy.init(args=None)
    pose_publisher = PosePublisher(args.x, args.y, args.a)

    try:
        while rclpy.ok():
            rclpy.spin_once(pose_publisher, timeout_sec=0.1)

        print("Node stopped. Exiting the script.")

    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Shutting down.")

    pose_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()