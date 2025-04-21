(defun World_Template ()
  (let ((p (make-instance 'Part)))
    (setf (slot-value 'handler p) #'World_handler)
    p))

(defun World_handler (eh mev)
  (send eh "" "World"))
