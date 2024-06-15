import BlackjackStrategy as bjs
import ImgRecognition as ir
import cv2 as cv
import numpy as np
import pytesseract
player_cards = []
dealer_cards = []
custom_config = r'--oem 3 --psm 10' 
player_cards = ir.get_player_cards(ir.Get_img(0), player_cards)
print("player cards")
ir.Card_printout(player_cards)
dealer_cards = ir.get_dealer_cards(ir.Get_img(0), dealer_cards)
dealer_upcard = dealer_cards[0]
print("dealer upcard")#nefunguje dopice
print(dealer_upcard)
# next_move = bjs.basic_strategy(player_cards, dealer_upcard)
# print(next_move)
print(ir.determine_color(ir.Get_img(0)))#taky nefunguje kurva

cv.waitKey()