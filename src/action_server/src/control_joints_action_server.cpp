#include <ros/ros.h>
#include <actionlib/server/simple_action_server.h>
#include <moveit/move_group_interface/move_group_interface.h>
#include <control_msgs/FollowJointTrajectoryAction.h>  // For the parallel gripper
#include <action_server/ControlJointsAction.h>  // Custom action message
#include <trajectory_msgs/JointTrajectory.h>
#include <trajectory_msgs/JointTrajectoryPoint.h>
#include <tf2/LinearMath/Quaternion.h>
#include <tf/tf.h> 

class ControlJointsAction
{
protected:
  ros::NodeHandle nh_;
  actionlib::SimpleActionServer<action_server::ControlJointsAction> as_;
  moveit::planning_interface::MoveGroupInterface move_group_;
  actionlib::SimpleActionClient<control_msgs::FollowJointTrajectoryAction> gripper_client_;

public:
  ControlJointsAction(const std::string &name)
    : as_(nh_, name, boost::bind(&ControlJointsAction::executeCB, this, _1), false),
      move_group_("arm_torso"),
      gripper_client_("/parallel_gripper_controller/follow_joint_trajectory", true)
  {
    move_group_.setPlannerId("RRTConnectkConfigDefault");
    move_group_.setPoseReferenceFrame("base_footprint");
    move_group_.setMaxVelocityScalingFactor(0.5);
    move_group_.setPlanningTime(20.0);

    // Wait for the gripper action server with timeout and error handling
    ROS_INFO("Waiting for gripper action server to start...");
    if (!gripper_client_.waitForServer(ros::Duration(5.0))) {
      ROS_ERROR("Gripper action server not available. Aborting startup.");
      ros::shutdown();
      return;
    }
    ROS_INFO("Gripper action server started.");

    as_.start();
  }

  bool waitForRobotState(double timeout) {
    ros::Time start_time = ros::Time::now();
    while ((ros::Time::now() - start_time).toSec() < timeout) {
        if (move_group_.getCurrentState()) {
            return true;
        }
        ros::Duration(0.1).sleep(); // Wait for 100 ms before checking again
    }
    return false;
    }

  void executeCB(const action_server::ControlJointsGoalConstPtr &goal)
  {
      if (!waitForRobotState(5.0)) {  // Wait for 5 seconds
        ROS_ERROR("Failed to fetch current robot state. Aborting.");
        as_.setAborted();
        return;
      }

      move_group_.setStartStateToCurrentState();

      // Get current joint values
      std::vector<double> current_joint_values = move_group_.getCurrentJointValues();
      std::vector<std::string> joint_names = move_group_.getJoints();

      // Map joint names to their current values
      std::map<std::string, double> joint_values_map;
      for (size_t i = 0; i < joint_names.size(); ++i)
      {
          joint_values_map[joint_names[i]] = current_joint_values[i];
      }

      // Set targets, preserving current values where necessary
      if (!std::isnan(goal->torso_lift))
      {
          joint_values_map["torso_lift_joint"] = goal->torso_lift;
      }

      if (!std::isnan(goal->arm_1))
      {
          joint_values_map["arm_1_joint"] = goal->arm_1;
      }
      
      if (!std::isnan(goal->arm_2))
      {
          joint_values_map["arm_2_joint"] = goal->arm_2;
      }
      
      if (!std::isnan(goal->arm_3))
      {
          joint_values_map["arm_3_joint"] = goal->arm_3;
      }
      
      if (!std::isnan(goal->arm_4))
      {
          joint_values_map["arm_4_joint"] = goal->arm_4;
      }
      
      if (!std::isnan(goal->arm_5))
      {
          joint_values_map["arm_5_joint"] = goal->arm_5;
      }
      
      if (!std::isnan(goal->arm_6))
      {
          joint_values_map["arm_6_joint"] = goal->arm_6;
      }
      
      if (!std::isnan(goal->arm_7))
      {
          joint_values_map["arm_7_joint"] = goal->arm_7;
      }

      // Set joint values for the move_group
      for (const auto &joint : joint_values_map)
      {
          move_group_.setJointValueTarget(joint.first, joint.second);
      }

      moveit::planning_interface::MoveGroupInterface::Plan my_plan;
      bool success = (move_group_.plan(my_plan) == moveit::planning_interface::MoveItErrorCode::SUCCESS);

      if (success)
      {
           ROS_INFO("Plan successful. Executing...");
           move_group_.move();

            // Check for move completion before proceeding
            if (move_group_.execute(my_plan) != moveit::planning_interface::MoveItErrorCode::SUCCESS) {
                ROS_WARN("Movement execution failed.");
                as_.setAborted();
                return;
            }

          // Create and send the gripper goal
          control_msgs::FollowJointTrajectoryGoal gripper_goal;
          gripper_goal.trajectory.joint_names.push_back("gripper_joint");  // Adjust this to your gripper joint name
          trajectory_msgs::JointTrajectoryPoint point;
          point.positions.push_back(goal->gripper_position);
          point.time_from_start = ros::Duration(1.0);  // 1 second to reach the goal
          gripper_goal.trajectory.points.push_back(point);

          gripper_client_.sendGoal(gripper_goal);
          gripper_client_.waitForResult();

          if (gripper_client_.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
          {
              as_.setSucceeded();
          }
          else
          {
              ROS_WARN("Gripper control failed.");
              as_.setAborted();
          }
      }
      else
      {
          ROS_WARN("Planning failed.");
          as_.setAborted();
      }
  }

};

int main(int argc, char **argv)
{
  ros::init(argc, argv, "control_joints_action_server");
  ControlJointsAction controlJoints("control_joints");
  ros::spin();
  return 0;
}
