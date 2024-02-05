import time

import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32

from radiacode import RadiaCode


class RadiationPublisher(Node):

    def __init__(self):
        super().__init__('radiation_publisher')
        self.publisher_ = self.create_publisher(Float32, '/count_rate', 10)
        timer_period = 1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        print('will use USB connection')
        self.rc = RadiaCode()

    def timer_callback(self):

        self.count_rate = [v.count_rate for v in list(self.rc.data_buf()) if hasattr(v, 'count_rate')]
        
        msg = Float32()
        msg.data = sum(self.count_rate) / len(self.count_rate)
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: {round(msg.data, 5)}')
        time.sleep(1)

def main():

    rclpy.init()

    radiation_publisher = RadiationPublisher()

    rclpy.spin(radiation_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    radiation_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
