import utils as u

def main():
    round_in_progress = False
    while True:
        # Capture the screen
        screenshot = u.capture_screen()
        
        if not round_in_progress:
            # Check if the start of the round is triggered by detecting "PLACE YOUR BETS"
            if u.check_message(screenshot, u.place_bets_coords, "PLACE YOUR BETS"):
                print("Start of a new round detected")
                u.click_position(u.betting_unit_coords)
                u.click_position(u.betting_position_coords)
                round_in_progress = True
        else:
            # Check if the round is underway by detecting "MAKE YOUR DECISION"
            if u.check_message(screenshot, u.make_decision_coords, "MAKE YOUR DECISION"):
                print("Round underway, making decisions")
                while True:
                    screenshot = u.capture_screen()
                    # Extract player total area
                    player_total_area = u.extract_area(screenshot, u.player_total_coords)
                    player_total_text = u.perform_ocr(player_total_area)
                    player_total_text = u.filter_card_value(player_total_text)
                    print(f"Player total text: {player_total_text}")

                    # Extract dealer total area
                    dealer_total_area = u.extract_area(screenshot, u.dealer_total_coords)
                    dealer_total_text = u.perform_ocr(dealer_total_area)
                    dealer_total_text = u.filter_card_value(dealer_total_text)
                    print(f"Dealer total text: {dealer_total_text}")

                    # Convert totals to values
                    player_total_value = u.card_value(player_total_text)
                    dealer_card_value = u.card_value(dealer_total_text)

                    print(f"Player total value: {player_total_value}")
                    print(f"Dealer card value: {dealer_card_value}")

                    if player_total_value is not None and dealer_card_value is not None:
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

                        # After making a decision, re-evaluate the totals
                        #Todo wait till dealer shows all cards
                        while True:
                            screenshot = u.capture_screen()
                            player_total_area = u.extract_area(screenshot, u.player_total_coords)
                            player_total_text = u.perform_ocr(player_total_area)
                            player_total_text = u.filter_card_value(player_total_text)
                            dealer_total_area = u.extract_area(screenshot, u.dealer_total_coords)
                            dealer_total_text = u.perform_ocr(dealer_total_area)
                            dealer_total_text = u.filter_card_value(dealer_total_text)

                            player_total_value = u.card_value(player_total_text)
                            dealer_card_value= u.card_value(dealer_total_text)
                            
                            
                            if dealer_card_value >= 17:
                                if player_total_value is None or dealer_card_value is None:
                                    continue

                                outcome = u.check_outcome(player_total_value, dealer_card_value)
                                print(f"Re-evaluated Outcome: {outcome}")

                                if outcome in ['Win', 'Loss', 'Push']:
                                    print("Round over, resetting for next round.")
                                    round_in_progress = False
                                    break
                                else:
                                    # Recalculate the action based on the new totals
                                    action = u.decide_action(player_total_value, dealer_card_value)
                                    print(f"New Decision: {action}")

                                    if action == 'Hit':
                                        u.triple_click_position(u.hit_button_coords)
                                    elif action == 'Stand':
                                        u.triple_click_position(u.stand_button_coords)
                                    elif action == 'Double':
                                        u.triple_click_position(u.double_button_coords)
main()
if __name__ == "__main__":
    main()
