import pytesseract
from PIL import ImageGrab, Image
import pyautogui
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'  

# Coordinates for player total, dealer total, and text areas
# (x, y, w, h)
player_total_coords = (860, 930, 30, 30)
dealer_total_coords = (540, 660 , 30, 30)
place_bets_coords = (820, 530, 350, 37)
make_decision_coords = (703, 530, 600, 38)
outcome_coords = (840, 880, 80, 30)  # Coordinates for outcome text area

# Coordinates for clicking on screen elements
betting_unit_coords = (800, 650)
betting_position_coords = (970, 930)
hit_button_coords = (890,440)
stand_button_coords = (1030, 440)
double_button_coords = (736,444)

def capture_screen():
    # Capture the screen
    screenshot = ImageGrab.grab()
    cv2.resize(np.array(screenshot), (1080 ,1920))
    return screenshot

def extract_area(image, coords):
    x, y, w, h = coords
    area = image.crop((x, y, x + w, y + h))
    return area

def preprocess_image(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    # Apply thresholding to get a binary image
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    return Image.fromarray(binary)

def perform_ocr(image):
    processed_image = preprocess_image(image)
    text = pytesseract.image_to_string(processed_image, config='--psm 10')
    return text.strip()

def check_message(image, coords, expected_text):
    
    area = extract_area(image, coords)
    text = perform_ocr(area) 
    print(f"Recognized text: {text}")  # Debugging line

        
    return expected_text.lower() in text.lower()

def card_value(card):
    card = card.upper().strip()
    if card == "A":
        return 4
    if card == "a":
        return 9
    if len(card)>=3:
        return int(card[:-2])
    try:
        return int(card)
    except ValueError:
        return 0

    

def filter_card_value(card_text):
    # Filter out unexpected characters
    card_text = card_text.replace(' ', '').replace('\n', '').replace('\r', '')
    filtered_text = ''.join(filter(str.isalnum, card_text))
    return filtered_text
#STRAT
def decide_action(player_total, dealer_card):
    if player_total <= 8:
        return 'Hit'
    elif player_total == 9:
        if dealer_card in [3, 4, 5, 6]:
            return 'Double'
        else:
            return 'Hit'
    elif player_total == 10:
        if dealer_card in [10, 11]:
            return 'Hit'
        else:
            return 'Double'
    elif player_total == 11:
        return 'Double'
    elif player_total == 12:
        if dealer_card in [4, 5, 6]:
            return 'Stand'
        else:
            return 'Hit'
    elif player_total in [13, 14, 15, 16]:
        if dealer_card in [2, 3, 4, 5, 6]:
            return 'Stand'
        else:
            return 'Hit'
    elif player_total >= 17:
        return 'Stand'
    return 'Invalid'
#triple click to overcome problems with bugged click
def triple_click_position(coords):
    print(f"Triple clicking at position: {coords}")
    for _ in range(3):
        pyautogui.click(coords[0], coords[1])

def click_position(coords):
    print(f"Clicking at position: {coords}")
    pyautogui.click(coords[0], coords[1])

def check_outcome_text():
    screenshot = capture_screen()
    outcome_area = extract_area(screenshot, outcome_coords)
    processed_image = preprocess_image(outcome_area)
    outcome_text = pytesseract.image_to_string(processed_image, config='--psm 10').strip().lower()
    
    if "bust" in outcome_text:
        return "bust"
    elif "lose" in outcome_text:
        return "lose"
    elif "win" in outcome_text:
        return "win"
    else:
        return "unknown"
#round outcome check
def check_outcome(player_total, dealer_total):
    outcome_text = check_outcome_text()
    if outcome_text == "bust":
        return 'Loss'
    elif outcome_text == "lose":
        return 'Loss'
    elif outcome_text == "win":
        return 'Win'

    if player_total is None or dealer_total is None:
        return None
    if dealer_total > 21:
        return 'Win'
    if player_total > 21:
        return 'Loss'
    if player_total > dealer_total:
        return 'Win'
    if player_total < dealer_total:
        return 'Loss'
    return 'Push'