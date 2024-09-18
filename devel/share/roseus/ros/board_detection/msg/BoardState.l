;; Auto-generated. Do not edit!


(when (boundp 'board_detection::BoardState)
  (if (not (find-package "BOARD_DETECTION"))
    (make-package "BOARD_DETECTION"))
  (shadow 'BoardState (find-package "BOARD_DETECTION")))
(unless (find-package "BOARD_DETECTION::BOARDSTATE")
  (make-package "BOARD_DETECTION::BOARDSTATE"))

(in-package "ROS")
;;//! \htmlinclude BoardState.msg.html


(defclass board_detection::BoardState
  :super ros::object
  :slots (_state ))

(defmethod board_detection::BoardState
  (:init
   (&key
    ((:state __state) (make-array 0 :initial-element 0 :element-type :integer))
    )
   (send-super :init)
   (setq _state __state)
   self)
  (:state
   (&optional __state)
   (if __state (setq _state __state)) _state)
  (:serialization-length
   ()
   (+
    ;; int32[] _state
    (* 4    (length _state)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32[] _state
     (write-long (length _state) s)
     (dotimes (i (length _state))
       (write-long (elt _state i) s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32[] _state
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _state (instantiate integer-vector n))
     (dotimes (i n)
     (setf (elt _state i) (sys::peek buf ptr- :integer)) (incf ptr- 4)
     ))
   ;;
   self)
  )

(setf (get board_detection::BoardState :md5sum-) "8790a1871dbb60376786a5453cc60ea1")
(setf (get board_detection::BoardState :datatype-) "board_detection/BoardState")
(setf (get board_detection::BoardState :definition-)
      "int32[] state

")



(provide :board_detection/BoardState "8790a1871dbb60376786a5453cc60ea1")


