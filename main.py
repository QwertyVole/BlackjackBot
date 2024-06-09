import BlackjackStrategy as bjs
import ImgRecognition as ir
import cv2 as cv
player_cards = []
dealer_cards = []
player_cards = ir.get_player_cards(ir.Get_img(0), player_cards)
print("player cards")
ir.Card_printout(player_cards)
dealer_cards = ir.get_dealer_cards(ir.Get_img(0), dealer_cards)
dealer_upcard = dealer_cards[0]
print(dealer_upcard)
next_move = bjs.basic_strategy(player_cards, dealer_upcard)
print(next_move)
cv.waitKey()