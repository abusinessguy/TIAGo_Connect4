#include <ros/ros.h>
#include <actionlib/server/simple_action_server.h>
#include <moveit/move_group_interface/move_group_interface.h>
#include <action_server/MoveToPoseAction.h>
#include <tf2/LinearMath/Quaternion.h>
#include <tf/tf.h>  // Include the necessary header for tf::createQuaternionMsgFromRollPitchYaw

class MoveToPoseAction
{
protected:
  ros::NodeHandle nh_;
  actionlib::SimpleActionServer<action_server::MoveToPoseAction> as_;
  moveit::planning_interface::MoveGroupInterface move_group_;
  std::string action_name_;

public:
  MoveToPoseAction(const std::string &name)
    : as_(nh_, name, boost::bind(&MoveToPoseAction::executeCB, this, _1), false),
      action_name_(name), move_group_("arm")
  {
    // Set the planner ID
    move_group_.setPlannerId("RRTConnectkConfigDefault");

    // Set the reference frame
    move_group_.setPoseReferenceFrame("base_footprint");

    // Set the velocity scaling factor
    move_group_.setMaxVelocityScalingFactor(0.5);

    // Set the planning time
    move_group_.setPlanningTime(10.0);

    as_.start();
  }

  void executeCB(const action_server::MoveToPoseGoalConstPtr &goal)
  {
      // Set the start state to the current state of the robot
      move_group_.setStartStateToCurrentState();

      // Copy the goal pose and override the orientation
      geometry_msgs::Pose target_pose = goal->pose.pose;  // Access the pose member explicitly

      // Define the fixed orientation using roll, pitch, and yaw
      // For example, 180 degrees around X-axis (M_PI radians)
      //target_pose.orientation = tf::createQuaternionMsgFromRollPitchYaw(-M_PI/2, 0.001, M_PI/2);  // Adjust RPY values as needed M_PI/2

      // Log the fixed orientation for verification
      ROS_INFO_STREAM("Using fixed orientation: x=" << target_pose.orientation.x
                      << ", y=" << target_pose.orientation.y
                      << ", z=" << target_pose.orientation.z
                      << ", w=" << target_pose.orientation.w);

      // Set the goal pose with the overridden orientation
      move_group_.setPoseTarget(target_pose);

      moveit::planning_interface::MoveGroupInterface::Plan my_plan;
      bool success = (move_group_.plan(my_plan) == moveit::planning_interface::MoveItErrorCode::SUCCESS);

      if (success)
      {
        move_group_.move();
        as_.setSucceeded();
      }
      else
      {
        as_.setAborted();
      }
  }

};

int main(int argc, char **argv)
{
  ros::init(argc, argv, "move_to_pose_action_server");
  MoveToPoseAction moveToPose("move_to_pose");
  ros::spin();
  return 0;
}
