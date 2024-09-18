#!/usr/bin/env python

import time
import numpy as np
import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from board_detection.msg import BoardState

# Initialize the CvBridge
bridge = CvBridge()

# Define global variables
last_observed_board_state = None  # Track the last observed board state
last_published_board_state = None #np.zeros((6, 7), dtype=int)  # Initialize as an empty board
stable_state_counter = 0  # Counter to track stable states
debounce_threshold = 5  # Number of consistent reads required before publishing
last_published_board_sum = -1
board_sum = 0

# Load the predefined dictionary for ArUco tags
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters_create()

def image_callback(msg):
    global last_published_board_state, last_observed_board_state, stable_state_counter
    rate = rospy.Rate(2)  # Set the rate to 1 Hz (one check per second)
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
                
                # # Draw the tag ID near the marker
                # tag_id = str(ids[i][0])  # Get the ID for this marker
                # center = tag_centers[i]
                # cv2.putText(cv_image, "ID: {}".format(tag_id), (center[0], center[1] - 10), 
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
                
                # # Optionally, you can also show the tag center coordinates
                # cv2.putText(cv_image, "({},{})".format(center[0], center[1]), 
                #             (center[0], center[1] + 20), 
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
            
            
            # Show the image with the detected markers and their information
            # cv2.imshow("Detected ArUco Tags", cv_image)
            # cv2.waitKey(0)  # Wait indefinitely until a key is pressed

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
            #cv2.waitKey(3)  # Wait indefinitely until a key is pressed


            if warped.size != 0:
                rows, cols = 6, 7
                board_state = np.zeros((rows, cols), dtype=int)

                # # Draw horizontal lines
                # for i in range(1, rows):
                #     y = i * cell_height
                #     cv2.line(warped, (0, y), (width, y), (255, 0, 0), 2)  # Blue horizontal lines

                # # Draw vertical lines
                # for j in range(1, cols):
                #     x = j * cell_width
                #     cv2.line(warped, (x, 0), (x, height), (255, 0, 0), 2)  # Blue vertical lines

                for i in range(rows):
                    for j in range(cols):
                        x = (j) * cell_width
                        y = (i) * cell_height
                        cell = warped[y:y + cell_height, x:x + cell_width]
                        #rospy.loginfo("Cell: {},{}".format(i, j))
                        color = detect_piece_color(cell)
                        board_state[i, j] = color

                rospy.loginfo("Board state:\n{}".format(board_state))
                board_sum = np.sum(board_state)
                rospy.loginfo("Board sum: {}".format(board_sum))

                # Compare the current board state with the last observed state and (last_published_board_sum + 1 == board_sum or last_published_board_sum + 2 == board_sum)
                if last_observed_board_state is None and not np.array_equal(board_state, last_observed_board_state) :
                    stable_state_counter = 1  # Reset the counter if the state is different
                else:
                    stable_state_counter += 1  # Increment the counter if the state is consistent

                # Update the last observed state
                last_observed_board_state = board_state.copy()

                if stable_state_counter >= debounce_threshold and not np.array_equal(board_state, last_published_board_state):
                    # If the stable state counter reaches the threshold
                    board_state_msg = BoardState()
                    board_state_msg.state = board_state.flatten().tolist()
                    board_state_pub.publish(board_state_msg)
                    last_published_board_state = board_state.copy()  # Update the last published state
                    rospy.loginfo("Published stable board state.")
                    stable_state_counter = 0  # Reset the debounce counter after publishing

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




def detect_piece_color(square):
    """Detect the color of a piece in the given square."""
    if square.size == 0:
        return 0
    
    height, width = square.shape[:2]
    center = (width // 2, height // 2)
    radius = int(min(width, height) * 0.4)

    # Create a mask with a filled circle
    mask = np.zeros((height, width), dtype=np.uint8)
    cv2.circle(mask, center, radius, 255, -1)

    # Convert the square to HSV
    hsv = cv2.cvtColor(square, cv2.COLOR_BGR2HSV)

    # Apply the mask to the HSV image
    masked_hsv = cv2.bitwise_and(hsv, hsv, mask=mask)

    lower_red1 = np.array([0, 110, 30])
    upper_red1 = np.array([10, 270, 160])
    lower_red2 = np.array([170, 110, 30])
    upper_red2 = np.array([180, 270, 160])
    lower_blue = np.array([90, 50, 0]) #([95, 60, 0])
    upper_blue = np.array([145, 250, 180]) #([141, 230, 130])



    # Create masks for red using both ranges
    mask_red1 = cv2.inRange(masked_hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(masked_hsv, lower_red2, upper_red2)

    # Combine the two red masks
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)


    mask_blue = cv2.inRange(masked_hsv, lower_blue, upper_blue)

    # Calculate the fraction of the square covered by the colors
    total_masked_pixels = cv2.countNonZero(mask)
    red_fraction = cv2.countNonZero(mask_red) / float(total_masked_pixels)
    blue_fraction = cv2.countNonZero(mask_blue) / float(total_masked_pixels)


    # #Debugging visualization
    # cv2.imshow("Square", square)
    # # cv2.waitKey(1)
    # cv2.imshow("masked_hsv", masked_hsv)
    # cv2.imshow("Red Mask", mask_red)
    # # cv2.waitKey(1)
    # cv2.imshow("Blue Mask", mask_blue)
    # cv2.waitKey(1)
    # # # rospy.loginfo("HSV Mean: {}".format(np.mean(hsv, axis=(0, 1))))
    #rospy.loginfo("Red Fraction: {:.2f}, Blue Fraction: {:.2f}".format(red_fraction, blue_fraction))
    # cv2.waitKey(500)  # Allow a brief pause to view the images

    # Determine the color based on the fraction
    if red_fraction > 0.7:
        return 1  # Red piece
    if blue_fraction > 0.7:
        return 2  # Blue piece
    return 0  # No piece or white


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
    board_state_pub = rospy.Publisher('/board_state', BoardState, queue_size=10)
    rospy.Subscriber('/xtion/rgb/image_raw', Image, image_callback)
    rospy.loginfo("Subscribed to /xtion/rgb/image_raw topic")
    rospy.spin()

if __name__ == "__main__":
    main()

