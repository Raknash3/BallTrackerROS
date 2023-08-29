#!/usr/bin/env python
# license removed for brevity

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

def main():
    bridge = CvBridge()

    #Initialize a publisher node
    rospy.init_node('tennis_ball_tracker_pub', anonymous=True)
    pub = rospy.Publisher('tennis_ball_image', Image, queue_size=10)
    rate = rospy.Rate(10)

    #Read video
    video_capture = cv2.VideoCapture('/home/ravi/catkin_ws/src/ros_basics_tutorials/src/assignments/assignment_3/tennis-ball-video.mp4')

    rospy.loginfo('Publishing video frame')
    #Convert each frame to an Image message and publish
    while not rospy.is_shutdown():
            ret, frame = video_capture.read()
            frame = cv2.resize(frame, (0,0), fx=0.5,fy=0.5)
            img_msg = bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            pub.publish(img_msg)
            rate.sleep()

    video_capture.release()
    rospy.spin() #To keep on publishing the video

main()