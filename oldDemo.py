import cv2 as cv
import numpy as numpy
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

custom_config = r'--oem 3 --psm 6'
originalImg =cv.imread("screenshots/Screenshot (20).png")
img =cv.resize(originalImg, (1920, 1080))
cv.imshow("window",img[612 : 642 , 903 : 933])


def click_event(event, x, y, flags, params): 
    # checking for right mouse clicks      
    if event==cv.EVENT_RBUTTONDOWN: 
        # displaying the coordinates 
        print(y-3,":",y+27,",",x-3,":",x+27) 

cv.setMouseCallback("window", click_event)
cv. waitKey(0)