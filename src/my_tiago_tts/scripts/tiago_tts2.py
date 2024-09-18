#!/usr/bin/env python

import time
import numpy as np
import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

# Initialize the CvBridge
bridge = CvBridge()

# Load the predefined dictionary for ArUco tags
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters_create()

def image_callback(msg):
    rate = rospy.Rate(.2)  # Set the rate to 1 Hz (one check per second)
    try:
        #rospy.loginfo("Received image")
        cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        gray_frame = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        tag_centers, corners = detect_aruco_tags(gray_frame)

        if corners is not None:
            for corner in corners:
                cv2.polylines(cv_image, [corner.astype(int)], True, (0, 255, 0), 2)
            
            # Display the image with detected tags
            cv2.imshow("Detected ArUco Tags", cv_image)
            cv2.waitKey(3)
        else:
            rospy.loginfo("No ArUco tags detected.")
        if tag_centers and len(tag_centers) == 4:
            rospy.loginfo("Detected 4 AprilTags")

            for i, corner in enumerate(corners):
                # Draw the marker borders
                cv2.polylines(cv_image, [corner.astype(int)], True, (0, 255, 0), 2)
                
                # Draw the tag ID near the marker
                tag_id = str(i)
                center = tag_centers[i]
                cv2.putText(cv_image, "ID: {}".format(tag_id), (center[0], center[1] - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
                
                # Optionally, you can also show the tag center coordinates
                cv2.putText(cv_image, "({},{})".format(center[0], center[1]), 
                            (center[0], center[1] + 20), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
            
            # Show the image with the detected markers and their information
            cv2.imshow("Detected ArUco Tags", cv_image)
            cv2.waitKey(0)  # Wait indefinitely until a key is pressed

            top_left = tag_centers[2]
            top_right = tag_centers[3]
            bottom_left = tag_centers[1]
            bottom_right = tag_centers[0]

            cell_width = int((top_right[0] - top_left[0]) / 8)
            cell_height = int((bottom_left[1] - top_left[1]) / 7)

            matrix, width, height = calculate_perspective_transform(
                top_left, top_right, bottom_left, bottom_right, cell_width, cell_height
            )
            frame = preprocess_image(cv_image, 1)
	    cv2.imshow("Frame", cv_image)
            warped = cv2.warpPerspective(frame, matrix, (width, height))

	    # Display the warped board before piece detection
            cv2.imshow("Warped Board", warped)
            cv2.waitKey(0)  # Wait indefinitely until a key is pressed


            if warped.size != 0:
                rows, cols = 6, 7
                board_state = np.zeros((rows, cols), dtype=int)

                for i in range(rows):
                    for j in range(cols):
                        x = (1 + j) * cell_width
                        y = (1 + i) * cell_height
                        cell = warped[y:y + cell_height, x:x + cell_width]
                        color = detect_piece_color(cell)
                        board_state[i, j] = color

                rospy.loginfo("Board state:")
                rospy.loginfo(board_state)
	rate.sleep()
            
    except CvBridgeError as e:
        rospy.logerr("Error converting ROS Image to OpenCV: {}".format(e))

def preprocess_image(image, reduction):
    """Reduce image resolution to reduce complexity."""
    width = int(image.shape[1] * reduction)
    height = int(image.shape[0] * reduction)
    dim = (width, height)
    resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized_image

def detect_aruco_tags(image):
    # Detect markers in the image using the specified ArUco dictionary and parameters
    corners, ids, rejected = cv2.aruco.detectMarkers(image, aruco_dict, parameters=parameters)

    # Check if any markers were detected
    if ids is None or len(ids) == 0:
        rospy.loginfo("No ArUco tags detected")
        return None, None

    # Log the IDs of the detected markers
    rospy.loginfo("Detected {} ArUco tags with IDs: {}".format(len(ids), ids.flatten().tolist()))

    # Calculate the center of each detected marker
    tag_centers = []
    for corner in corners:
        center = corner[0].mean(axis=0).astype(int)
        tag_centers.append(tuple(center))

    return tag_centers, corners



def detect_piece_color(square):
    """Detect the color of a piece in the given square."""
    if square.size == 0:
        return 0

    hsv = cv2.cvtColor(square, cv2.COLOR_BGR2HSV)
    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 70, 50])
    upper_red2 = np.array([180, 255, 255])
    lower_blue = np.array([90, 50, 0])
    upper_blue = np.array([140, 255, 255])

    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    # Calculate the fraction of the square covered by the colors
    red_fraction = cv2.countNonZero(mask_red) / float(square.size / 3)
    blue_fraction = cv2.countNonZero(mask_blue) / float(square.size / 3)

    # Debugging visualization
    cv2.imshow("Square", square)
    cv2.imshow("Red Mask", mask_red)
    cv2.imshow("Blue Mask", mask_blue)
    rospy.loginfo("HSV Mean: {}".format(np.mean(hsv, axis=(0, 1))))
    rospy.loginfo("Red Fraction: {:.2f}, Blue Fraction: {:.2f}".format(red_fraction, blue_fraction))
    cv2.waitKey(1)  # Allow a brief pause to view the images

    # Determine the color based on the fraction
    if red_fraction > 0.4:
        return 1  # Red piece
    if blue_fraction > 0.4:
        return 2  # Blue piece
    return 0  # No piece or white

def calculate_perspective_transform(top_left, top_right, bottom_left, bottom_right, cell_width, cell_height):
    """Calculate the perspective transform matrix."""
    pts1 = np.float32([top_left, top_right, bottom_right, bottom_left])
    width = cell_width * 9
    height = cell_height * 8
    pts2 = np.float32([
        [cell_width / 2, cell_height / 2],
        [width - cell_width / 2, cell_height / 2],
        [width - cell_width / 2, height - cell_height / 2],
        [cell_width / 2, height - cell_height / 2]
    ])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    return matrix, width, height

def main():
    rospy.loginfo("Starting image listener node")
    rospy.init_node('image_listener')
    rospy.loginfo("ROS node initialized")
    rospy.Subscriber('/xtion/rgb/image_raw', Image, image_callback)
    rospy.loginfo("Subscribed to /xtion/rgb/image_raw topic")
    rospy.spin()

if __name__ == "__main__":
    main()

