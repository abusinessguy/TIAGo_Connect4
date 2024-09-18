#include <ros/ros.h>
#include <actionlib/server/simple_action_server.h>
#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <action_server/MoveToPoseAction.h>
#include <moveit_msgs/CollisionObject.h>
#include <tf2/LinearMath/Quaternion.h>
#include <tf/tf.h>  

class MoveToPoseAction
{
protected:
  ros::NodeHandle nh_;
  actionlib::SimpleActionServer<action_server::MoveToPoseAction> as_;
  moveit::planning_interface::MoveGroupInterface move_group_;
  moveit::planning_interface::PlanningSceneInterface planning_scene_interface_;
  ros::Subscriber collision_object_sub_;  // Subscriber for collision objects
  std::string action_name_;

public:
  MoveToPoseAction(const std::string &name)
    : as_(nh_, name, boost::bind(&MoveToPoseAction::executeCB, this, _1), false),
      action_name_(name), move_group_("arm")
  {
    // Set up the planning configuration
    move_group_.setPlannerId("RRTConnectkConfigDefault");
    move_group_.setPoseReferenceFrame("base_footprint");
    move_group_.setMaxVelocityScalingFactor(0.5);
    move_group_.setPlanningTime(20.0);

    // Subscribe to collision objects topic
    collision_object_sub_ = nh_.subscribe("/collision_objects", 10, &MoveToPoseAction::collisionObjectCallback, this);

    as_.start();
  }

  void collisionObjectCallback(const moveit_msgs::CollisionObject::ConstPtr &msg)
  {
    // Add the received collision object to the planning scene
    std::vector<moveit_msgs::CollisionObject> collision_objects;
    collision_objects.push_back(*msg);  // Add the received object to the list

    planning_scene_interface_.addCollisionObjects(collision_objects);
    ROS_INFO_STREAM("Received and added collision object: " << msg->id);
  }

  void executeCB(const action_server::MoveToPoseGoalConstPtr &goal)
  {
    // Set the start state to the current state of the robot
    move_group_.setStartStateToCurrentState();

    // Set the target pose and plan motion
    geometry_msgs::Pose target_pose = goal->pose.pose;
    move_group_.setPoseTarget(target_pose);

    moveit::planning_interface::MoveGroupInterface::Plan my_plan;
    bool success = (move_group_.plan(my_plan) == moveit::planning_interface::MoveItErrorCode::SUCCESS);

    if (success)
    {
      ROS_INFO("Motion plan successful. Executing...");
      move_group_.move();
      as_.setSucceeded();
    }
    else
    {
      ROS_WARN("Motion plan failed.");
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
