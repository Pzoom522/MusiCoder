# -*- coding: UTF-8 -*-
import pydub
import pyaudio
import threading
from time import sleep
class Player:
    def __init__(self,segment): 
        self.seg=segment

        p=pyaudio.PyAudio()
        self.p=p
        self.stream=self.p.open(format=p.get_format_from_width(segment.sample_width),
                                channels=segment.channels,
                                rate=segment.frame_rate,
                                output=True)

        self.isPlay=False
        self.cur=0

        self.thrd=None
        self.lck=threading.Lock()

    def length(self):#return  length in seconds -float
        return self.seg.duration_seconds

    def position(self):  #return position in seconds -float
        return float(self.cur+1)/self.seg.frame_rate

    def setPosition(self,time):    #set a new playing time in seconds
        self.cur=int(self.seg.frame_rate*time)
 
    def play(self,block=None):  #play the sound and hold on for several seconds if block is given 
    #        self.lck.acquire()
        self.isPlay=True
        self.stream.start_stream()

        self.thrd=threading.Thread(target=self.__play__)
        self.thrd.start()
        if block!=None:
            sleep(block)
    #        self.lck.release()
    def __play__(self):
        for i in range(self.cur,int(self.seg.frame_count())):
            self.lck.acquire()

            if not self.isPlay:
                self.lck.release()
                break
            frame=self.seg.get_frame(i)
            self.cur=i
            self.stream.write(frame)

            self.lck.release()

        self.isPlay=False

    def stop(self):  # stop playing 
        self.lck.acquire()

        self.isPlay=False
        self.stream.stop_stream()

        self.lck.release()

        if self.thrd!=None:
            self.thrd.join()
    def close(self):
        self.stop()
        self.p.terminate()
if __name__ == '__main__':
    #exmaple 1:
    #-- load and play a song
    segment=pydub.AudioSegment.from_mp3("zhaolei.mp3")
    p=Player(segment)
    p.play()
    sleep(5)  # play() is an asynchronous function
    p.stop()
    p.close()

    #  exmaple 2:
    #-- reset time

    p=Player(segment)
    p.play()
    sleep(1)
    p.stop()
    p.setPosition(100)
    p.play()
    sleep(5)
    p.close()
