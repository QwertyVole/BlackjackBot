import cv2 as cv
import numpy as numpy

cap = cv.VideoCapture(0)#if 0 doesnt work, increment by one and try again
while True:
    isTrue, frame = cap.read()
    cv.imshow("frame", frame)

#press d to destroy all windows and stop the program
    if cv. waitKey(20) & 0xFF==ord("d"):
        break
cap.release()
cv.destroyAllWindows()