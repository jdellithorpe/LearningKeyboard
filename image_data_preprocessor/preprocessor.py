import cv
import sys

for file in sys.argv[1:]:
    im = cv.LoadImageM(file)
    cropped = cv.GetSubRect(im, (205, 145, 225, 95))
    cv.ConvertScale(cropped,cropped,-1,255)
    cv.Threshold(cropped, cropped, 145, 0, cv.CV_THRESH_TOZERO)
    cv.SaveImage(file, cropped)
