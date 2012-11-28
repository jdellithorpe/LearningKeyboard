import cv
import sys

for file in sys.argv[1:]:
    im = cv.LoadImageM(file)
    cropped = cv.GetSubRect(im, (205, 145, 225, 95))
    cv.SaveImage(file, cropped)
