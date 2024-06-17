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
    if len(card)>=3:
        return int(card[:-2])
    else:
        if card != "":
            return int(card)
        else: return ""


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

def main():
    round_in_progress = False
    while True:
        # Capture the screen
        screenshot = capture_screen()
        
        if not round_in_progress:
            # Check if the start of the round is triggered by detecting "PLACE YOUR BETS"
            if check_message(screenshot, place_bets_coords, "PLACE YOUR BETS"):
                print("Start of a new round detected")
                click_position(betting_unit_coords)
                click_position(betting_position_coords)
                round_in_progress = True
        else:
            # Check if the round is underway by detecting "MAKE YOUR DECISION"
            if check_message(screenshot, make_decision_coords, "MAKE YOUR DECISION"):
                print("Round underway, making decisions")
                while True:
                    screenshot = capture_screen()
                    # Extract player total area
                    player_total_area = extract_area(screenshot, player_total_coords)
                    player_total_text = perform_ocr(player_total_area)
                    player_total_text = filter_card_value(player_total_text)
                    print(f"Player total text: {player_total_text}")

                    # Extract dealer total area
                    dealer_total_area = extract_area(screenshot, dealer_total_coords)
                    dealer_total_text = perform_ocr(dealer_total_area)
                    dealer_total_text = filter_card_value(dealer_total_text)
                    print(f"Dealer total text: {dealer_total_text}")

                    # Convert totals to values
                    player_total_value = card_value(player_total_text)
                    dealer_card_value = card_value(dealer_total_text)

                    print(f"Player total value: {player_total_value}")
                    print(f"Dealer card value: {dealer_card_value}")

                    if player_total_value is not None and dealer_card_value is not None:
                        action = decide_action(player_total_value, dealer_card_value)
                        print(f"Player Total: {player_total_value}")
                        print(f"Dealer Total: {dealer_card_value}")
                        print(f"Decision: {action}")

                        # Perform the action based on the decision immediately after printing the decision
                        if action == 'Hit':
                            triple_click_position(hit_button_coords)
                        elif action == 'Stand':
                            triple_click_position(stand_button_coords)
                        elif action == 'Double':
                            triple_click_position(double_button_coords)

                        # After making a decision, re-evaluate the totals
                        #Todo wait till dealer shows all cards
                        while True:
                            screenshot = capture_screen()
                            player_total_area = extract_area(screenshot, player_total_coords)
                            player_total_text = perform_ocr(player_total_area)
                            player_total_text = filter_card_value(player_total_text)
                            dealer_total_area = extract_area(screenshot, dealer_total_coords)
                            dealer_total_text = perform_ocr(dealer_total_area)
                            dealer_total_text = filter_card_value(dealer_total_text)

                            player_total_value = card_value(player_total_text)
                            dealer_card_value= card_value(dealer_total_text)
                            
                            
                            if dealer_card_value >= 17:
                                if player_total_value is None or dealer_card_value is None:
                                    continue

                                outcome = check_outcome(player_total_value, dealer_card_value)
                                print(f"Re-evaluated Outcome: {outcome}")

                                if outcome in ['Win', 'Loss', 'Push']:
                                    print("Round over, resetting for next round.")
                                    round_in_progress = False
                                    break
                                else:
                                    # Recalculate the action based on the new totals
                                    action = decide_action(player_total_value, dealer_card_value)
                                    print(f"New Decision: {action}")

                                    if action == 'Hit':
                                        triple_click_position(hit_button_coords)
                                    elif action == 'Stand':
                                        triple_click_position(stand_button_coords)
                                    elif action == 'Double':
                                        triple_click_position(double_button_coords)
main()
if __name__ == "__main__":
    main()
