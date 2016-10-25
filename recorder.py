import matplotlib
matplotlib.use('TkAgg') # <-- THIS MAKES IT FAST!
import numpy
# import scipy
import struct
import pyaudio
import threading
import pylab
import struct
import json


class SwhRecorder:
    """Simple, cross-platform class to record from the microphone."""

    def __init__(self,device):
        """minimal garb is executed when class is loaded."""
        self.RATE=44100
        self.channels=2
        self.BUFFERSIZE=2**13 #1024 is a good buffer size
        self.secToRecord=.1
        self.threadsDieNow=False
        self.newAudio=False
        self.input_device_index=device

    def setup(self):
        """initialize sound card."""
        #TODO - windows detection vs. alsa or something for linux
        #TODO - try/except for sound card selection/initiation

        self.buffersToRecord=int(self.RATE*self.secToRecord/self.BUFFERSIZE)
        if self.buffersToRecord==0: self.buffersToRecord=1
        self.samplesToRecord=int(self.BUFFERSIZE*self.buffersToRecord)
        self.chunksToRecord=int(self.samplesToRecord/self.BUFFERSIZE)
        self.secPerPoint=1.0/self.RATE

        self.p = pyaudio.PyAudio()
        # http://forum.cogsci.nl/index.php?p=/discussion/287/open-two-sound-cards/p1
        count = self.p.get_device_count()
        devices = []
        for i in range(count):
              devices.append(self.p.get_device_info_by_index(i))
              print(json.dumps(self.p.get_device_info_by_index(i), sort_keys=True,indent=4, separators=(',', ': ')))
        for i, dev in enumerate(devices):
              print "%d - %s" % (i, dev['name'])
        devinfo = self.p.get_device_info_by_index(self.input_device_index)
        #print('for')
        #for i in range(48100,100000):
        #        printi,
        #        if self.p.is_format_supported(i,  # Sample rate
        #                 input_device=devinfo['index'],
        #                 input_channels=devinfo['maxInputChannels'],
        #                 input_format=pyaudio.paInt16):
        #            print('samplerate:'+str(i))
        #print('rof')

        self.inStream = self.p.open(format=pyaudio.paInt16,
            input_device_index=self.input_device_index,
            channels=self.channels,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.BUFFERSIZE)

        #self.xsBuffer=numpy.arange(self.BUFFERSIZE)*self.secPerPoint
        #self.xs=numpy.arange(self.chunksToRecord*self.BUFFERSIZE)*self.secPerPoint
        self.audio=numpy.empty((self.chunksToRecord*self.BUFFERSIZE*self.channels),dtype=numpy.int16)

    def close(self):
        """cleanly back out and release sound card."""
        self.p.close(self.inStream)

    ### RECORDING AUDIO ###

    def getAudio(self):
        """get a single buffer size worth of audio."""
        audioString=self.inStream.read(self.BUFFERSIZE)
        return numpy.fromstring(audioString,dtype=numpy.int16)

    def record(self,forever=True):
        """record secToRecord seconds of audio."""
        while True:
            if self.threadsDieNow: break
            for i in range(self.chunksToRecord):
                self.audio[i*self.BUFFERSIZE:(i+1)*self.BUFFERSIZE*self.channels]=self.getAudio()
            self.newAudio=True
            if forever==False: break

    def continuousStart(self):
        """CALL THIS to start running forever."""
        self.t = threading.Thread(target=self.record)
        self.t.start()

    def continuousEnd(self):
        """shut down continuous recording."""
        self.threadsDieNow=True

    ### MATH ###

    def downsample(self,data,mult):
        """Given 1D data, return the binned average."""
        overhang=len(data)%mult
        if overhang: data=data[:-overhang]
        data=numpy.reshape(data,(len(data)/mult,mult))
        data=numpy.average(data,1)
        return data

    def fft(self,data=None,trimBy=10,logScale=False,divBy=100):
        if data==None:
            data=self.audio.flatten()
        left,right=numpy.split(numpy.abs(numpy.fft.fft(data)),2)
        ys=numpy.add(left,right[::-1])
        if logScale:
            ys=numpy.multiply(20,numpy.log10(ys))
        xs=numpy.arange(self.BUFFERSIZE/2,dtype=float)
        if trimBy:
            i=int((self.BUFFERSIZE/2)/trimBy)
            ys=ys[:i]
            xs=xs[:i]*self.RATE/self.BUFFERSIZE
        if divBy:
            ys=ys/float(divBy)
        return xs,ys

    ### VISUALIZATION ###

    def plotAudio(self):
        """open a matplotlib popup window showing audio data."""
        pylab.plot(self.audio.flatten())
        pylab.show()

