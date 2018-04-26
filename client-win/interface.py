# -*- coding:utf-8 -*-
import os
import random
#import player
from pydub import AudioSegment
AudioSegment.converter='.\\ffmpeg.exe'

def loadSound(filepath):
    # Load sound which has format mp3 and wav.
    # Return AudioSegment object.
    (dir_, name_) = os.path.split(filepath)
    (name, ext) = os.path.splitext(name_)
    if ext not in ('.wav', '.mp3'):
        return None
    sound = AudioSegment.from_file(filepath, ext[1:])
    return sound


def cutSound(sound, start, end):
    # Cut the sound with a time window.(Use seconds as paramter)
    return sound[int(start * 1000):int(end * 1000)]


def exportSound(sound, filepath):
    sound.export(filepath)

def balanceSound(originalPath):

    #random a non-repeating file name
    ext = '.mp3'
    seed = '1234567890qazwsxedcrfvtgbyhnujmikolp_'
    name = ''.join(random.choice(seed)for _ in range(8))
    newPath = 'Temp/'+name+ext
    while os.path.exists(newPath):
        name = ''.join(random.choice(seed)for _ in range(8))
        newPath = 'Temp/'+name+ext
        
    #filter the original song using ffmpeg, and output to Temp file
    convert='.\\ffmpeg -loglevel panic -i \"'+originalPath+'\" -filter:a loudnorm '+newPath
    print "conv",convert
    os.popen(convert)
    print('balanced: '+newPath)
    return newPath

def test():
   
    filepath=raw_input("Please enter the filepath(.wav,.mp3):")
    start=int(input("The start sec:"))
    end=int(input("The start sec:"))
    
    sound = loadSound(filepath)
    if sound==None:
        print "Not a valid sound file"
        return 
    sound = cutSound(sound, start,end)
    exportSound(sound, 'result.mp3')
    exportSound(sound,'result.wav')

if __name__ == '__main__':
    test()
