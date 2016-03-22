from recorder import *
import time
SR = SwhRecorder()
SR.setup()

SR.record(forever=False) # record one buffer's worth of audio

pylab.plot(SR.audio.flatten()) # create the plot of the data

pylab.ion() # use interactive aka Non-blocking mode for .show()

pylab.show() # bring up the data window (non-blocking)

time.sleep(2) # wait 2 seconds

pylab.close() # close the data window

time.sleep(2) # wait 2 seconds
