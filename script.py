import cv2 as cv

#get rtmp stream to work

myrtmp_addr = "rtmp://myip:1935/myapp/mystream"
cap = cv.VideoCapture(myrtmp_addr)
frame,err = cap.read()