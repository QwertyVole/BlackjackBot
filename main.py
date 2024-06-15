import BlackjackStrategy as bjs
import ImgRecognition as ir
import cv2 as cv
import pytesseract
player_cards = []
dealer_cards = []
custom_config = r'--oem 3 --psm 10' 
player_cards = ir.get_player_cards(ir.Get_img(0), player_cards)
print("player cards")
ir.Card_printout(player_cards)
dealer_cards = ir.get_dealer_cards(ir.Get_img(0), dealer_cards)
dealer_upcard = dealer_cards[0]
print("dealer upcard")
print(dealer_upcard)
# cv.imshow("o",ir.Get_img(0)[590 : 627 , 610 : 646])
# cv.imshow("r",ir.Get_img(0)[400 : 428 , 595 : 620])
# print(pytesseract.image_to_string(ir.Get_img(0)[412 : 428 , 604 : 620], config = custom_config))
# next_move = bjs.basic_strategy(player_cards, dealer_upcard)
# print(next_move)
# print(ir.determine_color(ir.Get_img(0)))

cv.waitKey()