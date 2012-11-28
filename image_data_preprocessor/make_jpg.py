import cv
import sys

for file in sys.argv[1:]:
    im = cv.LoadImageM(file)
    cv.SaveImage(file + ".jpg", im)
