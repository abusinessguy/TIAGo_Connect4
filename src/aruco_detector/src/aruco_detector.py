#!/usr/bin/env python

import rospy
import cv2
import cv2.aruco as aruco
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import String
import numpy as np

class ArucoDetector:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/xtion/rgb/image_raw", Image, self.image_callback)
        self.info_pub = rospy.Publisher("/aruco_info", String, queue_size=10)

        # Approximate camera calibration parameters
        self.camera_matrix = np.array([[525.0, 0, 319.5],   # fx, 0, cx
                                       [0, 525.0, 239.5],   # 0, fy, cy
                                       [0, 0, 1]])          # 0, 0, 1

        self.dist_coeffs = np.array([0.1, -0.25, 0, 0, 0])   # [k1, k2, p1, p2, k3]

    def image_callback(self, data):
	    try:
		cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
	    except CvBridgeError as e:
		rospy.logerr("Could not convert from '{}' to 'bgr8'. Error: {}".format(data.encoding, e))
		return

	    # Detect ArUco markers
	    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
	    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
	    parameters = aruco.DetectorParameters_create()

	    corners, ids, rejected = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

	    if ids is not None and len(corners) > 0:
		# Ensure estimatePoseSingleMarkers returns the expected number of values
		estimate_result = aruco.estimatePoseSingleMarkers(corners, 0.05, self.camera_matrix, self.dist_coeffs)

		if len(estimate_result) == 2:
		    rvecs, tvecs = estimate_result

		    for i, marker_id in enumerate(ids):
		        # Draw bounding box around the marker
		        cv2.polylines(cv_image, [corners[i].astype(int)], True, (0, 255, 0), 2)

		        # Draw axis for the marker
		        aruco.drawAxis(cv_image, self.camera_matrix, self.dist_coeffs, rvecs[i], tvecs[i], 0.1)

		        # Log and publish the ID and pose of the marker
		        translation = tvecs[i].flatten()
		        rotation = rvecs[i].flatten()
		        rospy.loginfo("Detected ArUco ID: {} Translation: {} Rotation: {}".format(marker_id[0], translation, rotation))
		        self.info_pub.publish("ID: {} Translation: {} Rotation: {}".format(marker_id[0], translation, rotation))

		        # Optionally display the translation and rotation on the image
		        cv2.putText(cv_image, "ID: {} T: {} R: {}".format(marker_id[0], translation, rotation),
		                    tuple(corners[i][0][0].astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2, cv2.LINE_AA)
		else:
		    rospy.logwarn("estimatePoseSingleMarkers returned an unexpected number of values.")
	    else:
		rospy.loginfo("No ArUco markers detected.")

	    # Display the image with the detected markers and pose
	    cv2.imshow("Image window", cv_image)
	    cv2.waitKey(3)

    def cleanup(self):
        cv2.destroyAllWindows()

if __name__ == '__main__':
    rospy.init_node('aruco_detector', anonymous=True)
    detector = ArucoDetector()
    rospy.on_shutdown(detector.cleanup)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        rospy.loginfo("Shutting down ArUco Detector Node")

