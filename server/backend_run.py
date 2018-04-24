import os
import backend

class task:
    # basic unit of client-server interaction
    
    def __init__(self,content_audio_path): # fixed after "cut"
        self.endecoder=backend.encoder_decoder(content_audio_path)
        self.converter=backend.converter(self.endecoder.base_name)

    def soundToImage(self): # to spectrum
        return self.endecoder.audio2img()
   
    def convert(self,style): # texture transfer of spectra
        self.endecoder.setTransImgPath(style)
        return self.converter.run(self.endecoder.content_img_path,self.endecoder.trans_img_path,style)

    def imageToSound(self,quality,style): # restore audio with spectra
        self.endecoder.setTransSoundPath(style,quality)
        self.endecoder.img2audio(quality)

