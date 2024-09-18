#include <ros/ros.h>
#include <actionlib/server/simple_action_server.h>
#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>  // Include PlanningSceneInterface
#include <action_server/MoveToPoseAction.h>
#include <tf2/LinearMath/Quaternion.h>
#include <tf/tf.h>  // Include for quaternion operations

class MoveToPoseAction
{
protected:
  ros::NodeHandle nh_;
  actionlib::SimpleActionServer<action_server::MoveToPoseAction> as_;
  moveit::planning_interface::MoveGroupInterface move_group_;
  moveit::planning_interface::PlanningSceneInterface planning_scene_interface_;  // Add PlanningSceneInterface
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

    // Add collision objects to the planning scene
    addCollisionObjects();
  }

  void addCollisionObjects()
  {
    // Remove any existing box with the same ID
    std::vector<std::string> object_ids;
    object_ids.push_back("box");
    planning_scene_interface_.removeCollisionObjects(object_ids);

    // Wait for the scene to update
    ros::Duration(1.0).sleep();

    // Create a new box collision object
    moveit_msgs::CollisionObject collision_object;
    // Use either base_link or base_footprint depending on your use case
    collision_object.header.frame_id = "base_link";  // or "base_footprint" for ground-based reference
    //collision_object.header.frame_id = move_group_.getPlanningFrame();
    collision_object.id = "box";

    // Define the box size and pose
    shape_msgs::SolidPrimitive primitive;
    primitive.type = primitive.BOX;
    primitive.dimensions.resize(3);
    primitive.dimensions[0] = 0.3;  // Length
    primitive.dimensions[1] = 0.4;  // Width
    primitive.dimensions[2] = 0.5;  // Height

    // Set the position of the box
    geometry_msgs::Pose box_pose;
    box_pose.orientation.w = 1.0;
    box_pose.position.x = 0.0;  // Set new x-position
    box_pose.position.y = 0.0;  // Set new y-position
    box_pose.position.z = 0.0; // Set new height (z-position)

    // Add the box to the collision object
    collision_object.primitives.push_back(primitive);
    collision_object.primitive_poses.push_back(box_pose);
    collision_object.operation = collision_object.ADD;

    // Add the object to the planning scene
    std::vector<moveit_msgs::CollisionObject> collision_objects;
    collision_objects.push_back(collision_object);
    planning_scene_interface_.addCollisionObjects(collision_objects);

    ROS_INFO("Added a collision object to the planning scene.");
    ROS_INFO_STREAM("Box position: x=" << box_pose.position.x 
                    << ", y=" << box_pose.position.y
                    << ", z=" << box_pose.position.z);
    ROS_INFO_STREAM("Box size: length=" << primitive.dimensions[0]
                    << ", width=" << primitive.dimensions[1]
                    << ", height=" << primitive.dimensions[2]);

    // Wait for the scene to update
    ros::Duration(1.0).sleep();
  }

  void executeCB(const action_server::MoveToPoseGoalConstPtr &goal)
  {
      // Set the start state to the current state of the robot
      move_group_.setStartStateToCurrentState();

      // Copy the goal pose and override the orientation if needed
      geometry_msgs::Pose target_pose = goal->pose.pose;

      // Log the target pose
      ROS_INFO_STREAM("Target pose received: x=" << target_pose.position.x
                      << ", y=" << target_pose.position.y
                      << ", z=" << target_pose.position.z);

      // Set the goal pose for the robot
      move_group_.setPoseTarget(target_pose);

      // Plan the motion
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
