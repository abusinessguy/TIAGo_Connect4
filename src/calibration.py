#!/usr/bin/env python

import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image, CameraInfo
import numpy as np

class CameraCalibrator:
    def __init__(self):
        rospy.init_node('camera_calibrator')

        # Parameters
        self.chessboard_size = (7, 7)  # 7x7 internal corners for an 8x8 square grid
        self.square_size = 0.02174  # Size of a square in your defined units (meters in this case)
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        self.bridge = CvBridge()

        # Object points
        self.objp = np.zeros((self.chessboard_size[0] * self.chessboard_size[1], 3), np.float32)
        self.objp[:, :2] = np.mgrid[0:self.chessboard_size[0], 0:self.chessboard_size[1]].T.reshape(-1, 2)
        self.objp *= self.square_size

        # Storage for points
        self.objpoints = []
        self.imgpoints = []

        # Image subscriber
        self.image_sub = rospy.Subscriber("/xtion/rgb/image_raw", Image, self.image_callback)

    def image_callback(self, msg):
        rospy.loginfo("Image received.")
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            rospy.loginfo("Image converted to OpenCV format.")
        except CvBridgeError as e:
            rospy.logerr("Could not convert from '{}' to 'bgr8'. Error: {}".format(msg.encoding, e))
            return

        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        rospy.loginfo("Image converted to grayscale.")

        # Find the chessboard corners with the adjusted size
        ret, corners = cv2.findChessboardCorners(gray, self.chessboard_size, None)
        rospy.loginfo("Chessboard detection status: {}".format(ret))

        if ret:
            rospy.loginfo("Chessboard corners detected.")
            # If found, add object points, image points
            self.objpoints.append(self.objp)

            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), self.criteria)
            self.imgpoints.append(corners2)

            # Draw and display the corners
            cv_image = cv2.drawChessboardCorners(cv_image, self.chessboard_size, corners2, ret)
            cv2.imshow('Calibration Image', cv_image)
            cv2.waitKey(1)
        else:
            rospy.logwarn("Chessboard not detected in this frame.")

        if len(self.imgpoints) >= 20:  # Tune this to your needs
            self.calibrate_camera(gray.shape[::-1])
            rospy.signal_shutdown("Calibration complete")

    def calibrate_camera(self, image_size):
        # Perform camera calibration
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints, image_size, None, None)

        if ret:
            rospy.loginfo("Calibration successful")
            rospy.loginfo("Camera matrix:\n{}".format(mtx))
            rospy.loginfo("Distortion coefficients:\n{}".format(dist))
            rospy.loginfo("Rotation vectors:\n{}".format(rvecs))
            rospy.loginfo("Translation vectors:\n{}".format(tvecs))
        else:
            rospy.logwarn("Calibration failed")

if __name__ == '__main__':
    try:
        calibrator = CameraCalibrator()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    cv2.destroyAllWindows()
