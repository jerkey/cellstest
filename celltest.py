from recorder import *
import matplotlib.pyplot as plt
import time

def getKey(): # return a keypress
    press = screen.getch()
    while press == -1:
        press = screen.getch()
    return press

#import curses
#screen = curses.initscr()
#if screen:
#    curses.noecho()    #could be .echo() if you want to see what you type
#    curses.curs_set(0)
#    screen.timeout(0)
#    screen.keypad(1)  #nothing works without this
#    screen.scrollok(True) # allow text to scroll screen
#    screenSize = screen.getmaxyx()
#    midX = int(screenSize[1]/2) # store the midpoint of the width of the screen

SR0 = SwhRecorder(devicename='pulse')
SR0.setup()

SR0.record(forever=False) # record one buffer's worth of audio

#print(SR0.audio.flatten()[:10])
pylab.plot(SR0.audio.flatten()) # create the plot of the data

pylab.ion() # use interactive aka Non-blocking mode for .show()

with plt.xkcd():
    plt.show() # bring up the data window (non-blocking)

#press = getKey() # wait for a keypress
time.sleep(2)

pylab.close() # close the data window

time.sleep(0.01) # wait 2 seconds
