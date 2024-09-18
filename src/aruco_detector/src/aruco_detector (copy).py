#!/usr/bin/env python

import rospy
import cv2
import cv2.aruco as aruco
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import String

class ArucoDetector:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/xtion/rgb/image_raw", Image, self.image_callback)
        self.info_pub = rospy.Publisher("/aruco_info", String, queue_size=10)

    def image_callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            rospy.logerr("Could not convert from '{}' to 'bgr8'. Error: {}".format(data.encoding, e))
            return

        # Detect ArUco markers
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        parameters = aruco.DetectorParameters_create()

        corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        if ids is not None:
            for i, corner in enumerate(corners):
                # Draw bounding box around the marker
                cv2.polylines(cv_image, [corner.astype(int)], True, (0, 255, 0), 2)

                # Get the ID of the marker
                marker_id = ids[i][0]
                rospy.loginfo("Detected ArUco ID: {}".format(marker_id))

                # Publish the detected ArUco ID
                self.info_pub.publish("Detected ArUco ID: {}".format(marker_id))

                # Display the marker ID on the image
                cv2.putText(cv_image, "ID: {}".format(marker_id), tuple(corner[0][0].astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Display the image with the detected markers
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

