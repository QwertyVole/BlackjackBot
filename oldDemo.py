import cv2 as cv
import numpy as numpy
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

custom_config = r'--oem 3 --psm 6'

originalImg =cv.imread("screenshots/Screenshot (24).png")
img =cv.resize(originalImg, (1920, 1080))
cv.imshow("window",img)
cv.imshow("img",cv.resize(img[665 : 686 , 546 : 563], (30,30)))
print(pytesseract.image_to_string(cv.resize(img[665 : 686 , 546 : 563], (32, 32)), config = custom_config))

def click_event(event, x, y, flags, params): 
    # checking for right mouse clicks      
    if event==cv.EVENT_RBUTTONDOWN: 
        # displaying the coordinates 
        #print(y-3,":",y+27,",",x-3,":",x+27) 
        print(f"y:{y} x:{x}")
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        color = hsv[555, 1202]
        print(f"H{color[0]} S{color[1]} V{color[2]}")

cv.setMouseCallback("window", click_event)
cv. waitKey(0)