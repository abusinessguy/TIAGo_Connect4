#!/usr/bin/env python

import rospy
import actionlib
from geometry_msgs.msg import PoseStamped
from action_server.msg import MoveToPoseAction, MoveToPoseGoal

def send_goal():
    # Initialize ROS node
    rospy.init_node('send_goal_client')

    # Create an action client
    client = actionlib.SimpleActionClient('move_to_pose', MoveToPoseAction)

    # Wait for the action server to start
    rospy.loginfo("Waiting for action server to start...")
    client.wait_for_server()

    # Create a PoseStamped goal
    goal = MoveToPoseGoal()
    goal.pose.header.frame_id = "base_footprint"
    goal.pose.pose.position.x = 0.5
    goal.pose.pose.position.y = 0.0
    goal.pose.pose.position.z = 1.0
    goal.pose.pose.orientation.w = 1.0

    # Send the goal to the action server
    rospy.loginfo("Sending goal to action server...")
    client.send_goal(goal)

    # Wait for the result
    client.wait_for_result()

    # Print the result
    if client.get_result().success:
        rospy.loginfo("Goal achieved successfully!")
    else:
        rospy.logwarn("Failed to achieve the goal.")

if __name__ == '__main__':
    try:
        send_goal()
    except rospy.ROSInterruptException:
        pass

