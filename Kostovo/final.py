import cv2
import numpy as np
import pytesseract
from PIL import ImageGrab, Image
import time

# Set the tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update with your path

# Coordinates for player total and dealer total
player_total_coords = (773, 891, 26, 26)
dealer_total_coords = (479, 645, 34, 28)

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

def check_trigger_color(image, coords, expected_color):
    x, y, w, h = coords
    area = np.array(image.crop((x, y, x + w, y + h)))
    area = cv2.cvtColor(area, cv2.COLOR_BGR2RGB)
    mean_color = area.mean(axis=(0, 1))
    return np.allclose(mean_color, expected_color, atol=10)  # Tolerance can be adjusted

def card_value(card):
    card = card.upper().strip()
    if card in ['J', 'Q', 'K']:
        return 10
    elif card == 'A':
        return 11  # Initially treat Aces as 11
    else:
        try:
            return int(card)
        except ValueError:
            print(f"Invalid card value detected: {card}")
            return None

def filter_card_value(card_text):
    # Filter out non-numeric and unexpected characters
    card_text = card_text.replace(' ', '').replace('\n', '').replace('\r', '')
    filtered_text = ''.join(filter(str.isalnum, card_text))
    return filtered_text

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

def main():
    player_total_stable = None
    dealer_total_stable = None
    player_total_count = 0
    dealer_total_count = 0
    threshold = 3  # Number of consistent readings needed to confirm

    while True:
        # Capture the screen
        screenshot = capture_screen()

        # Check if the trigger color is present
        if check_trigger_color(screenshot, trigger_coords, trigger_color):
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

            if player_total_value is not None:
                if player_total_stable == player_total_value:
                    player_total_count += 1
                else:
                    player_total_stable = player_total_value
                    player_total_count = 1

            if dealer_card_value is not None:
                if dealer_total_stable == dealer_card_value:
                    dealer_total_count += 1
                else:
                    dealer_total_stable = dealer_card_value
                    dealer_total_count = 1

            if player_total_count >= threshold and dealer_total_count >= threshold:
                player_total_count = 0  # Reset count after confirmation
                dealer_total_count = 0  # Reset count after confirmation
                action = decide_action(player_total_stable, dealer_total_stable)
                print(f"Player Total: {player_total_stable}")
                print(f"Dealer Total: {dealer_total_stable}")
                print(f"Decision: {action}")

        # To avoid overwhelming the system, add a delay
        time.sleep(1)  # Adjust as needed

if __name__ == "__main__":
    main()
