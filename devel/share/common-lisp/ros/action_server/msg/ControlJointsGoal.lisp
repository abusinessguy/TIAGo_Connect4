; Auto-generated. Do not edit!


(cl:in-package action_server-msg)


;//! \htmlinclude ControlJointsGoal.msg.html

(cl:defclass <ControlJointsGoal> (roslisp-msg-protocol:ros-message)
  ((torso_lift
    :reader torso_lift
    :initarg :torso_lift
    :type cl:float
    :initform 0.0)
   (arm_1
    :reader arm_1
    :initarg :arm_1
    :type cl:float
    :initform 0.0)
   (arm_2
    :reader arm_2
    :initarg :arm_2
    :type cl:float
    :initform 0.0)
   (arm_3
    :reader arm_3
    :initarg :arm_3
    :type cl:float
    :initform 0.0)
   (arm_4
    :reader arm_4
    :initarg :arm_4
    :type cl:float
    :initform 0.0)
   (arm_5
    :reader arm_5
    :initarg :arm_5
    :type cl:float
    :initform 0.0)
   (arm_6
    :reader arm_6
    :initarg :arm_6
    :type cl:float
    :initform 0.0)
   (arm_7
    :reader arm_7
    :initarg :arm_7
    :type cl:float
    :initform 0.0)
   (gripper_position
    :reader gripper_position
    :initarg :gripper_position
    :type cl:float
    :initform 0.0))
)

(cl:defclass ControlJointsGoal (<ControlJointsGoal>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <ControlJointsGoal>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'ControlJointsGoal)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name action_server-msg:<ControlJointsGoal> is deprecated: use action_server-msg:ControlJointsGoal instead.")))

(cl:ensure-generic-function 'torso_lift-val :lambda-list '(m))
(cl:defmethod torso_lift-val ((m <ControlJointsGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader action_server-msg:torso_lift-val is deprecated.  Use action_server-msg:torso_lift instead.")
  (torso_lift m))

(cl:ensure-generic-function 'arm_1-val :lambda-list '(m))
(cl:defmethod arm_1-val ((m <ControlJointsGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader action_server-msg:arm_1-val is deprecated.  Use action_server-msg:arm_1 instead.")
  (arm_1 m))

(cl:ensure-generic-function 'arm_2-val :lambda-list '(m))
(cl:defmethod arm_2-val ((m <ControlJointsGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader action_server-msg:arm_2-val is deprecated.  Use action_server-msg:arm_2 instead.")
  (arm_2 m))

(cl:ensure-generic-function 'arm_3-val :lambda-list '(m))
(cl:defmethod arm_3-val ((m <ControlJointsGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader action_server-msg:arm_3-val is deprecated.  Use action_server-msg:arm_3 instead.")
  (arm_3 m))

(cl:ensure-generic-function 'arm_4-val :lambda-list '(m))
(cl:defmethod arm_4-val ((m <ControlJointsGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader action_server-msg:arm_4-val is deprecated.  Use action_server-msg:arm_4 instead.")
  (arm_4 m))

(cl:ensure-generic-function 'arm_5-val :lambda-list '(m))
(cl:defmethod arm_5-val ((m <ControlJointsGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader action_server-msg:arm_5-val is deprecated.  Use action_server-msg:arm_5 instead.")
  (arm_5 m))

(cl:ensure-generic-function 'arm_6-val :lambda-list '(m))
(cl:defmethod arm_6-val ((m <ControlJointsGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader action_server-msg:arm_6-val is deprecated.  Use action_server-msg:arm_6 instead.")
  (arm_6 m))

(cl:ensure-generic-function 'arm_7-val :lambda-list '(m))
(cl:defmethod arm_7-val ((m <ControlJointsGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader action_server-msg:arm_7-val is deprecated.  Use action_server-msg:arm_7 instead.")
  (arm_7 m))

(cl:ensure-generic-function 'gripper_position-val :lambda-list '(m))
(cl:defmethod gripper_position-val ((m <ControlJointsGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader action_server-msg:gripper_position-val is deprecated.  Use action_server-msg:gripper_position instead.")
  (gripper_position m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <ControlJointsGoal>) ostream)
  "Serializes a message object of type '<ControlJointsGoal>"
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'torso_lift))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'arm_1))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'arm_2))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'arm_3))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'arm_4))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'arm_5))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'arm_6))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'arm_7))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'gripper_position))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <ControlJointsGoal>) istream)
  "Deserializes a message object of type '<ControlJointsGoal>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'torso_lift) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'arm_1) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'arm_2) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'arm_3) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'arm_4) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'arm_5) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'arm_6) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'arm_7) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'gripper_position) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<ControlJointsGoal>)))
  "Returns string type for a message object of type '<ControlJointsGoal>"
  "action_server/ControlJointsGoal")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ControlJointsGoal)))
  "Returns string type for a message object of type 'ControlJointsGoal"
  "action_server/ControlJointsGoal")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<ControlJointsGoal>)))
  "Returns md5sum for a message object of type '<ControlJointsGoal>"
  "330b6114482d9def04dc8ca1d950eb95")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'ControlJointsGoal)))
  "Returns md5sum for a message object of type 'ControlJointsGoal"
  "330b6114482d9def04dc8ca1d950eb95")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<ControlJointsGoal>)))
  "Returns full string definition for message of type '<ControlJointsGoal>"
  (cl:format cl:nil "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======~%# Request part (Goal)~%float64 torso_lift~%float64 arm_1~%float64 arm_2~%float64 arm_3~%float64 arm_4~%float64 arm_5~%float64 arm_6~%float64 arm_7~%float64 gripper_position  # 0.0 for open, 1.0 for close (or adjust as needed)~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'ControlJointsGoal)))
  "Returns full string definition for message of type 'ControlJointsGoal"
  (cl:format cl:nil "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======~%# Request part (Goal)~%float64 torso_lift~%float64 arm_1~%float64 arm_2~%float64 arm_3~%float64 arm_4~%float64 arm_5~%float64 arm_6~%float64 arm_7~%float64 gripper_position  # 0.0 for open, 1.0 for close (or adjust as needed)~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <ControlJointsGoal>))
  (cl:+ 0
     8
     8
     8
     8
     8
     8
     8
     8
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <ControlJointsGoal>))
  "Converts a ROS message object to a list"
  (cl:list 'ControlJointsGoal
    (cl:cons ':torso_lift (torso_lift msg))
    (cl:cons ':arm_1 (arm_1 msg))
    (cl:cons ':arm_2 (arm_2 msg))
    (cl:cons ':arm_3 (arm_3 msg))
    (cl:cons ':arm_4 (arm_4 msg))
    (cl:cons ':arm_5 (arm_5 msg))
    (cl:cons ':arm_6 (arm_6 msg))
    (cl:cons ':arm_7 (arm_7 msg))
    (cl:cons ':gripper_position (gripper_position msg))
))
