import cv2 as cv

img = cv.imread("Pictures/OldVan.jpg")
cv.imshow("Cat", img)
cv.waitKey(0)