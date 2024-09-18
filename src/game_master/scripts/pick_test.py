#!/usr/bin/env python
import rospy
import actionlib
import numpy as np
import std_msgs.msg  # Add this line

from pal_interaction_msgs.msg import TtsAction, TtsGoal
from geometry_msgs.msg import PoseStamped
from action_server.msg import MoveToPoseAction, MoveToPoseGoal, ControlJointsAction, ControlJointsGoal

class PickTest:
    def __init__(self):
        rospy.init_node('pick_test_node')

        # Subscribe to the board state and AI move
        rospy.Subscriber("/aruco_piece/pick", PoseStamped, self.pick_position_callback)
        rospy.Subscriber("/aruco_piece/pick_wpoint", PoseStamped, self.pick_wpoint_position_callback)
        rospy.Subscriber("/hover_right_position", PoseStamped, self.hover_right_position_callback)
        rospy.Subscriber("/hover_left_position", PoseStamped, self.hover_left_position_callback)
        for i in range(7):
            rospy.Subscriber("/aruco_plane/pose_{}".format(i), PoseStamped, self.column_position_callback, callback_args=i)


        self.move_client = actionlib.SimpleActionClient('move_to_pose', MoveToPoseAction)
        self.move_client.wait_for_server()
        rospy.loginfo("Connected to move_to_pose server.")
        self.control_joints_client = actionlib.SimpleActionClient('control_joints', ControlJointsAction)
        self.control_joints_client.wait_for_server()
        rospy.loginfo("Connected to control_joints server.")

        # Define the waypoint in joint space as a dictionary
        self.MJPose = {
            'torso_lift': 0.35,
            'arm_joints': [.1, .98, -3.25, .58, 1.60, -.24, .37],
            'gripper_position': 0.0
        }
        self.MJPoseLeft = {
            'torso_lift': 0.35,
            'arm_joints': [2.65, .78, 1.5, .2, .5, -1,38, -1.6],
            #'arm_joints': [2.65, .78, 1.5, 1.1, .60, .14, 1.9],
            'gripper_position': 0.0
        }
        # Define the waypoint near pick zone in joint space as a dictionary
        self.pick_wp = {
            'torso_lift': 0.35,
            'arm_joints': [.15, .59, -1.32, .94, -2.04, .98, -.77],
            'gripper_position': 0.0
        }

        self.ai_move = 6


        # Initialize variables
        self.hover_right_position = None
        self.hover_left_position = None
        self.pick_position = None
        self.pick_wpoint_position = None

        rospy.loginfo("Pick test Node Started")
        self.play_game()

    def pick_position_callback(self, msg):
        self.pick_position = msg

    def hover_right_position_callback(self, msg):
        self.hover_right_position = msg  # Store the full PoseStamped message, not just the position

    def hover_left_position_callback(self, msg):
        self.hover_left_position = msg  # Store the full PoseStamped message, not just the position

    def column_position_callback(self, msg, index):
        # Initialize the list to store column positions if it doesn't exist
        if not hasattr(self, 'column_positions'):
            self.column_positions = [None] * 7
        # Store the pose based on the column index
        self.column_positions[index] = msg


    def pick_wpoint_position_callback(self, msg):
        self.pick_wpoint_position = msg  # Store the pick waypoint position

    def send_move_command(self, pose_msg):
        # Create a goal for the move action
        goal = MoveToPoseGoal()
        goal.pose = pose_msg  # Use the hover pose received

        # Send the goal to the move action server
        rospy.loginfo("Sending goal to move to hover position...")
        self.move_client.send_goal(goal)

        # Wait for the result
        self.move_client.wait_for_result()

        # Handle the result (e.g., check if the motion was successful)
        if self.move_client.get_result().success:
            rospy.loginfo("Successfully moved to commanded position.")
        else:
            rospy.logwarn("Failed to move to commanded position.")

    def send_control_joints_command(self, torso_lift, arm_joints, gripper_position):
        # Create a goal for the control joints action
        goal = ControlJointsGoal()

        # Set the torso_lift if provided
        if torso_lift is not None:
            goal.torso_lift = torso_lift
        else:
            goal.torso_lift = float('nan')  # Use NaN to indicate no change

        # Set the arm joints if provided
        if arm_joints is not None:
            goal.arm_1 = arm_joints[0]
            goal.arm_2 = arm_joints[1]
            goal.arm_3 = arm_joints[2]
            goal.arm_4 = arm_joints[3]
            goal.arm_5 = arm_joints[4]
            goal.arm_6 = arm_joints[5]
            goal.arm_7 = arm_joints[6]
        else:
            # Set arm joint goals to NaN if not specified to avoid altering them
            goal.arm_1 = float('nan')
            goal.arm_2 = float('nan')
            goal.arm_3 = float('nan')
            goal.arm_4 = float('nan')
            goal.arm_5 = float('nan')
            goal.arm_6 = float('nan')
            goal.arm_7 = float('nan')

        # Set the gripper position if provided
        if gripper_position is not None:
            goal.gripper_position = gripper_position
        else:
            goal.gripper_position = float('nan')  # Use NaN to indicate no change
        

        # Send the goal to the control joints action server
        rospy.loginfo("Sending command to control joints...")
        self.control_joints_client.send_goal(goal)

        # Wait for the result
        self.control_joints_client.wait_for_result()

        # Get the result
        result = self.control_joints_client.get_result()

        # Handle the result
        if result is None:
            rospy.logwarn("Control joints action did not return a result.")
        elif result.success:
            rospy.loginfo("Successfully controlled joints.")
        else:
            rospy.logwarn("Failed to control joints.")


    def play_game(self):
        rate = rospy.Rate(1)  # 1 Hz
        # self.talk("Going to M J position")
        self.send_control_joints_command(self.MJPose['torso_lift'], self.MJPose['arm_joints'], self.MJPose['gripper_position'])

        # Ensure that shutdown is properly handled
        while not rospy.is_shutdown() and not self.pick_position:
            rospy.logwarn("Pick position is not yet available.")
            rospy.sleep(5)

        if rospy.is_shutdown():
            rospy.loginfo("ROS is shutting down. Exiting...")
            return

        if self.pick_position:
            # The rest of your game logic continues here...
            self.send_control_joints_command(self.pick_wp['torso_lift'], self.pick_wp['arm_joints'], self.pick_wp['gripper_position'])
            self.send_control_joints_command(None, None, .1)
            self.send_move_command(self.pick_wpoint_position)
            self.send_move_command(self.pick_position)
            self.send_control_joints_command(None, None, 0)
            self.send_move_command(self.pick_wpoint_position)
            self.send_control_joints_command(self.pick_wp['torso_lift'], self.pick_wp['arm_joints'], self.pick_wp['gripper_position'])
            self.send_control_joints_command(self.MJPose['torso_lift'], self.MJPose['arm_joints'], self.MJPose['gripper_position'])

            if self.ai_move < 4:
                while not rospy.is_shutdown() and not self.hover_right_position:
                    rospy.logwarn("Hover position is not yet available.")
                    rospy.sleep(5)
                if rospy.is_shutdown():
                    rospy.loginfo("ROS is shutting down. Exiting...")
                    return

                if self.hover_right_position:
                    self.talk("Going to hover position")
                    self.send_move_command(self.hover_right_position)
                    self.talk("Going to column position{}".format(self.ai_move + 1))
                    self.send_move_command(self.column_positions[self.ai_move])
                    self.send_control_joints_command(None, None, .3)
                    self.send_control_joints_command(self.MJPose['torso_lift'], self.MJPose['arm_joints'], self.MJPose['gripper_position'])

            if self.ai_move > 3:
                self.send_control_joints_command(self.MJPoseLeft['torso_lift'], self.MJPoseLeft['arm_joints'], self.MJPoseLeft['gripper_position'])
                while not rospy.is_shutdown() and not self.hover_left_position:
                    rospy.logwarn("Hover position is not yet available.")
                    rospy.sleep(5)
                if rospy.is_shutdown():
                    rospy.loginfo("ROS is shutting down. Exiting...")
                    return

                if self.hover_left_position:
                    self.talk("Going to hover position")
                    self.send_move_command(self.hover_left_position)
                    self.talk("Going to column position{}".format(self.ai_move + 1))
                    self.send_move_command(self.column_positions[self.ai_move])
                    self.send_control_joints_command(None, None, .3)
                    self.send_control_joints_command(self.MJPoseLeft['torso_lift'], self.MJPoseLeft['arm_joints'], self.MJPoseLeft['gripper_position'])
                    self.send_control_joints_command(self.MJPose['torso_lift'], self.MJPose['arm_joints'], self.MJPose['gripper_position'])

            rospy.sleep(1)



    def talk(self, text):
        client = actionlib.SimpleActionClient('/tts', TtsAction)
        client.wait_for_server()

        goal = TtsGoal()
        goal.rawtext.text = text
        goal.rawtext.lang_id = "en_GB"  # Set language, e.g., en_GB for English (UK)

        client.send_goal(goal)
        client.wait_for_result()
        return client.get_result()



if __name__ == "__main__":
    try:
        pick_test = PickTest()
    except rospy.ROSInterruptException:
        pass

