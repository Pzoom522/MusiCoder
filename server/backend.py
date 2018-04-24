# -*- coding: utf-8 -*-
import os
import json
import matplotlib
matplotlib.use('Agg') # No pictures displayed
from matplotlib import pyplot as plt
import pylab
import scipy
from PIL import Image
import librosa
import librosa.display
import numpy as np
import multiprocessing as mp
from pydub import AudioSegment


class encoder_decoder:

    def __init__(self,audio_path):# shared para of EN/DEcoder. Set according to Content Audio

        self.limit=-80 # min value of db_matrix. default=-80(~=silence)
        self.max_volume=256 # max volume. default=256
        self.mode_pace={'LOFI':10,'STD':15,'HIFI':25}

        self.base_name=self.getBaseName(audio_path) # [TODO]加入唯一标识，比如ip+时间等，或者设计散列算法i
        self.content_auido_path=audio_path
        self.trans_audio_path  ='./temp/'+self.base_name+'_raw.wav'
        self.content_img_path  ='./temp/'+self.base_name+'.jpg'
        self.trans_img_path    ='./temp/'+self.base_name+'_trans.jpg'
        print(self.trans_img_path)#debug

    def getBaseName(self,audio_path):
        base_name=os.path.splitext(os.path.basename(audio_path))[0]
        return base_name
    
    def setTransImgPath(self,style):
        self.trans_img_path   ='./temp/'+self.base_name+'_'+style+'.jpg'
        pass

    def setTransSoundPath(self,style,quality):
        self.trans_audio_path ='./temp/'+self.base_name+'_'+style+'_'+quality+'.mp3'
        pass

    def getSpectrumMatrix(self,audio_path): # auido_file => db_matrix
        print(audio_path)
        sig, fs = librosa.load(audio_path,sr=None)
        D = np.abs(librosa.stft(sig))
        self.max_volume=np.max(D) # update
        D=librosa.amplitude_to_db(D,ref=np.max)
        return D

    def audio2img(self): # ENCODER
        spectrum = self.getSpectrumMatrix(self.content_auido_path)
        self.limit=np.min(spectrum) # update
        spectrum[spectrum<0.618*self.limit]=self.limit # remove BG noise & focus on texture

        pylab.axis('off') # no axis
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[]) # remove the white edge
        librosa.display.specshow(spectrum,cmap='magma',x_axis='time')
        fig = matplotlib.pyplot.gcf() # get handler
        fig.set_size_inches(10.25, 8.62)
        fig.savefig(self.content_img_path, dpi=100) # ideal pixel:1025*862(default mtx.shape)

        fig.clf()
        # DO NOT MODIFY
        # Pzoom-2018/03/07/01:48

        return True

    def readMagmaDiff(self): # get cmap diff list. default: magma
        magma_dif_list=[]
        with open('./data/magma_diff.json','r') as magma_file:
            magma_dif_list = json.loads(magma_file.read())['_magma_difference']
        return magma_dif_list

    def readImg(self,spectrum_path): # img_file => rgb_sum_matrix
        img_file=Image.open(spectrum_path)
        img_file = img_file.resize((862, 1025),Image.ANTIALIAS) # to make sure matrix_size fits
        mtx_rgb=np.array(img_file.transpose(Image.FLIP_TOP_BOTTOM)) # reverse
        mtx_rgb_sum=np.sum(mtx_rgb,2)/float(255)
        return mtx_rgb_sum

    def curver(self,mtx_rgb_sum,magma_dif_list): # rgb_sum_matrix => [0~1]_value_matrix. 256 values.
        mtx_value=np.ones(mtx_rgb_sum.shape)
        mtx_unit=np.ones(mtx_rgb_sum.shape) 
        # mtx_value=mtx_unit=np.ones(mtx_rgb_sum.shape)
        # avoid continuous assignments since it's shallow copying
        i=0
        for dif in magma_dif_list:
            mtx_rgb_sum=mtx_rgb_sum-dif*mtx_unit # get present diff matrix
            mtx_value[mtx_rgb_sum<0]=i/float(255)
            mtx_rgb_sum[mtx_rgb_sum<0]=3 # aviod re-write
            i=i+1
        return mtx_value

    def GLA(self,index,mtx_amp,pace): # index@segment
    # D. W. Griffin and J. S. Lim, “Signal estimation from modified short-time Fourier transform,” IEEE Trans. ASSP, vol.32, no.2, pp.236–243, Apr. 1984.
        
        phase = np.exp(1.j * np.random.uniform(0., 2*np.pi, size=mtx_amp.shape))
        x_ = librosa.istft(mtx_amp * phase)
        for i in range(pace*10):
            _, phase = librosa.magphase(librosa.stft(x_))
            x_ = librosa.istft(mtx_amp * phase)
        return x_

    def wav2mp3(self,filepath):
        filedir,basename=os.path.split(filepath)
        barename=os.path.splitext(basename)[0]
        filepath_new=os.path.join(filedir,barename+'.mp3')
        AudioSegment.from_wav(filepath).export(filepath_new)
        return filepath_new

    def reconstructer(self,mtx_amp,mode): # master of GLA
        pace=self.mode_pace.get(mode,self.mode_pace.get('STD')) # default_mode='STD'
        mtx_amp=(self.max_volume/np.max(mtx_amp))*mtx_amp
        # split into 5 parts (5*173=865~=861)
        mtx_amp_segs = [[0,mtx_amp[:,0*173:1*173],pace],
                        [1,mtx_amp[:,1*173:2*173],pace],
                        [2,mtx_amp[:,2*173:3*173],pace],
                        [3,mtx_amp[:,3*173:4*173],pace],
                        [4,mtx_amp[:,4*173:5*173],pace]]
        try:
            pool=mp.Pool()
            seg_songs=pool.starmap(self.GLA,mtx_amp_segs) # multiprocess. CPU num sensitive.
        finally:
            pool.close()
            pool.join() # [FIX TRY]: terminate zombies

        combined_sounds=np.hstack((seg_songs[0],seg_songs[1],seg_songs[2],seg_songs[3],seg_songs[4]))
 
        scipy.io.wavfile.write(self.trans_audio_path, 44100, combined_sounds) # [TODO] condition@44100
      
        self.trans_audio_path=(self.wav2mp3(self.trans_audio_path)).strip('\n')
        print(self.trans_audio_path)
        repr(self.trans_audio_path)
        return True

    def img2audio(self,mode): # DECODER
        magma_dif_list=self.readMagmaDiff()
        mtx_rgb_sum=self.readImg(self.trans_img_path)
        mtx_value=self.curver(mtx_rgb_sum,magma_dif_list)

        mtx_unit=np.ones(mtx_value.shape)
        mtx_db=(mtx_value/np.max(mtx_value)-mtx_unit)*float(abs(self.limit)) # get "normalized" db matrix
        mtx_amp=librosa.db_to_amplitude(mtx_db,ref=1.0)

        return self.reconstructer(mtx_amp,mode)
        # to be denoised

class converter:
    def __init__(self,base_name):
        self.model_paths={
                        'water':'converter/models/water.ckpt',
                        'future':'converter/models/future.ckpt',
                        'laser':'converter/models/laser.ckpt'

        }
        self.base_name=base_name

    def run(self,orig_img_path,trans_img_path,style):
        result=os.popen('python3 converter/run.py '+\
                        '--content '+orig_img_path+' '+\
                        '--style_model '+self.model_paths.get(style,'converter/models/water.ckpt')+' '+\
                        '--output '+trans_img_path+' &').read()
        if "DONE" in result:
            return True
        else:
            print(result)
            return False
