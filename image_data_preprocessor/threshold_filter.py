import cv
import sys

for file in sys.argv[1:]:
    im = cv.LoadImageM(file)
    cv.Threshold(im, im, 110, 0, cv.CV_THRESH_TOZERO_INV)
    #cv.FloodFill(im, (0,0), (255, 255, 255, 255))
    cv.SaveImage(file + ".jpg", im)
