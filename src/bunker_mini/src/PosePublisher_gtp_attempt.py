import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from action_msgs.msg import GoalStatusArray

class PosePublisher(Node):

    def __init__(self):
        super().__init__('pose_publisher')
        self.publisher = self.create_publisher(PoseStamped, '/goal_pose', 10)
        self.timer = self.create_timer(3, self.timer_callback)
        self.x_pos = 0.0
        self.y_pos = -1.0
        self.z_pos = 0.0

        # Adding subscriber for goal status
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
        pose_msg.pose.orientation.z = 0.0
        pose_msg.pose.orientation.w = 1.0

        self.publisher.publish(pose_msg)
        position_data = f'x: {pose_msg.pose.position.x}, y: {pose_msg.pose.position.y}'
        self.get_logger().info(f'Published PoseStamped message at position: {position_data}')

    def goal_status_callback(self, msg):
        # Assuming msg is your GoalStatusArray object
        status_list = msg.status_list
        if status_list:
            final_goal_status = status_list[-1]

            # Assuming status is an attribute of GoalStatus
            if hasattr(final_goal_status, 'status'):
                status_string = int(final_goal_status.status)
                print(f"Goal not reached yet, publishing again...")
                if status_string == 4 or status_string == 6:
                    print("Goal reached, stopping publisher")
                    Node.destroy_node(self)
                    rclpy.shutdown()
            else:
                print("The 'status' attribute is not present in the final GoalStatus object.")
        else:
            print("The status_list is empty.")


def main(args=None):
    rclpy.init(args=args)

    pose_publisher = PosePublisher()

    try:
        while rclpy.ok():
            rclpy.spin_once(pose_publisher, timeout_sec=0.1)

        print("Node stopped. Exiting the script.")

    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Shutting down.")

    # Destroy the node explicitly
    pose_publisher.destroy_node()

    # Shutdown the ROS 2 system
    rclpy.shutdown()

if __name__ == '__main__':
    main()