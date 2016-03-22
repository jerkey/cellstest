from recorder import *
SR = SwhRecorder()
SR.setup()

SR.record(forever=False)
pylab.plot(SR.audio.flatten())
pylab.show()        
