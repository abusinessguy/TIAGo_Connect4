# Install script for directory: /uio/kant/ifi-ansatt-u02/calvint/catkin_ws/src/action_server

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/uio/kant/ifi-ansatt-u02/calvint/catkin_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/action_server/action" TYPE FILE FILES
    "/uio/kant/ifi-ansatt-u02/calvint/catkin_ws/src/action_server/action/MoveToPose.action"
    "/uio/kant/ifi-ansatt-u02/calvint/catkin_ws/src/action_server/action/ControlJoints.action"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/action_server/msg" TYPE FILE FILES
    "/uio/kant/ifi-ansatt-u02/calvint/catkin_ws/devel/share/action_server/msg/MoveToPoseAction.msg"
    "/uio/kant/ifi-ansatt-u02/calvint/catkin_ws/devel/share/action_server/msg/MoveToPoseActionGoal.msg"
    "/uio/kant/ifi-ansatt-u02/calvint/catkin_ws/devel/share/action_server/msg/MoveToPoseActionResult.msg"
    "/uio/kant/ifi-ansatt-u02/calvint/catkin_ws/devel/share/action_server/msg/MoveToPoseActionFeedback.msg"
    "/uio/kant/ifi-ansatt-u02/calvint/catkin_ws/devel/share/action_server/msg/MoveToPoseGoal.msg"
    "/uio/kant/ifi-ansatt-u02/calvint/catkin_ws/devel/share/action_server/msg/MoveToPoseResult.msg"
    "/uio/kant/ifi-ansatt-u02/calvint/catkin_ws/devel/share/action_server/msg/MoveToPoseFeedback.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/action_server/msg" TYPE FILE FILES
    "/uio/kant/ifi-ansatt-u02/calvint/catkin_ws/devel/share/action_server/msg/ControlJointsAction.msg"
    "/uio/kant/ifi-ansatt-u02/calvint/catkin_ws/devel/share/action_server/msg/ControlJointsActionGoal.msg"
    "/uio/kant/ifi-ansatt-u02/calvint/catkin_ws/devel/share/action_server/msg/ControlJointsActionResult.msg"
    "/uio/kant/ifi-ansatt-u02/calvint/catkin_ws/devel/share/action_server/msg/ControlJointsActionFeedback.msg"
    "/uio/kant/ifi-ansatt-u02/calvint/catkin_ws/devel/share/action_server/msg/ControlJointsGoal.msg"
    "/uio/kant/ifi-ansatt-u02/calvint/catkin_ws/devel/share/action_server/msg/ControlJointsResult.msg"
    "/uio/kant/ifi-ansatt-u02/calvint/catkin_ws/devel/share/action_server/msg/ControlJointsFeedback.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/action_server/cmake" TYPE FILE FILES "/uio/kant/ifi-ansatt-u02/calvint/catkin_ws/build/action_server/catkin_generated/installspace/action_server-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/uio/kant/ifi-ansatt-u02/calvint/catkin_ws/devel/include/action_server")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/uio/kant/ifi-ansatt-u02/calvint/catkin_ws/devel/share/roseus/ros/action_server")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/uio/kant/ifi-ansatt-u02/calvint/catkin_ws/devel/share/common-lisp/ros/action_server")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/uio/kant/ifi-ansatt-u02/calvint/catkin_ws/devel/share/gennodejs/ros/action_server")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python2" -m compileall "/uio/kant/ifi-ansatt-u02/calvint/catkin_ws/devel/lib/python2.7/dist-packages/action_server")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages" TYPE DIRECTORY FILES "/uio/kant/ifi-ansatt-u02/calvint/catkin_ws/devel/lib/python2.7/dist-packages/action_server")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/uio/kant/ifi-ansatt-u02/calvint/catkin_ws/build/action_server/catkin_generated/installspace/action_server.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/action_server/cmake" TYPE FILE FILES "/uio/kant/ifi-ansatt-u02/calvint/catkin_ws/build/action_server/catkin_generated/installspace/action_server-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/action_server/cmake" TYPE FILE FILES
    "/uio/kant/ifi-ansatt-u02/calvint/catkin_ws/build/action_server/catkin_generated/installspace/action_serverConfig.cmake"
    "/uio/kant/ifi-ansatt-u02/calvint/catkin_ws/build/action_server/catkin_generated/installspace/action_serverConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/action_server" TYPE FILE FILES "/uio/kant/ifi-ansatt-u02/calvint/catkin_ws/src/action_server/package.xml")
endif()

