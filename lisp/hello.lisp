(defun Hello_Template ()
  (let ((p (make-instance 'Part)))
    (setf (slot-value 'handler p) #'Hello_handler)
    p))

(defun Hello_handler (eh mev)
  (send eh "" "Hello"))
