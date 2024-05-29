import cv2 as cv
import numpy as numpy
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

custom_config = r'--oem 3 --psm 6'
originalImg =cv.imread("screenshots/png8.png")
img =cv.resize(originalImg, (1280, 720))
player_firstcard = img[596:622, 618:646]
player_secondcard = img[579 : 607 , 645 : 673]
dealer_card = img[393 : 411 , 342 : 360]
cv.imshow("window",img)
cv.imshow("player first card", player_firstcard)
cv.imshow("player second card", player_secondcard)
cv.imshow("dealer card", dealer_card)

def click_event(event, x, y, flags, params): 
    # checking for right mouse clicks      
    if event==cv.EVENT_RBUTTONDOWN: 
        # displaying the coordinates 
        print(y,":",y+28,",",x,":",x+28) 

cv.setMouseCallback("window", click_event)
print("Players first card:", pytesseract.image_to_string(player_firstcard, config = custom_config))
print("Players second card:", pytesseract.image_to_string(player_secondcard, config = custom_config))
print("Dealer first card:", pytesseract.image_to_string(dealer_card, config = custom_config))
cv. waitKey(0)