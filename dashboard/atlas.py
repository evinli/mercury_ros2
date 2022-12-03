import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class Atlas(Node):
    def __init__(self):
        super().__init__('atlas')
        self.subscription = self.create_subscription(String, 'gps', self.gps_callback, 10)
        self.subscription_img = self.create_subscription(Image, 'img', self.img_callback, 10)
        self.subscription  # prevent unused variable warning
        self.subscription_img  # prevent unused variable warning

        self.bridge = CvBridge()

    def gps_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)
    
    def img_callback(self, data):
        self.get_logger().info('Receiving video frame')
        current_frame = self.bridge.imgmsg_to_cv2(data)
        cv2.imshow("frame", current_frame)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)

    atlas = Atlas()

    rclpy.spin(atlas)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    atlas.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()