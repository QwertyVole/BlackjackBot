import cv2 as cv
import numpy as numpy
import pytesseract
#from BlackjackStrategy import #missingClass
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

custom_config = r'--oem 3 --psm 6' 
splitBool = False
doubleBool = False

cap = cv.VideoCapture(0)
#if 0 doesnt work, increment by one and try again
while True:
    isTrue, img = cap.read()
    cv.imshow("Video", img)
    if splitBool == True:
      #get coordinates for split cards
      print("všechno je v piči nevim co dělat")
    if doubleBool == True:
        print("všechno je v piči nevim co dělat")
    player_first_card = pytesseract.image_to_string(img[596:612, 618:636 ], config = custom_config)
    player_first_card = player_first_card[0]
    player_second_card = pytesseract.image_to_string(img[576:594, 643:661 ], config = custom_config)
    player_second_card = player_second_card[0]
    dealer_first_card = pytesseract.image_to_string(img[596:612, 618:636 ], config = custom_config)
    dealer_first_card = dealer_first_card[0]
    print("player1",player_first_card, "player2", player_second_card, "dealer1", dealer_first_card )
#press d to destroy all windows and stop the program
    if cv. waitKey(20) & 0xFF==ord("d"):
        break
cap.release()
cv.destroyAllWindows()