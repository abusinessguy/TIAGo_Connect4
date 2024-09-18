#!/usr/bin/env python

import time
import numpy as np
from scipy.stats import circmean
import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from board_detection.msg import BoardState

# MAKE A CHECKERBOARD PATTERN
# Start with red in the bottom left corner.


# Initialize the CvBridge
bridge = CvBridge()

# Define global variables
# last_observed_board_state = None  # Track the last observed board state
# last_published_board_state = None #np.zeros((6, 7), dtype=int)  # Initialize as an empty board
# stable_state_counter = 0  # Counter to track stable states
# debounce_threshold = 5  # Number of consistent reads required before publishing

# Load the predefined dictionary for ArUco tags
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters_create()



def image_callback(msg):
    global last_published_board_state, last_observed_board_state, stable_state_counter
    rate = rospy.Rate(5)  # Set the rate to 1 Hz (one check per second)
    blue_hues =[]
    blue_sats =[]
    blue_vals =[]
    red_hues =[]
    red_sats =[]
    red_vals =[]
    try:
        #rospy.loginfo("Received image")
        cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        gray_frame = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        tag_centers, corners, ids = detect_aruco_tags(gray_frame)

        if corners is not None:
            for corner in corners:
                cv2.polylines(cv_image, [corner.astype(int)], True, (0, 255, 0), 2)
            
            # Display the image with detected tags
            #cv2.imshow("Detected ArUco Tags", cv_image)
            #cv2.waitKey(3)
        else:
            # rospy.loginfo("No ArUco tags detected.")
            return

        if tag_centers and ids is not None and len(tag_centers) == 4:
            # Draw the marker borders and IDs
            for i, corner in enumerate(corners):
                # Draw the marker borders
                cv2.polylines(cv_image, [corner.astype(int)], True, (0, 255, 0), 2)
                
            # Define marker ID to corner position mapping
            marker_id_to_position = {
                0: "top_left",
                1: "top_right",
                3: "bottom_right",
                2: "bottom_left"
            }
            # Create a mapping from detected IDs to corners
            id_to_corners = {ids[i][0]: corners[i][0] for i in range(len(ids))}

            # Determine positions based on IDs
            positions = {v: id_to_corners[k] for k, v in marker_id_to_position.items() if k in id_to_corners}

            if len(positions) < 4:
                rospy.loginfo("Not all expected markers detected.")
                return

            # Extract positions and ensure they are tuples of coordinates
            top_left = tuple(map(int, positions["top_left"].mean(axis=0)))
            top_right = tuple(map(int, positions["top_right"].mean(axis=0)))
            bottom_left = tuple(map(int, positions["bottom_left"].mean(axis=0)))
            bottom_right = tuple(map(int, positions["bottom_right"].mean(axis=0)))


            cell_width = int((top_right[0] - top_left[0]) / 8)
            cell_height = int((bottom_left[1] - top_left[1]) / 5)

            matrix, width, height = calculate_perspective_transform(
                top_left, top_right, bottom_left, bottom_right, cell_width, cell_height
            )
            frame = preprocess_image(cv_image, 1)
            if frame is None or frame.size == 0:
                rospy.logerr("Invalid frame to warp.")
                return
	    #cv2.imshow("Frame", cv_image)
            warped = cv2.warpPerspective(frame, matrix, (width, height))
            if warped is None or warped.size == 0:
                rospy.logerr("Warping failed, invalid warped image.")
                return
	    # Display the warped board before piece detection
            # cv2.imshow("Warped Board", warped)
            # cv2.waitKey(3)  # Wait indefinitely until a key is pressed


            if warped.size != 0:
                rows, cols = 6, 7
                board_state_hue = np.zeros((rows, cols), dtype=int)
                board_state_sat = np.zeros((rows, cols), dtype=int)
                board_state_value = np.zeros((rows, cols), dtype=int)
                

                for i in range(rows):
                    for j in range(cols):
                        x = (j) * cell_width
                        y = (i) * cell_height
                        cell = warped[y:y + cell_height, x:x + cell_width]
                        # rospy.loginfo("Cell: {},{}".format(i, j))
                        hsv_values = detect_hsv_values(cell)
                        
                        board_state_hue[i, j] = hsv_values[0]
                        board_state_sat[i, j] = hsv_values[1]
                        board_state_value[i, j] = hsv_values[2]
                        if (i + j)%2 ==0:
                            blue_hues.append(hsv_values[0])
                            blue_sats.append(hsv_values[1])
                            blue_vals.append(hsv_values[2])
                        else:
                            red_hues.append(hsv_values[0])
                            red_sats.append(hsv_values[1])
                            red_vals.append(hsv_values[2])

                rospy.loginfo("blue_hues:{}".format(blue_hues))
                rospy.loginfo("red_hues:{}".format(red_hues))
                mean_blue_hue = circular_mean(blue_hues)
                std_dev_blue_hue = circular_std(blue_hues, mean_blue_hue)
                rospy.loginfo("mean blue_hues:{:.1f}".format(mean_blue_hue))
                rospy.loginfo("stdev blue_hues:{:1f}".format(std_dev_blue_hue))
                mean_red_hue = circular_mean(red_hues)
                std_dev_red_hue = circular_std(red_hues, mean_red_hue)
                rospy.loginfo("mean red_hues:{:.1f}".format(mean_red_hue))
                rospy.loginfo("stdev red_hues:{:1f}".format(std_dev_red_hue))


                # rospy.loginfo("Hues:\n{}".format(board_state_hue))
                # rospy.loginfo("Saturation:\n{}".format(board_state_sat))
                # rospy.loginfo("Values:\n{}".format(board_state_value))
                # # Find the highest and lowest hues and values from the top and bottom
                # blue_hue = board_state_hue[0:2, :]
                # red_hue = board_state_hue[3:5, :]

                blue_highest_hue = mean_blue_hue + 3*std_dev_blue_hue
                blue_lowest_hue = mean_blue_hue - 3*std_dev_blue_hue

                red_highest_hue = (mean_red_hue + 3*std_dev_red_hue)%179
                red_lowest_hue = (mean_red_hue - 3*std_dev_red_hue)%179

                # blue_sat = board_state_sat[0:2, :]
                # red_sat = board_state_sat[3:5, :]

                # blue_highest_sat = np.max(blue_sat)
                # blue_lowest_sat = np.min(blue_sat)

                # red_highest_sat = np.max(red_sat)
                # red_lowest_sat = np.min(red_sat)

                # blue_value = board_state_value[0:2, :]
                # red_value = board_state_value[3:5, :]

                # blue_highest_value = np.max(blue_value)
                # blue_lowest_value = np.min(blue_value)

                # red_highest_value = np.max(red_value)
                # red_lowest_value = np.min(red_value)

                # Print the results
                rospy.loginfo("Blue hue range: {} - {}".format(blue_lowest_hue, blue_highest_hue))
                rospy.loginfo("Red hue range: {} - {}".format(red_lowest_hue, red_highest_hue))
                # rospy.loginfo("Blue sat range: {} - {}".format(blue_lowest_sat, blue_highest_sat))
                # rospy.loginfo("Red sat range: {} - {}".format(red_lowest_sat, red_highest_sat))
                # rospy.loginfo("Blue value range: {} - {}".format(blue_lowest_value, blue_highest_value))
                # rospy.loginfo("Red value range: {} - {}".format(red_lowest_value, red_highest_value))

                rospy.loginfo("\nlower_red1 = np.array([0, {}, {}])\n \
                              upper_red1 = np.array([{}, {}, {}])\n \
                              lower_red2 = np.array([{}, {}, {}])\n \
                              upper_red2 = np.array([179, {}, {}])\n \
                              lower_blue = np.array([{}, {}, {}])\n \
                              upper_blue = np.array([{}, {}, {}])" \
                              .format(1, 1,\
                                      1 , 1, 1,\
                                      1, 1, 1,\
                                      1, 1,\
                                      blue_lowest_hue, 1, 1,\
                                      blue_highest_hue, 1, ))
                

                rate.sleep()
            
    except CvBridgeError as e:
        rospy.logerr("Error converting ROS Image to OpenCV: {}".format(e))


def circular_mean(values, max_value=179):
    """Calculate the circular mean of a list of values."""
    values = np.array(values, dtype=np.float32)
    angles = (values / max_value) * 2 * np.pi
    mean_angle = np.arctan2(np.mean(np.sin(angles)), np.mean(np.cos(angles)))
    mean_hue = (mean_angle / (2 * np.pi)) * max_value
    if mean_hue < 0:
        mean_hue += max_value
    return mean_hue

# def circular_mean(values, max_value=179):
#     """Calculate the circular mean of a list of values."""
#     values = np.array(values, dtype=np.float32)
#     print("Input values: {}".format(values))
    
#     # Convert values to angles in radians
#     angles = (values / max_value) * 2 * np.pi
#     print("Angles (radians): {}".format(angles))
    
#     # Compute mean angle
#     mean_sin = np.mean(np.sin(angles))
#     mean_cos = np.mean(np.cos(angles))
#     print("Mean Sin: {}, Mean Cos: {}".format(mean_sin, mean_cos))
    
#     mean_angle = np.arctan2(mean_sin, mean_cos)
#     print("Mean Angle (radians): {}".format(mean_angle))
    
#     # Convert mean angle back to the original scale
#     mean_hue = (mean_angle / (2 * np.pi)) * max_value
#     print("Mean Hue before correction: {}".format(mean_hue))
    
#     # Ensure mean_hue is within [0, max_value]
#     mean_hue = mean_hue % max_value
#     print("Final Mean Hue: {}".format(mean_hue))
    
#     return mean_hue




def circular_std(values, mean_hue, max_value=179):
    """Calculate the circular standard deviation of a list of values."""
    values = np.array(values, dtype=np.float32)
    angles = (values / max_value) * 2 * np.pi
    mean_angle = (mean_hue / max_value) * 2 * np.pi
    std_dev = np.sqrt(np.mean(np.square(np.arctan2(np.sin(angles - mean_angle), np.cos(angles - mean_angle)))))
    return (std_dev / (2 * np.pi)) * max_value

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
        # rospy.loginfo("No ArUco tags detected")
        return None, None, None

    # Log the IDs of the detected markers
    # rospy.loginfo("Detected {} ArUco tags with IDs: {}".format(len(ids), ids.flatten().tolist()))

    # Calculate the center of each detected marker
    tag_centers = []
    for corner in corners:
        center = corner[0].mean(axis=0).astype(int)
        tag_centers.append(tuple(center))

    return tag_centers, corners, ids


def detect_hsv_values(square):
    """Calculate and return the mean HSV values of the given square."""
    if square.size == 0:
        return (0, 0, 0)
    
    height, width = square.shape[:2]
    center = (width // 2, height // 2)
    radius = int(min(width, height) * 0.4)

    # Create a mask with a filled circle
    mask = np.zeros((height, width), dtype=np.uint8)
    cv2.circle(mask, center, radius, 255, -1)

    # Convert the square to HSV
    hsv = cv2.cvtColor(square, cv2.COLOR_BGR2HSV)



    # Extract the hue channel (H channel is the first channel in the HSV image)
    hue_channel = hsv[:, :, 0]

    # Apply the mask to the hue channel
    masked_hue = cv2.bitwise_and(hue_channel, hue_channel, mask=mask)
    # Extract the hue values within the circular region
    hue_values = masked_hue[mask > 0]
    rospy.loginfo("cell_hues:{}".format(hue_values))

    mean_hue1 = circmean(hue_values, high=179, low=0)
    mean_hue = circular_mean(hue_values)
    std_dev_hue = circular_std(hue_values, mean_hue)
    rospy.loginfo("cell std_dev_hue: {}   cell mean_hue: {} cell circmean_hue: {}".format(std_dev_hue, mean_hue, mean_hue1))
    
    # # Visualize the masked hue channel
    # cv2.imshow("Masked Hue Channel", masked_hue)
    # cv2.waitKey(500)  # Allow a brief pause to view the image




    # Apply the mask to the HSV image
    masked_hsv = cv2.bitwise_and(hsv, hsv, mask=mask)
    cv2.imshow("masked_hsv", masked_hsv)

    # Calculate the mean HSV values within the circular region
    mean_hsv = cv2.mean(hsv, mask=mask)[:3]
    mean_hsv = (mean_hue, mean_hsv[1], mean_hsv[2])
    
    return tuple(map(int, mean_hsv))

def calculate_perspective_transform(top_left, top_right, bottom_left, bottom_right, cell_width, cell_height):
    """Calculate the perspective transform matrix."""
    pts1 = np.float32([top_left, top_right, bottom_right, bottom_left])
    width = cell_width * 7
    height = cell_height * 6
    pts2 = np.float32([
        [-cell_width / 2, +cell_height/2],
        [width + cell_width / 2, +cell_height/2],
        [width + cell_width / 2, height - cell_height/2],
        [-cell_width / 2, height - cell_height/2]
    ])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    return matrix, width, height

def main():
    global board_state_pub  # Ensure this variable is available globally
    rospy.loginfo("Starting image listener node")
    rospy.init_node('image_listener')
    #board_state_pub = rospy.Publisher('/board_state', BoardState, queue_size=10)
    rospy.Subscriber('/xtion/rgb/image_raw', Image, image_callback)
    rospy.loginfo("Subscribed to /xtion/rgb/image_raw topic")
    rospy.spin()

if __name__ == "__main__":
    main()

