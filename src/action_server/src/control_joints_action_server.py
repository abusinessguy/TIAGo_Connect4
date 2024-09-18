#!/usr/bin/env python



import rospy
import actionlib
import moveit_commander
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectoryPoint
from action_server.msg import ControlJointsAction, ControlJointsGoal

class ControlJointsActionServer:
    def __init__(self):
        rospy.init_node('control_joints_action_server')
        
        # Initialize MoveIt commander and the gripper action client
        self.move_group = moveit_commander.MoveGroupCommander("arm_torso")
        self.move_group.set_planning_time(20.0)
        self.move_group.set_max_velocity_scaling_factor(0.5)
        self.move_group.set_pose_reference_frame("base_footprint")
        
        self.gripper_client = actionlib.SimpleActionClient("/parallel_gripper_controller/follow_joint_trajectory", FollowJointTrajectoryAction)
        rospy.loginfo("Waiting for gripper action server...")
        self.gripper_client.wait_for_server()
        rospy.loginfo("Gripper action server started.")

        self.server = actionlib.SimpleActionServer('control_joints', ControlJointsAction, self.execute_cb, False)
        self.server.start()

    def execute_cb(self, goal):
        # Set joint target for the arm and torso
        current_joint_values = self.move_group.get_current_joint_values()
        joint_names = self.move_group.get_active_joints()

        joint_values = {joint: current_joint_values[i] for i, joint in enumerate(joint_names)}

        # Update the joint targets from the goal (only update non-NaN values)
        if not rospy.is_shutdown():
            if goal.torso_lift is not None:
                joint_values["torso_lift_joint"] = goal.torso_lift

            if goal.arm_1 is not None:
                joint_values["arm_1_joint"] = goal.arm_1

            # Repeat for other arm joints...

            self.move_group.set_joint_value_target(joint_values)

            # Set the start state to the robot's current state before planning
            self.move_group.set_start_state_to_current_state()

            # Plan the motion
            plan = self.move_group.plan()

            # Check if the plan is valid
            if plan.joint_trajectory.points:
                # Execute the plan
                self.move_group.execute(plan, wait=True)
                self.send_gripper_goal(goal.gripper_position)
            else:
                rospy.logwarn("Planning failed or returned an empty plan.")
                self.server.set_aborted()


    def send_gripper_goal(self, gripper_position):
        gripper_goal = FollowJointTrajectoryGoal()
        gripper_goal.trajectory.joint_names = ["gripper_joint"]
        point = JointTrajectoryPoint()
        point.positions = [gripper_position]
        point.time_from_start = rospy.Duration(1.0)
        gripper_goal.trajectory.points = [point]

        self.gripper_client.send_goal(gripper_goal)
        self.gripper_client.wait_for_result()
        
        if self.gripper_client.get_state() == actionlib.GoalStatus.SUCCEEDED:
            self.server.set_succeeded()
        else:
            rospy.logwarn("Gripper control failed.")
            self.server.set_aborted()

if __name__ == '__main__':
    server = ControlJointsActionServer()
    rospy.spin()

