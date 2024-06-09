import cv2 as cv
import numpy
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

custom_config = r'--oem 3 --psm 6' 

def Get_img(img):
        img =cv.imread("screenshots/png5.png")#take this out when you want to use OBS feed
        img =cv.resize(img, (1280, 720))
        cv.imshow("window",img)
        return img

#if 0 doesnt work, increment by one and try again
def Card_printout(cards):
    for x in cards:
        print(x)

def To_card(string):
    return string[0]
    

def get_player_cards(img, player_cards):         
    player_cards = [img[596:622, 618:646], img[575:607, 643 : 673]]# change so it works with multiple cards
    for i in range(len(player_cards)):
        player_cards[i]=To_card(pytesseract.image_to_string(player_cards[i], config = custom_config))
    return player_cards

def get_dealer_cards(img, dealer_cards):
    dealer_cards = [img[393 : 411 , 342 : 360]]#change so it works with multiple cards
    for i in range(len(dealer_cards)):        
        dealer_cards[i] = To_card(pytesseract.image_to_string(dealer_cards[i], config = custom_config))
    return dealer_cards