import rclpy
from rclpy.node import Node

from pyzbar.pyzbar import decode
import cv2
import serial
import time

cap = cv2.VideoCapture(0)

#import rospy
import cv2

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from pyzbar.pyzbar import decode

# class QRCodeDetectorNode:

class QRCodeDetectorNode(Node):

    def simple_subscriber(self):
        self.subscription = self.create_subscription(
            Image,
            '/stereo_right',
            self.listener_callback,
            10)
        self.subscription

    def __init__(self):
        super().__init__('qr_code_detector')
        #self.image_sub = rospy("/camera_1/image_raw", Image, self.callback)
        self.image_sub = self.create_subscription(Image, "stereo_right", self.callback)
        #self.image_sub = simple_subscriber(self)
        self.publisher_ = self.create_publisher(String, 'qr_code_detector_topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def callback(self,data):
        bridge = CvBridge()

        try:
            cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(e)

        (rows,cols,channels) = cv_image.shape
        
        image = cv_image

        resized_image = cv2.resize(image, (360, 640)) 

        gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
        thresh = 40
        img_bw = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)[1]

        #cv2.imshow("B&W Image", gray)
        #cv2.imshow("B&W Image /w threshold", img_bw)

        qr_result = decode(img_bw)

        #print (qr_result)
        
        qr_data = qr_result[0].data
        msg = String()
        msg.data = f'QR Data {qr_data}'
        self.publisher_.publish(msg)
        self.get_logger().info('QR Data: "%s"' % msg.data)

        (x, y, w, h) = qr_result[0].rect

        cv2.rectangle(resized_image, (x, y), (x + w, y + h), (0, 0, 255), 4)

        text = "{}".format(qr_data)
        cv2.putText(resized_image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.imshow("Camera output", resized_image)

        cv2.waitKey(5)

# def main(args=None):
# 	camera_1()
	
# 	try:
# 		rospy.spin()
# 	except KeyboardInterrupt:
# 		rospy.loginfo("Shutting down")
	
# 	cv2.destroyAllWindows()

def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = QRCodeDetectorNode()

    rclpy.spin(minimal_publisher)

    rclpy.shutdown()

if __name__ == '__main__':
    rospy.init_node('camera_read', anonymous=False)
    main()

if __name__ == '__main__':
    main()
