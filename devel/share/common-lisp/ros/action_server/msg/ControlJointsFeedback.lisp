; Auto-generated. Do not edit!


(cl:in-package action_server-msg)


;//! \htmlinclude ControlJointsFeedback.msg.html

(cl:defclass <ControlJointsFeedback> (roslisp-msg-protocol:ros-message)
  ()
)

(cl:defclass ControlJointsFeedback (<ControlJointsFeedback>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <ControlJointsFeedback>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'ControlJointsFeedback)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name action_server-msg:<ControlJointsFeedback> is deprecated: use action_server-msg:ControlJointsFeedback instead.")))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <ControlJointsFeedback>) ostream)
  "Serializes a message object of type '<ControlJointsFeedback>"
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <ControlJointsFeedback>) istream)
  "Deserializes a message object of type '<ControlJointsFeedback>"
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<ControlJointsFeedback>)))
  "Returns string type for a message object of type '<ControlJointsFeedback>"
  "action_server/ControlJointsFeedback")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ControlJointsFeedback)))
  "Returns string type for a message object of type 'ControlJointsFeedback"
  "action_server/ControlJointsFeedback")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<ControlJointsFeedback>)))
  "Returns md5sum for a message object of type '<ControlJointsFeedback>"
  "d41d8cd98f00b204e9800998ecf8427e")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'ControlJointsFeedback)))
  "Returns md5sum for a message object of type 'ControlJointsFeedback"
  "d41d8cd98f00b204e9800998ecf8427e")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<ControlJointsFeedback>)))
  "Returns full string definition for message of type '<ControlJointsFeedback>"
  (cl:format cl:nil "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======~%# Feedback (optional)~%# You can include feedback fields here if needed~%~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'ControlJointsFeedback)))
  "Returns full string definition for message of type 'ControlJointsFeedback"
  (cl:format cl:nil "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======~%# Feedback (optional)~%# You can include feedback fields here if needed~%~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <ControlJointsFeedback>))
  (cl:+ 0
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <ControlJointsFeedback>))
  "Converts a ROS message object to a list"
  (cl:list 'ControlJointsFeedback
))
