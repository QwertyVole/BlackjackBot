import cv2 as cv
import numpy as np
import pytesseract
import time
import pyautogui

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# Define the coordinates for the areas to capture (adjust these coordinates based on your screen)
coordinates = {
    'player_firstcard': (618, 596, 646, 622),
    'player_secondcard': (645, 579, 673, 607),
    'dealer_card': (342, 393, 360, 411)
}

# Basic strategy functions
def basic_strategy(player_hand, dealer_upcard):
    player_total = calculate_hand(player_hand)
    if len(player_hand) == 2 and player_hand[0] == player_hand[1]:  # Check for pairs
        pair = player_hand[0]
        return pair_strategy(pair, dealer_upcard)
    elif 'A' in player_hand and player_total <= 21:
        return soft_hand_strategy(player_total, dealer_upcard)
    else:
        return hard_hand_strategy(player_total, dealer_upcard)

def pair_strategy(pair, dealer_upcard):
    if pair in ['A', 8]:
        return "split"
    elif pair in [10, 'K', 'Q', 'J']:
        return "stand"
    elif pair == 9:
        if dealer_upcard in [2, 3, 4, 5, 6, 8, 9]:
            return "split"
        else:
            return "stand"
    elif pair == 7:
        if dealer_upcard in [2, 3, 4, 5, 6, 7]:
            return "split"
        else:
            return "hit"
    elif pair == 6:
        if dealer_upcard in [2, 3, 4, 5, 6]:
            return "split"
        else:
            return "hit"
    elif pair == 5:
        if dealer_upcard in [2, 3, 4, 5, 6, 7, 8, 9]:
            return "double"
        else:
            return "hit"
    elif pair == 4:
        if dealer_upcard in [5, 6]:
            return "split"
        else:
            return "hit"
    elif pair in [3, 2]:
        if dealer_upcard in [2, 3, 4, 5, 6, 7]:
            return "split"
        else:
            return "hit"
    return "hit"

def soft_hand_strategy(total, dealer_upcard):
    if total == 20:
        return "stand"
    elif total == 19:
        if dealer_upcard == 6:
            return "double"
        else:
            return "stand"
    elif total == 18:
        if dealer_upcard in [2, 7, 8]:
            return "stand"
        elif dealer_upcard in [3, 4, 5, 6]:
            return "double"
        else:
            return "hit"
    elif total in [17, 16]:
        if dealer_upcard in [3, 4, 5, 6]:
            return "double"
        else:
            return "hit"
    elif total in [15, 14]:
        if dealer_upcard in [4, 5, 6]:
            return "double"
        else:
            return "hit"
    elif total in [13, 12]:
        if dealer_upcard in [5, 6]:
            return "double"
        else:
            return "hit"
    return "hit"

def hard_hand_strategy(total, dealer_upcard):
    if total >= 17:
        return "stand"
    elif total == 16:
        if dealer_upcard in [2, 3, 4, 5, 6]:
            return "stand"
        else:
            return "hit"
    elif total == 15:
        if dealer_upcard in [2, 3, 4, 5, 6]:
            return "stand"
        else:
            return "hit"
    elif total == 14:
        if dealer_upcard in [2, 3, 4, 5, 6]:
            return "stand"
        else:
            return "hit"
    elif total == 13:
        if dealer_upcard in [2, 3, 4, 5, 6]:
            return "stand"
        else:
            return "hit"
    elif total == 12:
        if dealer_upcard in [4, 5, 6]:
            return "stand"
        else:
            return "hit"
    elif total == 11:
        return "double"
    elif total == 10:
        if dealer_upcard in [2, 3, 4, 5, 6, 7, 8, 9]:
            return "double"
        else:
            return "hit"
    elif total == 9:
        if dealer_upcard in [3, 4, 5, 6]:
            return "double"
        else:
            return "hit"
    return "hit"

# Function to calculate the hand value
def calculate_hand(hand):
    total = 0
    aces = 0
    for card in hand:
        if card == 'A':
            aces += 1
            total += 11
        elif card in ['K', 'Q', 'J']:
            total += 10
        else:
            total += card
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

# Function to deal a card
def deal_card():
    return random.choice(cards)

# Function to take a screenshot and process it to extract card values
def get_card_value(area):
    screenshot = pyautogui.screenshot(region=area)
    screenshot = cv.cvtColor(np.array(screenshot), cv.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(screenshot, config=custom_config)
    # Extract card value from the text
    if 'A' in text:
        return 'A'
    elif any(face in text for face in ['K', 'Q', 'J']):
        return 10
    else:
        try:
            return int(text)
        except ValueError:
            return None

# Function to handle a single blackjack hand
def play_hand(player_hand, dealer_upcard):
    doubled_down = False
    while True:
        action = basic_strategy(player_hand, dealer_upcard)
        print(f"Player's action: {action}")
        if action == "hit":
            player_hand.append(deal_card())
            print(f"Player's hand: {player_hand}, total: {calculate_hand(player_hand)}")
            if calculate_hand(player_hand) > 21:
                print("Player busts! Dealer wins.")
                return 'bust'
        elif action == "stand":
            break
        elif action == "double" and len(player_hand) == 2:
            player_hand.append(deal_card())
            print(f"Player's hand after double: {player_hand}, total: {calculate_hand(player_hand)}")
            if calculate_hand(player_hand) > 21:
                print("Player busts after double! Dealer wins.")
                return 'bust'
            doubled_down = True
            break
        elif action == "split" and len(player_hand) == 2:
            # Handle splitting
            split_hand_1 = [player_hand[0], deal_card()]
            split_hand_2 = [player_hand[1], deal_card()]
            result_1 = play_hand(split_hand_1, dealer_upcard)
            result_2 = play_hand(split_hand_2, dealer_upcard)
            return result_1, result_2
    return calculate_hand(player_hand), doubled_down

# Main function to play the game
def play_blackjack():
    global player_wins, dealer_wins, player_money, current_bet

    # Deal initial cards
    player_hand = [deal_card(), deal_card()]
    dealer_hand = [deal_card(), deal_card()]
    
    print(f"Dealer's upcard: {dealer_hand[0]}")
    print(f"Player's hand: {player_hand}, total: {calculate_hand(player_hand)}")

    player_result = play_hand(player_hand, dealer_hand[0])
    
    if isinstance(player_result, tuple):
        # Handle the case where the hand was split
        results = player_result
    else:
        results = [player_result]

    # Dealer's turn
    while calculate_hand(dealer_hand) < 17:
        dealer_hand.append(deal_card())
    
    dealer_total = calculate_hand(dealer_hand)
    print(f"Dealer's hand: {dealer_hand}, total: {dealer_total}")

    for result in results:
        if result == 'bust':
            dealer_wins += 1
            player_money -= current_bet
            current_bet *= 2
        else:
            player_total, doubled_down = result
            if dealer_total > 21 or player_total > dealer_total:
                player_wins += 1
                player_money += current_bet * (2 if doubled_down else 1)
                current_bet = starting_bet
            elif player_total < dealer_total:
                dealer_wins += 1
                player_money -= current_bet * (2 if doubled_down else 1)
                current_bet *= 2
            else:
                print("Push!")
                if doubled_down:
                    current_bet = starting_bet

# Main function
def main():
    global player_money, current_bet

    while True:
        print(f"\nPlayer's money: ${player_money}")
        print(f"Current bet: ${current_bet}")

        play_blackjack()

        if player_money <= 0:
            print("You are out of money! Game over.")
            break

        choice = input("Press 'Q' to play again, 'W' to exit: ").strip().upper()
        if choice == 'W':
            break

    print(f"\nFinal player money: ${player_money}")
    print(f"Player wins: {player_wins}")
    print(f"Dealer wins: {dealer_wins}")

if __name__ == "__main__":
    main()

