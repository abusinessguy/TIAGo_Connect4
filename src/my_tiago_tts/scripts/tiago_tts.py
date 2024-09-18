#!/usr/bin/env python
import rospy
import actionlib
from pal_interaction_msgs.msg import TtsAction, TtsGoal

def talk(text):
    # Create an action client
    client = actionlib.SimpleActionClient('/tts', TtsAction)
    
    # Wait until the action server has started up and started listening for goals
    client.wait_for_server()

    # Create a goal to send to the action server
    goal = TtsGoal()
    goal.rawtext.text = text
    goal.rawtext.lang_id = "en_GB"  # Set language, e.g., en_GB for English (UK)

    # Send the goal to the action server
    client.send_goal(goal)

    # Wait for the server to finish performing the action
    client.wait_for_result()

    # Print the result of the action
    return client.get_result()

if __name__ == '__main__':
    rospy.init_node('tiago_talker')
    text = "Hello, I am TIAGo."
    result = talk(text)
    rospy.loginfo("TIAGo says: %s", text)

