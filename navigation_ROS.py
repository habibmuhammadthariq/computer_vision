#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
import simple_find_contours as fc


def callback(data):
    bridge = CvBridge()
    # get images from camera
    try:
        cv_img = bridge.imgmsg_to_cv2(data, 'bgr8')
    except CvBridgeError as e:
        print(e)

    detected_image = fc.extract(cv_img, True)
    direction, distance = fc.get_direction()
    print("Next destination : {}".format(direction))

    cv2.imshow('Detected Image', detected_image)
    cv2.waitKey(1)

    # publish detected object
    try:
        img_pub.publish(bridge.cv2_to_imgmsg(detected_image, 'bgr8'))
    except CvBridgeError as e:
        print(e)


def drone_navigation():
    global img_pub

    rospy.init_node('drone_navigation', anonymous=True)
    rospy.Subscriber('/webcam', Image, callback)
    img_pub = rospy.Publisher('/detected_object', Image, queue_size=1)
    rospy.spin()


if __name__ == '__main__':
    try:
        drone_navigation()
    except rospy.ROSInterruptException:
        pass
