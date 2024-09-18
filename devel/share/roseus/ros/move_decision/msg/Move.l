;; Auto-generated. Do not edit!


(when (boundp 'move_decision::Move)
  (if (not (find-package "MOVE_DECISION"))
    (make-package "MOVE_DECISION"))
  (shadow 'Move (find-package "MOVE_DECISION")))
(unless (find-package "MOVE_DECISION::MOVE")
  (make-package "MOVE_DECISION::MOVE"))

(in-package "ROS")
;;//! \htmlinclude Move.msg.html


(defclass move_decision::Move
  :super ros::object
  :slots (_column _TurnCounter _winner _player ))

(defmethod move_decision::Move
  (:init
   (&key
    ((:column __column) 0)
    ((:TurnCounter __TurnCounter) 0)
    ((:winner __winner) 0)
    ((:player __player) 0)
    )
   (send-super :init)
   (setq _column (round __column))
   (setq _TurnCounter (round __TurnCounter))
   (setq _winner (round __winner))
   (setq _player (round __player))
   self)
  (:column
   (&optional __column)
   (if __column (setq _column __column)) _column)
  (:TurnCounter
   (&optional __TurnCounter)
   (if __TurnCounter (setq _TurnCounter __TurnCounter)) _TurnCounter)
  (:winner
   (&optional __winner)
   (if __winner (setq _winner __winner)) _winner)
  (:player
   (&optional __player)
   (if __player (setq _player __player)) _player)
  (:serialization-length
   ()
   (+
    ;; int32 _column
    4
    ;; int32 _TurnCounter
    4
    ;; int32 _winner
    4
    ;; int32 _player
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _column
       (write-long _column s)
     ;; int32 _TurnCounter
       (write-long _TurnCounter s)
     ;; int32 _winner
       (write-long _winner s)
     ;; int32 _player
       (write-long _player s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _column
     (setq _column (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _TurnCounter
     (setq _TurnCounter (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _winner
     (setq _winner (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _player
     (setq _player (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get move_decision::Move :md5sum-) "540f6692ebd5dddcb06a7ba689a29a28")
(setf (get move_decision::Move :datatype-) "move_decision/Move")
(setf (get move_decision::Move :definition-)
      "int32 column
int32 TurnCounter
int32 winner
int32 player

")



(provide :move_decision/Move "540f6692ebd5dddcb06a7ba689a29a28")


