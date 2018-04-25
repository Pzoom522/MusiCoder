# -*- coding:utf-8 -*-
import sys
from PyQt4 import QtGui,QtCore
from pydub import AudioSegment
from player import Player
import thread
import time
import design
import math

# This class is used to replace normal slider.Which modifies the slider behaviour when mouse clicked.
# The normal slider will move a little in the direction of mouse.And this one will move set the position 
# excatly as the mouse is. 
class QCustomSlider(QtGui.QSlider):
    release=QtCore.pyqtSignal() 
    def mousePressEvent(self,ev):
        if ev.button()==QtCore.Qt.LeftButton:
            ev.accept()
            self.setValue(self.minimum()+(self.maximum()-self.minimum())*ev.x()/self.width())
        super(QCustomSlider,self).mousePressEvent(ev)

#This class is a PyQt-implemented sound player. It will act as most of the players you see.
#It contains player as the core to do the playing work.
class QPlayer(QtGui.QWidget):
    def __init__(self,parent=None):
        super(QPlayer,self).__init__(parent=parent)
        self.__initUI__()

    def __initUI__(self):    
        
        #Set up almost all the ui components.
        self.btn=QtGui.QPushButton("",self)
        self.btn.setGeometry(design.PlayButton.pos_x,design.PlayButton.pos_y,design.PlayButton.size_x,design.PlayButton.size_y)
        self.btn.clicked.connect(self.buttonClicked)
        self.btn.setEnabled(False) 
        self.btn.setStyleSheet('QPushButton{background:transparent;background-image:url(%s)}'%design.PlayButton.play_unable)

        self.pressed=False

        self.lbl_now=QtGui.QLabel(self) #current time label
        self.lbl_now.setGeometry(design.PlayTimeNow.pos_x,design.PlayTimeNow.pos_y,design.PlayTimeNow.size_x,design.PlayTimeNow.size_y)
        self.lbl_now.setText("00:00")
        
        self.setStyleSheet('QLabel{background:transparent;color:white}')

        self.lbl_end=QtGui.QLabel(self) #Music length label 
        self.lbl_end.setGeometry(design.PlayTimeTotal.pos_x,design.PlayTimeTotal.pos_y,design.PlayTimeTotal.size_x,design.PlayTimeTotal.size_y)
        self.lbl_end.setText("00:00")

        self.sld=QCustomSlider(QtCore.Qt.Horizontal,self)
        self.sld.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld.setGeometry(design.PlayBar.pos_x,design.PlayBar.pos_y,design.PlayBar.size_x,design.PlayBar.size_y)
        self.sld.valueChanged[int].connect(self.changeValue) 
        self.sld.sliderPressed.connect(self.sliderPressed)
        self.sld.sliderReleased.connect(self.sliderReleased)
        self.connect(self.sld,QtCore.SIGNAL('mouseReleaseEvent()'),self,QtCore.SLOT('sliderReleased'))
        self.sld.setEnabled(False)

        self.show()

    def buttonClicked(self):
        # --Event proccessing func.
        # Set player accoding to its state
        if self.p.isPlay:
            self.p.stop()
            self.btn.setStyleSheet('QPushButton{background:transparent;background-image:url(%s)}'%design.PlayButton.play)
        else:
            self.p.play()
            self.btn.setStyleSheet('QPushButton{background:transparent;background-image:url(%s)}'%design.PlayButton.pause)

    def pause(self):
        self.p.stop()
        self.btn.setStyleSheet('QPushButton{background:transparent;background-image:url(%s)}'%design.PlayButton.play)

    def changeValue(self,val): 
        # --Event proccessing func.
        # Change lable`s text when slider is slidered.
        self.lbl_now.setText("%02d:%02d"% divmod(val,60))


    def sliderPressed(self): #
        # --Event proccessing func.
        self.pressed=True    
        #Set self.pressed

    def sliderReleased(self):
        # --Event proccessing func.
        # Change the current playing position when slider is released.
        val=self.sld.value()
        
        isPlay=self.p.isPlay

        self.p.stop()
        self.p.setPosition(val)

        if isPlay:  #Recover the state stored.
           self.p.play()

        self.pressed=False

    def __track__(self):
       
        #Move slider to show how much music is played.
        ratio=self.p.position()/self.p.length()
        
        #1. Reset position if the music is done.
        if ratio>=1 and self.p.isPlay==False:
            self.p.setPosition(0)
            ratio=0
            self.btn.setStyleSheet('QPushButton{background:transparent;background-image:url(%s)}'%design.PlayButton.play)
        
        #2. Update slider and labels.
        if not self.pressed:
            val=int(self.p.position())
            self.sld.setValue(val)
            t=int(self.p.position())
            self.lbl_now.setText("%02d:%02d"% divmod(t,60))

    def track(self):
        # Set a timer to use call __track__ function.
        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.__track__)
        self.timer.start(1000)

    def addMusic(self,segment): 
        # Load a AudioSegment object.
        self.btn.setEnabled(True)
        self.btn.setStyleSheet('QPushButton{background:transparent;background-image:url(%s)}'%design.PlayButton.play)
       
        self.sld.setEnabled(True)
        self.p=Player(segment)

        t=math.floor(self.p.length())
        self.sld.setMaximum(t)
        self.lbl_end.setText("%02d:%02d"% divmod(t,60))

        self.track()

    def removeMusic(self):
        # Remove the music it loads. And it  will stop playing.
        self.timer.stop()
        self.p.close()

        #self.btn.setText("Play")
        self.btn.setEnabled(False)
        self.btn.setStyleSheet('QPushButton{background:transparent;background-image:url(%s)}'%design.PlayButton.play_unable)

        self.sld.setValue(0)
        self.sld.setEnabled(False)

        self.lbl_end.setText("00:00")
        self.lbl_now.setText("00:00")

    def close(self):
        # Close itself.
        self.p.close()

    def hide(self):
        # Hide itself and stop playing.
        self.p.stop()
        self.btn.hide()
        self.lbl_now.hide()
        self.lbl_end.hide()
        self.sld.hide()

    def show(self):
        # Show it self.
        self.btn.show()
        self.lbl_now.show()
        self.lbl_end.show()
        self.sld.show()
        

if __name__=="__main__":
    # This is a demo to show QPlayer
    app=QtGui.QApplication(sys.argv)
    
    widget=QtGui.QWidget()
    widget.show()

    ply=QPlayer(widget)                     # init and set geometry
    ply.addMusic(AudioSegment.from_mp3('Adele - Rolling In the Deep.mp3'))
    ply.setGeometry(200,200,600,100)


    sys.exit(app.exec_())
