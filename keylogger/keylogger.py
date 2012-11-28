#!/usr/local/bin/Python
"""Displays the keysym for each KeyPress event as you type."""
import Tkinter
import commands
import sys
import time

root = Tkinter.Tk()
root.title("Keysym Logger")
    
def reportEvent(event):
    #depth_frame = commands.getoutput("ls " + sys.argv[1] + "*.pgm | tail -n 1 | xargs -n1 basename")
    print '%s,%s,%d,%f' % (event.keysym, event.keysym_num, event.time, time.time())
    
text  = Tkinter.Text(root, width=20, height=5, highlightthickness=2)
    
text.bind('<KeyPress>', reportEvent)
    
text.pack(expand=1, fill="both")
text.focus_set()
root.mainloop()
