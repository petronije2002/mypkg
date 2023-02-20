#!/usr/bin/env python3


import rclpy
from rclpy.node import Node
import cv2
import cv_bridge
import numpy
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import Twist

class Follower(Node):

    def __init__(self):


        super().__init__('follower')

        self.publisher_ = self.create_publisher(Twist,'/cmd_vel',15)
                                        
        self.subscriber = self.create_subscription(Image,'/camera1/image_raw', 
                                         self.image_callback,10)
    
        self.bridge = cv_bridge.CvBridge()
        #cv2.namedWindow("window", 1)

        self.twist = Twist()

    def image_callback(self, msg):
        image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) 
        # change below lines to map the color you wanted robot to follow
        # lower_yellow = numpy.array([ 10,  10,  10])

        # upper_yellow = numpy.array([255, 255, 250])

        lower_yellow = numpy.array( [25, 50, 70])

        upper_yellow = numpy.array( [35, 255, 255])

        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        
        h, w, d = image.shape
        search_top = 3*h/4-200
        search_bot = 3*h/4 + 120
        mask[0:int(search_top), 0:w] = 0
        mask[int(search_bot):h, 0:w] = 0
        M = cv2.moments(mask)
        if M['m00'] > 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.circle(image, (cx, cy), 20, (0,0,255), -1)
            # CONTROL starts
            err = cx - w/2
            self.twist.linear.x = 0.35
            self.twist.angular.z = -float(err) / 120.0
            self.publisher_.publish(self.twist)
            # CONTROL ends
        cv2.imshow("mask",mask)
        cv2.imshow("output", image)
        cv2.waitKey(3)

def main(args=None):
    rclpy.init(args=args)

    follower = Follower()

    rclpy.spin(follower)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    follower.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
