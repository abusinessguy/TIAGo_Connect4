; Auto-generated. Do not edit!


(cl:in-package board_detection-msg)


;//! \htmlinclude BoardState.msg.html

(cl:defclass <BoardState> (roslisp-msg-protocol:ros-message)
  ((state
    :reader state
    :initarg :state
    :type (cl:vector cl:integer)
   :initform (cl:make-array 0 :element-type 'cl:integer :initial-element 0)))
)

(cl:defclass BoardState (<BoardState>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <BoardState>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'BoardState)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name board_detection-msg:<BoardState> is deprecated: use board_detection-msg:BoardState instead.")))

(cl:ensure-generic-function 'state-val :lambda-list '(m))
(cl:defmethod state-val ((m <BoardState>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader board_detection-msg:state-val is deprecated.  Use board_detection-msg:state instead.")
  (state m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <BoardState>) ostream)
  "Serializes a message object of type '<BoardState>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'state))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let* ((signed ele) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    ))
   (cl:slot-value msg 'state))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <BoardState>) istream)
  "Deserializes a message object of type '<BoardState>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'state) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'state)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:aref vals i) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296)))))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<BoardState>)))
  "Returns string type for a message object of type '<BoardState>"
  "board_detection/BoardState")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'BoardState)))
  "Returns string type for a message object of type 'BoardState"
  "board_detection/BoardState")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<BoardState>)))
  "Returns md5sum for a message object of type '<BoardState>"
  "8790a1871dbb60376786a5453cc60ea1")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'BoardState)))
  "Returns md5sum for a message object of type 'BoardState"
  "8790a1871dbb60376786a5453cc60ea1")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<BoardState>)))
  "Returns full string definition for message of type '<BoardState>"
  (cl:format cl:nil "int32[] state~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'BoardState)))
  "Returns full string definition for message of type 'BoardState"
  (cl:format cl:nil "int32[] state~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <BoardState>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'state) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <BoardState>))
  "Converts a ROS message object to a list"
  (cl:list 'BoardState
    (cl:cons ':state (state msg))
))
