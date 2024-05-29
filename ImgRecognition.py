import cv2 as cv
import numpy as numpy
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

custom_config = r'--oem 3 --psm 6' 


cap = cv.VideoCapture(0)
#if 0 doesnt work, increment by one and try again
while True:
    isTrue, img = cap.read()
    cv.imshow("Video", img)        
    # print("Players first card:", pytesseract.image_to_string(img[596:612, 618:636 ], config = custom_config))
    # print("Players second card:", pytesseract.image_to_string(img[576:594, 643:661 ], config = custom_config))
    # print("Dealer first card:", pytesseract.image_to_string(img[596:612, 618:636 ], config = custom_config))
#press d to destroy all windows and stop the program
    if cv. waitKey(20) & 0xFF==ord("d"):
        break
cap.release()
cv.destroyAllWindows()