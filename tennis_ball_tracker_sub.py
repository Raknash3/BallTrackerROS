#!/usr/bin/env python
# license removed for brevity

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge,CvBridgeError
import cv2
import numpy as np
import sys

bridge = CvBridge()

def filter_color(rgb_image, lower_bound_color, upper_bound_color):
    #convert the image into the HSV color space
    hsv_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2HSV)
    cv2.imshow("hsv image",hsv_image)

    #find the upper and lower bounds of the yellow color (tennis ball)
    yellowLower =(30, 150, 100)
    yellowUpper = (50, 255, 255)

    #define a mask using the lower and upper bounds of the yellow color 
    mask = cv2.inRange(hsv_image, lower_bound_color, upper_bound_color)

    return mask


#A function to get the contours from the binary image. 
def getContours(binary_image):      
    #_, contours, hierarchy = cv2.findContours(binary_image, 
    #                                          cv2.RETR_TREE, 
    #                                           cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(binary_image.copy(), 
                                            cv2.RETR_EXTERNAL,
	                                        cv2.CHAIN_APPROX_SIMPLE)
    return contours

#A function to draw the contours over the video frames
def draw_ball_contour(binary_image, rgb_image, contours):
    black_image = np.zeros([binary_image.shape[0], binary_image.shape[1],3],'uint8')
    
    for c in contours:
        area = cv2.contourArea(c)
        perimeter= cv2.arcLength(c, True)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        #The higher the area value the more strict the program will be with detecting the ball.
        if (area>750):
            cv2.drawContours(rgb_image, [c], -1, (150,250,150), 1)
            cv2.drawContours(black_image, [c], -1, (150,250,150), 1)
            cx, cy = get_contour_center(c)
            cv2.circle(rgb_image, (cx,cy),(int)(radius),(0,0,255),1)
            cv2.circle(black_image, (cx,cy),(int)(radius),(0,0,255),1)
            cv2.circle(black_image, (cx,cy),5,(150,150,255),-1)
            print ("Area: {}, Perimeter: {}".format(area, perimeter))
    
    print ("Total number of contours in frame: {}".format(len(contours)))
    cv2.imshow("RGB Image Contours",rgb_image)
    cv2.imshow("Black Image Contours",black_image)

#A function to get contour centroids
def get_contour_center(contour):
    M = cv2.moments(contour)
    cx=-1
    cy=-1
    if (M['m00']!=0):
        cx= int(M['m10']/M['m00'])
        cy= int(M['m01']/M['m00'])
    return cx, cy


def image_callback(ros_image):
  print ('Got an image')

  #convert ros_image into an opencv-compatible image
  
  global bridge
  try:
    frame = bridge.imgmsg_to_cv2(ros_image, "bgr8")
  except CvBridgeError as e:
      print(e)

  yellowLower =(30, 150, 100)
  yellowUpper = (50, 255, 255)
  binary_image_mask = filter_color(frame, yellowLower, yellowUpper)
  contours = getContours(binary_image_mask)
  draw_ball_contour(binary_image_mask, frame,contours)      

  font = cv2.FONT_HERSHEY_SIMPLEX
  cv2.putText(frame,'Ball tracker Activated with ROS & OpenCV!',(10,350), font, 1,(255,255,255),2,cv2.LINE_AA)
  cv2.imshow("Image window", frame)
  cv2.waitKey(100)
   

def main():
  rospy.init_node('tennis_ball_tracker_sub', anonymous=True)

  image_sub = rospy.Subscriber('tennis_ball_image',Image, image_callback)
  
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  
  cv2.destroyAllWindows()

main()