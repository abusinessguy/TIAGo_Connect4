#include <ros/ros.h>
#include <geometry_msgs/PoseStamped.h>
#include <moveit/move_group_interface/move_group_interface.h>

geometry_msgs::PoseStamped goal_pose;

void goalPoseCallback(const geometry_msgs::PoseStamped::ConstPtr &msg) {
  goal_pose = *msg;
}

int main(int argc, char **argv) {
  ros::init(argc, argv, "plan_arm_torso_ik");

  ros::NodeHandle nh;
  ros::Subscriber sub = nh.subscribe("/aruco_piece/pick", 1, goalPoseCallback);

  ros::AsyncSpinner spinner(1);
  spinner.start();

  moveit::planning_interface::MoveGroupInterface group_arm_torso("arm_torso");
  group_arm_torso.setPoseReferenceFrame("base_footprint");

  while (ros::ok()) {
    if (goal_pose.header.frame_id != "") {
      group_arm_torso.setPoseTarget(goal_pose);

      moveit::planning_interface::MoveGroupInterface::Plan my_plan;
      bool success = (group_arm_torso.plan(my_plan) == moveit::planning_interface::MoveItErrorCode::SUCCESS);

      if (success) {
        ROS_INFO("Plan found, executing...");
        group_arm_torso.move();
        ROS_INFO("Execution completed.");
      } else {
        ROS_WARN("No plan found.");
      }

      // Reset the goal pose to avoid re-execution
      goal_pose.header.frame_id = "";
    }

    ros::Duration(0.1).sleep();
  }

  spinner.stop();
  return 0;
}
