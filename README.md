# BallTrackerROS
BallTrackerROS is a Python-based project that utilizes the Robot Operating System (ROS) framework along with OpenCV for tracking a yellow ball in a video stream. The project captures video frames from a ROS topic, applies computer vision techniques to detect the yellow ball, and overlays a contour around the detected ball in real-time.

## Features:
- Ball tracking in video streams using ROS and OpenCV.
- Detection and tracking of a yellow ball using color-based image processing.
- Visualization of the tracked ball with a contour overlaid on the video frames

## Installation:
1. Clone the repository
2. Install necessary libraries and dependcies (ROS, OpenCV, OpenCV Bridge)

## Launching:
1. Launch roscore
2. Run the publisher script for publishing the video frames (The video is also provided)
3. Then run the subscriber node
4. This subscriber node will receive the video frames from the publisher and use OpenCV to draw a contour over the tennis ball in the video published and displays it.

Note: Make sure the location of video file in the publisher script is correct.
