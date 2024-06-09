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
player_first_card = pytesseract.image_to_string(img[596:622, 618:646], config = custom_config)
#player_first_card = player_first_card[1]
player_second_card = pytesseract.image_to_string(img[579:607 , 645:673], config = custom_config)
#player_second_card = player_second_card[1]
dealer_first_card = pytesseract.image_to_string(img[393 : 411 , 342 : 360], config = custom_config)
#dealer_first_card = dealer_first_card[1]
print("player1",player_first_card, "player2", player_second_card, "dealer1", dealer_first_card )
cv. waitKey(0)