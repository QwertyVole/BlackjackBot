import pyautogui as pa

def Bet(amount):
    pa.moveTo(800, 650)
    pa.leftClick()
    pa.moveTo(970, 930)
    i=0
    while amount > 0:
        pa.leftClick()
        i+=1

def Hit():
    pa.moveTo(736,444)
    pa.leftClick

def Stand():
    pa.moveTo(886, 444)
    pa.leftClick

def Double():
    pa.moveTo(1032,444)
    pa.leftClick

def Reject_Insurance():
    pa.moveTo(886, 444)
    pa.leftClick