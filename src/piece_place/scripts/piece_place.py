#!/usr/bin/env python

import rospy
import numpy as np
import cv2
import cv2.aruco as aruco
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import PoseStamped, Quaternion
from cv_bridge import CvBridge, CvBridgeError
import tf2_ros
import tf2_geometry_msgs.tf2_geometry_msgs as tf2_geometry_msgs
from tf.transformations import quaternion_multiply, quaternion_from_euler, euler_from_quaternion

class PiecePlace:
    def __init__(self):
        rospy.init_node('piece_place')
        
        self.bridge = CvBridge()
        self.tfBuffer = tf2_ros.Buffer()
        self.listener = tf2_ros.TransformListener(self.tfBuffer)

        self.marker_dict = aruco.DICT_4X4_50  # Change to your specific dictionary type
        self.marker_size = rospy.get_param("~marker_size", 0.03)  # Set your marker size to 1 inch (0.0254 meters)

        self.frame_counter = 0  # Frame counter to track which frame is being processed
        self.process_every_n_frames = 5  # Process every 5th frame

        self.camera_topic = rospy.get_param("~camera_topic", "/xtion/rgb/image_raw")
        self.camera_info_topic = rospy.get_param("~camera_info_topic", "/xtion/rgb/camera_info")
        
        self.camera_matrix = None
        self.dist_coeffs = None

        self.image_sub = rospy.Subscriber(self.camera_topic, Image, self.image_callback)
        self.camera_info_sub = rospy.Subscriber(self.camera_info_topic, CameraInfo, self.camera_info_callback)
        self.pose_pub = rospy.Publisher("/aruco_plane/pose", PoseStamped, queue_size=10)
        self.poses_pub = [rospy.Publisher("/aruco_plane/pose_{}".format(i), PoseStamped, queue_size=10) for i in range(7)]
        self.hover_right_pub = rospy.Publisher("/hover_right_position", PoseStamped, queue_size=10)
        self.hover_left_pub = rospy.Publisher("/hover_left_position", PoseStamped, queue_size=10)
        self.marker_poses_pub = {
            0: rospy.Publisher("/aruco_marker_0/pose", PoseStamped, queue_size=10),
            1: rospy.Publisher("/aruco_marker_1/pose", PoseStamped, queue_size=10),
            2: rospy.Publisher("/aruco_marker_2/pose", PoseStamped, queue_size=10),
            3: rospy.Publisher("/aruco_marker_3/pose", PoseStamped, queue_size=10)
        }

        # The base frame you want to align orientations with
        self.base_footprint = rospy.get_param("~base_footprint", "base_footprint")

    def camera_info_callback(self, camera_info):
        self.camera_matrix = np.array(camera_info.K).reshape((3, 3))
        self.dist_coeffs = np.array(camera_info.D)

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
            #pose.pose.orientation = tf::createQuaternionMsgFromRollPitchYaw(-M_PI/2, 0.001, M_PI/2);  // Adjust RPY values as needed M_PI/2
            
            # Get current orientation as a quaternion
            # current_orientation = [
            #     pose.pose.orientation.x,
            #     pose.pose.orientation.y,
            #     pose.pose.orientation.z,
            #     pose.pose.orientation.w
            # ]
            
            # Multiply the current orientation with the new rotation quaternion
            #new_orientation = quaternion_multiply(rotation_quat, current_orientation)
            new_orientation = rotation_quat
            # Update the pose's orientation
            pose.pose.orientation.x = new_orientation[0]
            pose.pose.orientation.y = new_orientation[1]
            pose.pose.orientation.z = new_orientation[2]
            pose.pose.orientation.w = new_orientation[3]
        
        return pose
    
    def image_callback(self, data):
        # Increment frame counter
        self.frame_counter += 1

        # Only process every N-th frame (10th frame in this case)
        if self.frame_counter % self.process_every_n_frames != 0:
            return  # Skip processing for non-10th frames
        

        rate = rospy.Rate(0.5)
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
        
        parameters = aruco.DetectorParameters_create()
        corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        if ids is not None:
            aruco.drawDetectedMarkers(cv_image, corners, ids)
        else:
            rospy.logwarn("No markers detected.")
            return
        
        required_markers = {0, 1, 2, 3}
        detected_markers = set(ids.flatten()) if ids is not None else set()
        
        if required_markers.issubset(detected_markers):
            index0 = np.where(ids == 0)[0][0]
            index1 = np.where(ids == 1)[0][0]
            index2 = np.where(ids == 2)[0][0]
            index3 = np.where(ids == 3)[0][0]
            
            rvecs, tvecs = aruco.estimatePoseSingleMarkers(corners, self.marker_size, self.camera_matrix, self.dist_coeffs)
            
            positions = [tvecs[index0][0], tvecs[index1][0], tvecs[index2][0], tvecs[index3][0]]

            # Loop through each marker and transform their poses from camera frame to base frame
            for marker_id, pos in enumerate(positions):
                pose_marker = PoseStamped()
                pose_marker.header.frame_id = data.header.frame_id
                pose_marker.header.stamp = rospy.Time.now()
                pose_marker.pose.position.x = pos[0]
                pose_marker.pose.position.y = pos[1]
                pose_marker.pose.position.z = pos[2]

                try:
                    # Get the transform from the camera frame to the base frame
                    transform = self.tfBuffer.lookup_transform(self.base_footprint, data.header.frame_id, rospy.Time(0))

                    # Transform the pose to the base frame
                    pose_marker_transformed = tf2_geometry_msgs.do_transform_pose(pose_marker, transform)

                    # Publish marker pose after transformation
                    self.marker_poses_pub[marker_id].publish(pose_marker_transformed)
                except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
                    rospy.logwarn("Could not get transform from {} to {}: {}".format(self.base_footprint, data.header.frame_id, e))
                    return

            # Calculate and publish intermediate poses between marker 0 and marker 1
            pos0 = positions[0]
            pos1 = positions[1]
            line_vector = pos1 - pos0

            for i in range(7):
                fraction = (i + 1) / 8.0
                position = pos0 + fraction * line_vector

                pose = PoseStamped()
                pose.header.frame_id = data.header.frame_id
                pose.header.stamp = rospy.Time.now()
                pose.pose.position.x = position[0]
                pose.pose.position.y = position[1]
                pose.pose.position.z = position[2]

                try:
                    if i < 4:
                        # Transform the intermediate pose to the base frame
                        pose_transformed = tf2_geometry_msgs.do_transform_pose(pose, transform)
                        pose_transformed = self.apply_transformations(pose_transformed, translation=(-.015, -0.221, 0.17), rotation_euler=(-np.pi / 2, .17, np.pi/2)) #(-M_PI/2, 0.001, M_PI/2) 23 deg to rad = 0.4
                        self.poses_pub[i].publish(pose_transformed)

                    # Handle the hover pose at position 3
                    if i == 3:
                        hover_pose_rightside = PoseStamped()
                        hover_pose_rightside.header = pose_transformed.header
                        hover_pose_rightside.pose.position.x = pose_transformed.pose.position.x
                        hover_pose_rightside.pose.position.y = pose_transformed.pose.position.y
                        hover_pose_rightside.pose.position.z = pose_transformed.pose.position.z
                        hover_pose_rightside.pose.orientation = pose_transformed.pose.orientation

                        hover_pose_leftside = PoseStamped()
                        hover_pose_leftside.header = pose_transformed.header
                        hover_pose_leftside.pose.position.x = pose_transformed.pose.position.x
                        hover_pose_leftside.pose.position.y = pose_transformed.pose.position.y
                        hover_pose_leftside.pose.position.z = pose_transformed.pose.position.z
                        hover_pose_leftside.pose.orientation = pose_transformed.pose.orientation

                        # Transform hover pose to the base frame and publish it
                        hover_pose_rightside_transformed = self.apply_transformations(hover_pose_rightside, translation=(0, -0.019, 0), rotation_euler=(-np.pi / 2, 0.001, np.pi/2))
                        self.hover_right_pub.publish(hover_pose_rightside_transformed)
                        #hover_pose_transformed = tf2_geometry_msgs.do_transform_pose(hover_pose_transformed, transform)
                        hover_pose_leftside_transformed = self.apply_transformations(hover_pose_leftside, translation=(0, 0.221+0.221+.019, 0), rotation_euler=(-np.pi / 2, 0.001, -np.pi/2))
                        self.hover_left_pub.publish(hover_pose_leftside_transformed)

                    if i > 3:
                        # Transform the intermediate pose to the base frame
                        pose_transformed = tf2_geometry_msgs.do_transform_pose(pose, transform)
                        pose_transformed = self.apply_transformations(pose_transformed, translation=(-.015, 0.221+.053, 0.17), rotation_euler=(-np.pi / 2, .17, -np.pi/2)) #(-M_PI/2, 0.001, M_PI/2) 23 deg to rad = 0.4
                        self.poses_pub[i].publish(pose_transformed)
                        rospy.loginfo("Poses published")



                        # rospy.loginfo("Hover position: x={}, y={}, z={}, orientation={}".format(
                        #     hover_pose_rightside_transformed.pose.position.x,
                        #     hover_pose_rightside_transformed.pose.position.y,
                        #     hover_pose_rightside_transformed.pose.position.z,
                        #     hover_pose_rightside_transformed.pose.orientation
                        # ))
                        # q = hover_pose_rightside_transformed.pose.orientation
                        # quaternion = [q.x, q.y, q.z, q.w]

                        # # Convert quaternion to Euler angles
                        # roll, pitch, yaw = euler_from_quaternion(quaternion)

                        # rospy.loginfo("Hover orientation in Euler angles: roll={}, pitch={}, yaw={}".format(roll, pitch, yaw))

                except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
                    rospy.logwarn("Could not get transform for pose {} to base frame: {}".format(i, e))
                    return

        else:
            rospy.logwarn("Not all required markers (0, 1, 2, 3) are detected.")

        cv2.imshow("Aruco Markers", cv_image)
        cv2.waitKey(1)
        rate.sleep()



    def publish_marker_pose(self, data, tvec, marker_id):
        pose = PoseStamped()
        pose.header.frame_id = data.header.frame_id
        pose.header.stamp = rospy.Time.now()
        pose.pose.position.x = tvec[0]
        pose.pose.position.y = tvec[1]
        pose.pose.position.z = tvec[2]

        # Transform the position to the base_footprint frame
        try:
            # Get the transform from the camera frame to the base_footprint frame
            #transform = self.tfBuffer.lookup_transform(self.base_footprint, data.header.frame_id, rospy.Time(0))

            # Transform the position to the base_footprint frame
            #pose_transformed = tf2_geometry_msgs.do_transform_pose(pose, transform)

            # Set the orientation to match the base frame's orientation
            #pose_transformed.pose.orientation = transform.transform.rotation

            # Publish the transformed pose with the base frame's orientation
            #self.marker_poses_pub[marker_id].publish(pose_transformed)
            self.marker_poses_pub[marker_id].publish(pose)
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            rospy.logwarn("Could not get transform from {} to {}: {}".format(self.base_footprint, data.header.frame_id, e))
            return


if __name__ == '__main__':
    try:
        node = PiecePlace()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
