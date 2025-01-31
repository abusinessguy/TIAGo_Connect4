#!/usr/bin/env python2

import rospy
import cv2
import cv2.aruco as aruco
import tf2_ros as tf2
from tf_conversions import transformations
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import PoseStamped
import numpy as np
import tf2_geometry_msgs
from tf.transformations import quaternion_multiply, quaternion_from_euler, euler_from_quaternion


class ArucoDetector:
    def __init__(self):
        rospy.init_node('aruco_detector')
        self.bridge = CvBridge()
        self.tfBuffer = tf2.Buffer()
        self.listener = tf2.TransformListener(self.tfBuffer)
        self.camera_topic = rospy.get_param("~camera_topic", "/xtion/rgb/image_raw")
        self.camera_info_topic = rospy.get_param("~camera_info_topic", "/xtion/rgb/camera_info")
        self.marker_dict = rospy.get_param("~marker_dict", aruco.DICT_6X6_250)
        self.marker_size = rospy.get_param("~marker_size", 0.0525)
        self.base_frame = rospy.get_param("~base_frame", "base_footprint")
        self.camera_matrix = None
        self.dist_coeffs = None
        self.image_sub = rospy.Subscriber(self.camera_topic, Image, self.image_callback)
        self.camera_info_sub = rospy.Subscriber(self.camera_info_topic, CameraInfo, self.camera_info_callback)
        self.aruco_pick_pub = rospy.Publisher("/aruco_piece/pick", PoseStamped, queue_size=10)
        self.aruco_pick_wpoint_pub = rospy.Publisher("/aruco_piece/pick_wpoint", PoseStamped, queue_size=10)
        self.frame_counter = 0  # Frame counter to track which frame is being processed
        self.process_every_n_frames = 10  # Process every 10th frame

    def camera_info_callback(self, camera_info):
        if self.camera_matrix is None and self.dist_coeffs is None:
            self.camera_matrix = np.array(camera_info.K).reshape(3, 3)
            self.dist_coeffs = np.array(camera_info.D)
            self.camera_info_sub.unregister()

    def image_callback(self, data):
        # Increment frame counter
        self.frame_counter += 1

        # Only process every N-th frame (10th frame in this case)
        if self.frame_counter % self.process_every_n_frames != 0:
            return  # Skip processing for non-10th frames
        
        rospy.sleep(1)
        if self.camera_matrix is None or self.dist_coeffs is None:
            rospy.logwarn("Camera parameters not yet available.")
            return

        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            rospy.logerr("Could not convert from '{}' to 'bgr8'. Error: {}".format(data.encoding, e))
            return

        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.Dictionary_get(self.marker_dict)
        
        # Create and customize the detector parameters
        parameters = aruco.DetectorParameters_create()
        
        # Example of improved parameters
        parameters.adaptiveThreshWinSizeMin = 3
        parameters.adaptiveThreshWinSizeMax = 23
        parameters.adaptiveThreshWinSizeStep = 10
        
        # Detect markers with improved parameters
        corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        if ids is not None:
            rvecs, tvecs = aruco.estimatePoseSingleMarkers(corners, self.marker_size, self.camera_matrix, self.dist_coeffs)
            for i, marker_id in enumerate(ids):
                rospy.loginfo("Processing marker ID: {}".format(marker_id))
                aruco_pose = PoseStamped()
                aruco_pose.pose.position.x = tvecs[i][0][0]
                aruco_pose.pose.position.y = tvecs[i][0][1]
                aruco_pose.pose.position.z = tvecs[i][0][2]
                quaternion = transformations.quaternion_from_euler(rvecs[i][0][0], rvecs[i][0][1], rvecs[i][0][2])
                aruco_pose.pose.orientation.x = quaternion[0]
                aruco_pose.pose.orientation.y = quaternion[1]
                aruco_pose.pose.orientation.z = quaternion[2]
                aruco_pose.pose.orientation.w = quaternion[3]
                aruco_pose.header.frame_id = data.header.frame_id
                aruco_pose.header.stamp = rospy.Time.now()
                
                # Transform pose to base frame
                pose_transformed = self.transform_pose_to_base(aruco_pose)

                if pose_transformed:
                    wpoint = self.apply_transformations(pose_transformed, translation=(0.02, 0.03, 0.13+0.225), rotation_euler=(0, np.pi / 2, 0))
                    self.aruco_pick_wpoint_pub.publish(wpoint)
                    pickPos = self.apply_transformations(pose_transformed, translation=(0.0, 0, -0.04), rotation_euler=(0, np.pi / 2, 0))
                    self.aruco_pick_pub.publish(pickPos)
                    

    def transform_pose_to_base(self, aruco_pose):
        """move_text
        Transforms the detected marker's pose from the camera frame to the base frame.
        :param aruco_pose: PoseStamped in the camera frame.
        :return: Transformed PoseStamped in the base frame.
        """
        try:
            # Wait for the transform to become available
            if self.tfBuffer.can_transform(self.base_frame, aruco_pose.header.frame_id, rospy.Time(0), rospy.Duration(1.0)):
                # Perform the transformation from the camera frame to the base frame
                transform = self.tfBuffer.lookup_transform(self.base_frame, aruco_pose.header.frame_id, rospy.Time(0), rospy.Duration(1.0))
                transformed_pose = tf2_geometry_msgs.do_transform_pose(aruco_pose, transform)
                return transformed_pose
            else:
                rospy.logwarn("Transform from {} to {} not available yet".format(aruco_pose.header.frame_id, self.base_frame))
                return None
        except (tf2.LookupException, tf2.ConnectivityException, tf2.ExtrapolationException) as e:
            rospy.logwarn("Failed to transform pose: {}".format(e))
            return None

    def apply_transformations(self, pose, translation=None, rotation_euler=None):
        """
        Apply translation and rotation to a given PoseStamped object.
        
        :param pose: PoseStamped object to be transformed
        :param translation: Tuple (dx, dy, dz) for translation (optional)
        :param rotation_euler: Tuple (roll, pitch, yaw) for rotation in radians (optional)
        :return: Transformed PoseStamped object
        """

        # Apply translation if provided
        if translation:
            pose.pose.position.x += translation[0]
            pose.pose.position.y += translation[1]
            pose.pose.position.z += translation[2]

        # Apply rotation if provided
        if rotation_euler:
            # Convert euler angles to a quaternion
            rotation_quat = quaternion_from_euler(rotation_euler[0], rotation_euler[1], rotation_euler[2])

            pose.pose.orientation.x = rotation_quat[0]
            pose.pose.orientation.y = rotation_quat[1]
            pose.pose.orientation.z = rotation_quat[2]
            pose.pose.orientation.w = rotation_quat[3]
        
        return pose
    
    def cleanup(self):
        rospy.loginfo("Cleaning up resources.")
        cv2.destroyAllWindows()
        self.image_sub.unregister()
        self.aruco_pick_pub.unregister()


if __name__ == '__main__':
    detector = ArucoDetector()
    rospy.on_shutdown(detector.cleanup)
    rospy.spin()
