import cv2 as cv
import numpy as np
import pytesseract
from PIL import Image 
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

custom_config = r'--oem 3 --psm 6' 

def determine_color(image):
    # Extract the region of interest (ROI)
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    color = hsv[555, 1202]
    
    # Define color ranges in HSV
    gray_range = (np.array([110, 20, 80]), np.array([120, 50, 100]))
    yellow_range = (np.array([20, 230, 170]), np.array([30, 255, 190]))
    red_range = (np.array([170, 200, 210]), np.array([180, 230, 240]))
    green_range = (np.array([55, 240, 190]), np.array([65, 260, 210]))
    
    # Check if the color falls within the defined ranges
    if cv.inRange(color, gray_range[0], gray_range[1]).any():
        return "gray"
    elif cv.inRange(color, yellow_range[0], yellow_range[1]).any():
        return "yellow"
    elif cv.inRange(color, red_range[0], red_range[1]).any():
        return "red"
    elif cv.inRange(color, green_range[0], green_range[1]).any():
        return "green"
    else:
        return None


def Get_img(img):
    #Todo:thresholding/masking/binarizing images
    img =cv.imread("screenshots/Screenshot (20).png")#take this out when you want to use OBS feed
    img =cv.resize(img, (1920, 1080))
    #img =cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    return img


def Card_printout(cards):
    for x in cards:
        print(x)

def To_card(string):
    cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J","Q", "K", "A"]
    output = None
    for i in range(len(string)):
        if string[i] in cards:
            output = string[i]
            break
        elif string[i] == 1:
            output == 10
            break
    return output

def get_player_cards(img, player_cards):         
    player_cards = [img[897 : 927 , 927 : 957],img[872 : 902 , 962 : 992] ]# change so it works with multiple cards
    for i in range(len(player_cards)):
        player_cards[i]=To_card(pytesseract.image_to_string(player_cards[i], config = custom_config))
    return player_cards

def get_dealer_cards(img, dealer_cards):
    dealer_cards = [cv.flip(cv.flip(img[640 : 670 , 937 : 967],0),1)]#change so it works with multiple cards
    for i in range(len(dealer_cards)):        
        dealer_cards[i] = To_card(pytesseract.image_to_string(dealer_cards[i], config = custom_config))
    return dealer_cards