#!/usr/bin/env python

import rospy
from moveit_msgs.msg import CollisionObject
from shape_msgs.msg import SolidPrimitive
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Header
import copy  # For deep copying the pose, otherwise it will repeatedly apply offsets

class CollisionObjectPublisher:
    def __init__(self):
        rospy.init_node('collision_object_publisher')

        # Publisher for collision objects
        self.pub = rospy.Publisher('/collision_objects', CollisionObject, queue_size=10)

        # Subscriber for ArUco marker poses
        rospy.Subscriber('/aruco_piece/pick', PoseStamped, self.aruco_piece_pose_callback)
        rospy.Subscriber('/aruco_marker_0/pose', PoseStamped, self.aruco_marker_0_pose_callback)

        self.aruco_piece_pose = None  # To store the latest ArUco piece pose
        self.aruco_marker_0_pose = None  # To store the latest ArUco marker 0 pose

        # Start publishing collision objects
        self.publish_collision_object()

    def aruco_piece_pose_callback(self, msg):
        """ Callback function to receive ArUco piece pose """
        rospy.loginfo("Received ArUco piece position")
        self.aruco_piece_pose = msg.pose  # Store the received pose

    def aruco_marker_0_pose_callback(self, msg):
        """ Callback function to receive ArUco marker 0 pose """
        rospy.loginfo("Received ArUco marker 0 position")
        self.aruco_marker_0_pose = msg.pose  # Store the received pose

    def publish_collision_object(self):
        """ Publishes collision objects at the ArUco marker positions """
        rate = rospy.Rate(0.1)  # 0.1 Hz
        while not rospy.is_shutdown():
            if self.aruco_piece_pose is not None:
                # Create a deep copy of the received ArUco piece pose
                piece_box_pose = copy.deepcopy(self.aruco_piece_pose)

                # Apply an offset to the ArUco piece marker's position
                piece_box_pose.position.x += 0.5  # Shift x by 0.5 meters
                piece_box_pose.position.y += 0.0  # Shift y by 0.0 meters
                piece_box_pose.position.z += -0.395  # Shift z by -0.37 meters (lower the box)

                # Create a CollisionObject message for the ArUco piece
                collision_object_piece = CollisionObject()
                collision_object_piece.header = Header()
                collision_object_piece.header.frame_id = "base_link"
                collision_object_piece.id = "aruco_piece_collision_box"

                # Define the box's shape and dimensions
                primitive_piece = SolidPrimitive()
                primitive_piece.type = SolidPrimitive.BOX
                primitive_piece.dimensions = [0.001, 1.4, 1.4]  # Box size

                # Add shape and pose to the CollisionObject
                collision_object_piece.primitives.append(primitive_piece)
                collision_object_piece.primitive_poses.append(piece_box_pose)
                collision_object_piece.operation = CollisionObject.ADD

                # Publish the CollisionObject for the ArUco piece
                self.pub.publish(collision_object_piece)
                rospy.loginfo("Published collision object for ArUco piece at modified position")

            if self.aruco_marker_0_pose is not None:
                # Create a deep copy of the received ArUco marker 0 pose
                marker_0_box_pose = copy.deepcopy(self.aruco_marker_0_pose)

                # Apply an offset to the ArUco marker 0's position
                marker_0_box_pose.position.x += 0.0  # Shift x by 0.5 meters, positive moves box away from robot
                marker_0_box_pose.position.y += -0.18  # Shift y by 0.0 meters, positive moves box left *form robot
                marker_0_box_pose.position.z += -0.34  # Shift z by -0.37 meters (negative lowers the box)

                # Create a CollisionObject message for the ArUco marker 0
                collision_object_marker_0 = CollisionObject()
                collision_object_marker_0.header = Header()
                collision_object_marker_0.header.frame_id = "base_link"
                collision_object_marker_0.id = "aruco_marker_0_collision_box"

                # Define the box's shape and dimensions
                primitive_marker_0 = SolidPrimitive()
                primitive_marker_0.type = SolidPrimitive.BOX
                primitive_marker_0.dimensions = [0.02, .48, .6]  # Box size

                # Add shape and pose to the CollisionObject
                collision_object_marker_0.primitives.append(primitive_marker_0)
                collision_object_marker_0.primitive_poses.append(marker_0_box_pose)
                collision_object_marker_0.operation = CollisionObject.ADD

                # Publish the CollisionObject for the ArUco marker 0
                self.pub.publish(collision_object_marker_0)
                rospy.loginfo("Published collision object for ArUco marker 0 at modified position")

            rate.sleep()

if __name__ == '__main__':
    try:
        node = CollisionObjectPublisher()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
