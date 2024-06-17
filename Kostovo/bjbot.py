import cv2
import numpy as np
import pytesseract
from PIL import ImageGrab, Image
import time

# Set the tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  

# Coordinates for the first two player cards, player total, and dealer total
first_card_coords = (830, 857, 30, 26)  
second_card_coords = (862, 831, 31, 27)  
player_total_coords = (773, 891, 26, 26)  
dealer_total_coords = (483, 644, 28, 28) 

# Coordinates and color for the trigger area
trigger_coords = (1248, 542, 30, 15)
trigger_color = (79, 81, 88)  # RGB

def capture_screen():
    # Capture the screen
    screenshot = ImageGrab.grab()
    return screenshot

def extract_area(image, coords):
    x, y, w, h = coords
    area = image.crop((x, y, x + w, y + h))
    return area

def perform_ocr(image):
    text = pytesseract.image_to_string(image, config='--psm 10')
    return text.strip()

def check_trigger_color(image, coords, expected_color):
    x, y, w, h = coords
    area = np.array(image.crop((x, y, x + w, y + h)))
    area = cv2.cvtColor(area, cv2.COLOR_BGR2RGB)
    mean_color = area.mean(axis=(0, 1))
    return np.allclose(mean_color, expected_color, atol=10)  

def main():
    while True:
        # Capture the screen
        screenshot = capture_screen()

        # Check if the trigger color is present
        if check_trigger_color(screenshot, trigger_coords, trigger_color):
            # Extract first card area
            first_card_area = extract_area(screenshot, first_card_coords)
            first_card_text = perform_ocr(first_card_area)

            # Extract second card area
            second_card_area = extract_area(screenshot, second_card_coords)
            second_card_text = perform_ocr(second_card_area)

            # Extract player total area
            player_total_area = extract_area(screenshot, player_total_coords)
            player_total_text = perform_ocr(player_total_area)

            # Extract dealer total area
            dealer_total_area = extract_area(screenshot, dealer_total_coords)
            dealer_total_text = perform_ocr(dealer_total_area)

            print("First Card:", first_card_text)
            print("Second Card:", second_card_text)
            print("Player Total:", player_total_text)
            print("Dealer Total:", dealer_total_text)

        
        time.sleep(1) 

def basic_strategy(player_total, dealer_value, soft):
    """ This is a simple implementation of Blackjack's
        basic strategy. It is used to recommend actions
        for the player. """

    if 4 <= player_total <= 8:
        return 'hit'
    if player_total == 9:
        if dealer_value in [1,2,7,8,9,10]:
            return 'hit'
        return 'double'
    if player_total == 10:
        if dealer_value in [1, 10]:
            return 'hit'
        return 'double'
    if player_total == 11:
        if dealer_value == 1:
            return 'hit'
        return 'double'
    if soft:
        #we only double soft 12 because there's no splitting
        if player_total in [12, 13, 14]:
            if dealer_value in [5, 6]:
                return 'double'
            return 'hit'
        if player_total in [15, 16]:
            if dealer_value in [4, 5, 6]:
                return 'double'
            return 'hit'
        if player_total == 17:
            if dealer_value in [3, 4, 5, 6]:
                return 'double'
            return 'hit'
        if player_total == 18:
            if dealer_value in [3, 4, 5, 6]:
                return 'double'
            if dealer_value in [2, 7, 8]:
                return 'stand'
            return 'hit'
        if player_total >= 19:
            return 'stand'

    else:
        if player_total == 12:
            if dealer_value in [1, 2, 3, 7, 8, 9, 10]:
                return 'hit'
            return 'stand'
        if player_total in [13, 14, 15, 16]:
            if dealer_value in [2, 3, 4, 5, 6]:
                return 'stand'
            return 'hit'

        if player_total >= 17:
            return 'stand'

if __name__ == "__main__":
    main()
