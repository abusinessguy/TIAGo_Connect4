
(cl:in-package :asdf)

(defsystem "board_detection-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "BoardState" :depends-on ("_package_BoardState"))
    (:file "_package_BoardState" :depends-on ("_package"))
  ))