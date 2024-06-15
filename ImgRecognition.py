import cv2 as cv
import numpy
import pytesseract
from PIL import Image 
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

custom_config = r'--oem 3 --psm 6' 
def get_color_name(hue, saturation, value):
    if 0 <= hue <= 10 or 160 <= hue <= 180:
        return 'red'
    elif 20 <= hue <= 30:
        return 'yellow'
    elif 35 <= hue <= 85:
        return 'green'
    else:
        return 'unknown'
    
def determine_color(image):
    # Extract the region of interest (ROI)
    roi = image[357 : 385 , 735 : 763]

    # Convert the ROI to the HSV color space
    hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)

    # Calculate the average color of the ROI
    avg_hue = numpy.mean(hsv_roi[:, :, 0])
    avg_saturation = numpy.mean(hsv_roi[:, :, 1])
    avg_value = numpy.mean(hsv_roi[:, :, 2])

    # Determine the color based on average HSV values
    color = get_color_name(avg_hue, avg_saturation, avg_value)
    return color

def Get_img(img):
        img =cv.imread("screenshots/Screenshot (20).png")#take this out when you want to use OBS feed
        img =cv.resize(img, (1920, 1080))
        img =cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        cv.imshow("window",img)
        return img

#if 0 doesnt work, increment by one and try again
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
        else:
            raise Exception(string)
    return output

def get_player_cards(img, player_cards):         
    player_cards = [img[897 : 927 , 927 : 957],img[872 : 902 , 962 : 992] ]# change so it works with multiple cards
    for i in range(len(player_cards)):
        player_cards[i]=To_card(pytesseract.image_to_string(player_cards[i], config = custom_config))
    return player_cards

def get_dealer_cards(img, dealer_cards):
    dealer_cards = [img[612 : 642 , 903 : 933]]#change so it works with multiple cards
    for i in range(len(dealer_cards)):        
        dealer_cards[i] = To_card(pytesseract.image_to_string(dealer_cards[i], config = custom_config))
    return dealer_cards