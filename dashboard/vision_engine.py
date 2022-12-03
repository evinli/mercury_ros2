import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class VisionEngine(Node):
    def __init__(self):
        super().__init__('vision_engine')
        # Create gps and image publisher objects
        self.publisher_ = self.create_publisher(String, 'gps', 10)
        self.publisher_img = self.create_publisher(Image, 'img', 10)

        # Create timer callback function
        # timer_period = 0.03  # Gives approx 30fps
        # self.timer = self.create_timer(timer_period, self.timer_callback)
        # self.i = 0

        # Open a video file to read from it:
        self.video_name = "/home/fizzer/ros2_ws/src/dashboard/sample_vid.mp4"
        self.video_reader = cv2.VideoCapture(self.video_name)
        self.bridge = CvBridge()
        self.publish_img()

    def publish_img(self):
        ret, frame = self.video_reader.read()
        while(ret):
            self.publisher_img.publish(self.bridge.cv2_to_imgmsg(frame))
            ret, frame = self.video_reader.read()

        self.get_logger().info('Publishing video frame')

    def timer_callback(self):
        # Publish gps data
        msg = String()
        msg.data = 'Hello world: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

        # Publish image data
        ret, frame = self.video_reader.read()
        if ret == True:
            self.publisher_img.publish(self.bridge.cv2_to_imgmsg(frame))
        self.get_logger().info('Publishing video frame')
    
def main(args=None):
    rclpy.init(args=args)

    vision_engine = VisionEngine()

    rclpy.spin(vision_engine)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    vision_engine.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()