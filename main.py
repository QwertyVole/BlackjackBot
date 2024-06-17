import utils as u

def main():
    round_in_progress = False
    while True:
        # Capture the screen
        screenshot = u.capture_screen()
        if not round_in_progress and u.check_message(screenshot, u.place_bets_coords, "PLACE YOUR BETS"):
            # Check if the start of the round is triggered by detecting "PLACE YOUR BETS"
            print("Start of a new round detected")
            u.click_position(u.betting_unit_coords)
            u.click_position(u.betting_position_coords)
            round_in_progress = True
        else:
            # Check if the round is underway by detecting "MAKE YOUR DECISION"
            if u.check_message(screenshot, u.make_decision_coords, "MAKE YOUR DECISION"):
                print("Round underway, making decisions")
                # Extract player total area
                player_total_area = u.extract_area(screenshot, u.player_total_coords)
                player_total_text = u.perform_ocr(player_total_area)
                player_total_text = u.filter_card_value(player_total_text)
                #print(f"Player total text: {player_total_text}")

                # Extract dealer total area
                dealer_total_area = u.extract_area(screenshot, u.dealer_total_coords)
                dealer_total_text = u.perform_ocr(dealer_total_area)
                dealer_total_text = u.filter_card_value(dealer_total_text)
                #print(f"Dealer total text: {dealer_total_text}")

                # Convert totals to values
                player_total_value = u.card_value(player_total_text)
                dealer_card_value = u.card_value(dealer_total_text)

                print(f"Player total value: {player_total_value}")
                print(f"Dealer card value: {dealer_card_value}")

                if player_total_value != 0 and dealer_card_value != 0 and dealer_card_value < 17:
                    action = u.decide_action(player_total_value, dealer_card_value)
                    print(f"Player Total: {player_total_value}")
                    print(f"Dealer Total: {dealer_card_value}")
                        
                    print(f"Decision: {action}")

                    # Perform the action based on the decision immediately after printing the decision
                    if action == 'Hit':
                        u.triple_click_position(u.hit_button_coords)
                    elif action == 'Stand':
                        u.triple_click_position(u.stand_button_coords)
                    elif action == 'Double':
                        u.triple_click_position(u.double_button_coords)
            elif u.check_message(screenshot, u.place_bets_coords, "PLACE YOUR BETS"):
                print("End of round")
                break    

main()                            
if __name__ == "__main__":
    main()
