import random

# Define the card values
cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'A']
player_money = 1000  # Initial budget
starting_bet = 10  # Initial bet
current_bet = starting_bet  # Current bet amount

# Basic strategy based on the provided chart
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
    if pair == 'A' or pair == 8:
        return "split"
    elif pair == 10:
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
    elif pair == 3 or pair == 2:
        if dealer_upcard in [2, 3, 4, 5, 6, 7]:
            return "split"
        else:
            return "hit"
    return "hit"

def soft_hand_strategy(total, dealer_upcard):
    if total == 20:
        return "stand"
    elif total == 19:
        if dealer_upcard in [6]:
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
    elif total == 17 or total == 16:
        if dealer_upcard in [3, 4, 5, 6]:
            return "double"
        else:
            return "hit"
    elif total == 15 or total == 14:
        if dealer_upcard in [4, 5, 6]:
            return "double"
        else:
            return "hit"
    elif total == 13 or total == 12:
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
        else:
            total += card
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

# Deal cards
def deal_card():
    return random.choice(cards)

# Initialize game
player_wins = 0
dealer_wins = 0

def play_blackjack():
    global player_wins, dealer_wins, player_money, current_bet
    
    # Deal initial cards
    player_hand = [deal_card(), deal_card()]
    dealer_hand = [deal_card(), deal_card()]
    
    print(f"Dealer's upcard: {dealer_hand[0]}")
    print(f"Player's hand: {player_hand}, total: {calculate_hand(player_hand)}")
    
    doubled_down = False
    
    # Player's turn
    while True:
        action = basic_strategy(player_hand, dealer_hand[0])
        
        print(f"Player's action: {action}")
        
        if action == "hit":
            player_hand.append(deal_card())
            print(f"Player's hand: {player_hand}, total: {calculate_hand(player_hand)}")
            if calculate_hand(player_hand) > 21:
                print("Player busts! Dealer wins.")
                dealer_wins += 1
                player_money -= current_bet  # Deduct bet amount
                current_bet *= 2  # Double the bet for the next round
                return
        elif action == "stand":
            break
        elif action == "double" and len(player_hand) == 2:
            player_hand.append(deal_card())
            print(f"Player's hand after double: {player_hand}, total: {calculate_hand(player_hand)}")
            if calculate_hand(player_hand) > 21:
                print("Player busts after double! Dealer wins.")
                dealer_wins += 1
                player_money -= current_bet * 2  # Deduct double bet amount
                current_bet *= 2  # Double the bet for the next round
                return
            doubled_down = True
            break
        elif action == "split":
            print("Player splits (not fully implemented in this script).")
            # For simplicity, we won't handle splitting in this script
            break
    
    # Dealer's turn
    while calculate_hand(dealer_hand) < 17:
        dealer_hand.append(deal_card())
    
    player_total = calculate_hand(player_hand)
    dealer_total = calculate_hand(dealer_hand)
    
    print(f"Dealer's hand: {dealer_hand}, total: {dealer_total}")
    
    if dealer_total > 21 or player_total > dealer_total:
        print("Player wins!")
        player_wins += 1
        player_money += current_bet * (2 if doubled_down else 1)  # Add bet amount
        current_bet = starting_bet  # Reset the bet to the starting amount
    elif player_total < dealer_total:
        print("Dealer wins!")
        dealer_wins += 1
        player_money -= current_bet * (2 if doubled_down else 1)  # Deduct bet amount
        current_bet *= 2  # Double the bet for the next round
    else:
        print("Push!")
        if doubled_down:
            current_bet = starting_bet  # Reset the bet to the starting amount
        # No change in player_money for a push

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
