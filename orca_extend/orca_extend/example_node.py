import rclpy
from rclpy.node import Node

from std_msgs.msg import String

from sensor_msgs.msg import Image

import cv2
from cv_bridge import CvBridge, CvBridgeError
from pyzbar.pyzbar import decode

class ExampleNode(Node):

    def __init__(self):
        super().__init__('example_node')
        self.publisher_ = self.create_publisher(String, 'example_topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            Image,
            '/stereo_right', 
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, img):
        bridge = CvBridge()

        try:
            cv_image = bridge.imgmsg_to_cv2(img, desired_encoding="bgr8")
        except CvBridgeError as e:
            self.get_logger().error(e)

        image = cv_image
        cv2.imshow("Camera output normal", image)
        # cv2.waitKey(3)

        resized_image = cv2.resize(image, (360, 640))

        gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
        thresh = 40
        img_bw = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)[1]

        qr_result = decode(img_bw)

        if len(qr_result)>0:
            print(qr_result[0].data)
            
        # qr_data = qr_result[0].data
        print(qr_result)


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    minimal_subscriber.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
