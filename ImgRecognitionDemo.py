import cv2 as cv
import numpy as numpy
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


originalImg =cv.imread("screenshots/png4.png")
img =cv.resize(originalImg, (1280, 720))
def click_event(event, x, y, flags, params): 


    # checking for right mouse clicks      
    if event==cv.EVENT_RBUTTONDOWN: 
  
        # displaying the coordinates 
        # on the Shell 
        print(x, ' ', y) 

custom_config = r'--oem 3 --psm 6' 
img = img[596:612, 618:636 ]        
cv.imshow("window",img)
cv.setMouseCallback("window", click_event)
print(pytesseract.image_to_string(img, config = custom_config))
cv. waitKey(0)