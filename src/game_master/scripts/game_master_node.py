#!/usr/bin/env python
import rospy
import actionlib
import numpy as np
import std_msgs.msg  # Add this line

from board_detection.msg import BoardState
from move_decision.msg import Move
from pal_interaction_msgs.msg import TtsAction, TtsGoal
from geometry_msgs.msg import PoseStamped
from action_server.msg import MoveToPoseAction, MoveToPoseGoal, ControlJointsAction, ControlJointsGoal

class GameMaster:
    def __init__(self):
        rospy.init_node('game_master_node')

        # Flag to track whether the game has officially started
        self.game_started = False
        self.ai_move_made = False  # Track if the AI has made its move

        # Subscribe to the board state and AI move
        rospy.Subscriber('/board_state', BoardState, self.board_state_callback)
        rospy.Subscriber('/ai_move', Move, self.ai_move_callback)
        rospy.Subscriber("/hover_left_position", PoseStamped, self.hover_left_position_callback)
        rospy.Subscriber("/hover_right_position", PoseStamped, self.hover_right_position_callback)
        rospy.Subscriber("/aruco_piece/pick", PoseStamped, self.pick_position_callback)
        rospy.Subscriber("/aruco_piece/pick_wpoint", PoseStamped, self.pick_wpoint_position_callback)
        for i in range(7):
            rospy.Subscriber("/aruco_plane/pose_{}".format(i), PoseStamped, self.column_position_callback, callback_args=i)

        

        # Publisher for indicating whose turn it is (AI or human)
        self.turn_pub = rospy.Publisher('/turn_indicator', std_msgs.msg.String, queue_size=10)

        # Publisher for the AI's move
        self.ai_move_pub = rospy.Publisher('/ai_move', Move, queue_size=10)

        self.current_board = None
        self.ai_move = None
        self.game_over = False
        self.current_turn = None
        self.TurnCounter = 0
        self.LastMove = None
        self.winner = 0
        self.player = None

        # # Define the waypoint pose
        # self.waypoint_pose = PoseStamped()
        # self.waypoint_pose.header.frame_id = "base_link"  # Adjust this to the appropriate frame of reference
        # self.waypoint_pose.pose.position.x = 0.0
        # self.waypoint_pose.pose.position.y = 0.5
        # self.waypoint_pose.pose.position.z = 0.70
        # self.waypoint_pose.pose.orientation.w = 1.0  # Assuming neutral orientation

        self.move_client = actionlib.SimpleActionClient('move_to_pose', MoveToPoseAction)
        self.move_client.wait_for_server()
        rospy.loginfo("Connected to move_to_pose server.")
        self.control_joints_client = actionlib.SimpleActionClient('control_joints', ControlJointsAction)
        self.control_joints_client.wait_for_server()
        rospy.loginfo("Connected to control_joints server.")

        # Define the waypoint in joint space as a dictionary
        self.MJPoseRight = {
            'torso_lift': 0.35,
            'arm_joints': [.1, .98, -3.25, .58, -1.60, -.24, .37],
            'gripper_position': 0.0
        }
        self.MJPoseLeft = {
            'torso_lift': 0.35,
            'arm_joints': [2.65, .78, 1.5, .2, .5, -1,38, -1.6],
            'gripper_position': 0.0
        }
        # Define the waypoint near pick zone in joint space as a dictionary
        self.pick_wp = {
            'torso_lift': 0.35,
            'arm_joints': [.15, .59, -1.32, .94, -2.04, .98, -.77],
            'gripper_position': 0.0
        }


        # Initialize variables
        self.hover_left_position = None
        self.hover_right_position = None
        self.pick_position = None
        self.pick_wpoint_position = None

        rospy.loginfo("Game Master Node Started")
        self.play_game()

    def hover_right_position_callback(self, msg):
        self.hover_right_position = msg  # Store the full PoseStamped message, not just the position

    def hover_left_position_callback(self, msg):
        self.hover_left_position = msg  # Store the full PoseStamped message, not just the position

    def pick_position_callback(self, msg):
        self.pick_position = msg

    def pick_wpoint_position_callback(self, msg):
        self.pick_wpoint_position = msg  # Store the pick waypoint position

    def column_position_callback(self, msg, index):
        # Initialize the list to store column positions if it doesn't exist
        if not hasattr(self, 'column_positions'):
            self.column_positions = [None] * 7

        # Store the pose based on the column index
        self.column_positions[index] = msg

    def send_move_command(self, pose_msg):
        # Create a goal for the move action
        goal = MoveToPoseGoal()
        goal.pose = pose_msg  # Use the hover pose received

        # Send the goal to the move action server
        rospy.loginfo("Sending goal to move to position...")
        self.move_client.send_goal(goal)

        # Wait for the result
        self.move_client.wait_for_result()

        # Handle the result (e.g., check if the motion was successful)
        if self.move_client.get_result().success:
            rospy.loginfo("Successfully moved to position.")
        else:
            rospy.logwarn("Failed to move to position.")

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



    def board_state_callback(self, msg):
        self.current_board = msg.state
        rospy.loginfo("Received board state update.")

        # Check if it's AI's turn and a move hasn't been made yet, and the game has started
        if self.current_turn == 'AI' and self.ai_move is not None and self.game_started and not self.ai_move_made:
            rospy.loginfo("AI making its move...")
            self.handle_ai_turn()

    def ai_move_callback(self, msg):
        self.ai_move = msg.column
        self.TurnCounter = msg.TurnCounter
        self.winner = msg.winner
        self.player = msg.player

        #rospy.loginfo("AI has decided to move to column: {}".format(self.ai_move + 1))

    def play_game(self):
        rate = rospy.Rate(1)  # 1 Hz
        #self.talk("Going to M J position")
        self.send_control_joints_command(self.MJPoseRight['torso_lift'], self.MJPoseRight['arm_joints'], self.MJPoseRight['gripper_position'])
        rospy.sleep(.6)

        # Wait for the board to be empty before starting the game
        while not rospy.is_shutdown():
            if self.current_board is not None and np.all(np.array(self.current_board) == 0):
                rospy.loginfo("Board is confirmed empty. Starting the game...")
                self.game_started = True  # Set the flag indicating the game has started
                break

            rospy.logwarn("Waiting for the board to be consistently empty before starting...")
            rate.sleep()

        while not rospy.is_shutdown() and not self.game_over and self.game_started:
            rospy.loginfo("Turn counter: {}".format(self.TurnCounter))
            if self.winner != 0:
                rospy.loginfo("There is a winner")
                if self.winner == 1:
                    winner_text = "You win... next time victory shal be mine human"
                if self.winner == 2:
                    winner_text = "I win! Good effort human"
                self.game_over = True
                self.talk(winner_text)  # Use the TTS function to speak the move
                return
            else:
                if self.player == 2:
                    self.handle_ai_turn()
                if self.player == 1:
                    self.handle_human_turn()
            rate.sleep()

    def handle_ai_turn(self):
        if self.current_board is None:
            rospy.logwarn("Waiting for initial board state...")
            return

        rospy.loginfo("AI's turn...")
        
        # Announce AI's move
        self.turn_pub.publish("AI")
        while self.ai_move is None:
            #rospy.loginfo("Thinking...")
            rospy.sleep(1)
        if self.TurnCounter != self.LastMove:
            self.announce_move(self.ai_move + 1)  # Convert to 1-based index
            

             # Move to pick position
            while not self.pick_position:
                rospy.logwarn("Pick position is not yet available.")
                rospy.sleep(5)
            if self.pick_position:

                #self.talk("Going to joint commanded way point")
                self.send_control_joints_command(self.pick_wp['torso_lift'], self.pick_wp['arm_joints'], self.pick_wp['gripper_position'])

                # Open Gripper
                # self.talk("Opening gripper to  point 1")
                self.send_control_joints_command(None, None, .1)

                #self.talk("Going to position commanded way point")
                self.send_move_command(self.pick_wpoint_position)

                #self.talk("Going to Pick position")
                self.send_move_command(self.pick_position)
                #self.send_control_joints_command(0.31, None, None)
                rospy.sleep(1)

                # Close Gripper
                #self.talk("Closing gripper")
                self.send_control_joints_command(None, None, 0)
                # rospy.sleep(1)
                # self.send_control_joints_command(0.35, None, None)
                # rospy.sleep(1)

                #self.talk("Returning to way position commanded way point")
                self.send_move_command(self.pick_wpoint_position)

                #self.talk("Returning to joint commanded way point")
                self.send_control_joints_command(self.pick_wp['torso_lift'], self.pick_wp['arm_joints'], self.pick_wp['gripper_position'])

                #self.talk("Returning to M J position")
                self.send_control_joints_command(self.MJPoseRight['torso_lift'], self.MJPoseRight['arm_joints'], self.MJPoseRight['gripper_position'])

                if self.ai_move < 4:
                
                    # Move to hover position
                    while not self.hover_right_position:
                        rospy.logwarn("Hover position is not yet available.")
                        rospy.sleep(5)
                    if self.hover_right_position:
                        #self.talk("Going to hover position")
                        self.send_move_command(self.hover_right_position)
                        #rospy.sleep(1)
                        #Go to Column
                        self.talk("Going to column position{}".format(self.ai_move+1))
                        self.send_move_command(self.column_positions[self.ai_move])
                        #rospy.sleep(1)
                        # Open Gripper
                        self.send_control_joints_command(None, None, .3)
                        #self.talk("Returning to M J position")
                        self.send_control_joints_command(self.MJPoseRight['torso_lift'], self.MJPoseRight['arm_joints'], self.MJPoseRight['gripper_position'])

                if self.ai_move > 3:
                    self.send_control_joints_command(self.MJPoseLeft['torso_lift'], self.MJPoseLeft['arm_joints'], self.MJPoseLeft['gripper_position'])
                    # Move to hover position
                    while not self.hover_left_position:
                        rospy.logwarn("Hover position is not yet available.")
                        rospy.sleep(5)
                    if self.hover_left_position:
                        #self.talk("Going to hover position")
                        self.send_move_command(self.hover_left_position)
                        #rospy.sleep(1)
                        #Go to Column
                        self.talk("Going to column position{}".format(self.ai_move+1))
                        self.send_move_command(self.column_positions[self.ai_move])
                        #rospy.sleep(1)
                        # Open Gripper
                        self.send_control_joints_command(None, None, .3)
                        #self.talk("Returning to M J position")
                        self.send_control_joints_command(self.MJPoseLeft['torso_lift'], self.MJPoseLeft['arm_joints'], self.MJPoseLeft['gripper_position'])
                        self.send_control_joints_command(self.MJPoseRight['torso_lift'], self.MJPoseRight['arm_joints'], self.MJPoseRight['gripper_position'])

                
                rospy.sleep(1)

            # AI makes the move (this would need to be detected by the camera)
            #self.ai_move_pub.publish(self.ai_move)
            self.ai_move_made = True  # Mark that the AI has made its move
            self.LastMove = self.TurnCounter
            
            # # Wait for the camera to detect the move and update the board state
            # rospy.loginfo("Waiting for the camera to detect AI's move...")
            # previous_board = self.current_board[:]
            # while not rospy.is_shutdown():
            #     rospy.sleep(0.1)  # Small delay to avoid busy-waiting
                
            #     # Check if the board state has been updated by the camera
            #     if not np.array_equal(self.current_board, previous_board):
            #         rospy.loginfo("AI's move detected by camera.")
            #         self.current_turn = 'Human'  # Switch to human's turn after detecting the move
            #         self.ai_move_made = False  # Reset the flag for the next AI turn
            #         break

    def handle_human_turn(self):
        rospy.loginfo("Waiting for human's move...")
        yourturn_text = "Your turn."
        #self.talk("Returning to M J position")
        self.send_control_joints_command(self.MJPoseRight['torso_lift'], self.MJPoseRight['arm_joints'], self.MJPoseRight['gripper_position'])
        rospy.sleep(.6)
        # Close Gripper
        self.send_control_joints_command(None, None, 0)
        #rospy.loginfo("Announcing move: {}".format(move_text))
        self.talk(yourturn_text)  # Use the TTS function to speak the move
        self.turn_pub.publish("Human")

        # Store the current board state
        previous_board = self.current_board[:]
        previous_sum = np.sum(previous_board)

        # Wait for a valid change in the board state
        while not rospy.is_shutdown():
            rospy.sleep(0.1)  # Small sleep to prevent busy-waiting

            # Calculate the sum of the current board state
            current_sum = np.sum(self.current_board)

            # Check if the board state has changed and if the sum is as expected
        #     if not np.array_equal(self.current_board, previous_board) and (current_sum == previous_sum + 2 or current_sum == previous_sum + 1):
        #         rospy.loginfo("Human has made a move.")
        # #             self.current_turn = 'AI'  # Switch to AI's turn after human move is detected
            if self.player == 2:
                # self.handle_ai_turn()
                break

    def announce_move(self, move):
        # Announce the move out loud using TTS
        move_text = "I choose column {}".format(move)
        rospy.loginfo("Announcing move: {}".format(move_text))
        self.talk(move_text)  # Use the TTS function to speak the move

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
        game_master = GameMaster()
    except rospy.ROSInterruptException:
        pass

