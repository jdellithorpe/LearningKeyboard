#!/usr/bin/env python
import freenect
import cv
import frame_convert
import time

#cv.NamedWindow('Depth')
#cv.NamedWindow('Video')
print('Press ESC in window to stop')


def get_depth():
    time_string = "%1.6f" % time.time()
    cv.SaveImage(time_string + ".pgm", frame_convert.pretty_depth_cv(freenect.sync_get_depth()[0]))


def get_video():
    return frame_convert.video_cv(freenect.sync_get_video()[0])


while 1:
    get_depth()
    #cv.ShowImage('Depth', get_depth())
    #cv.ShowImage('Video', get_video())
    if cv.WaitKey(10) == 27:
        break
