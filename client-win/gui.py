# -*- coding: utf-8 -*-
import sys
import shutil
from PyQt4 import QtGui,QtCore,Qt
from QPlayer import QPlayer
from QSegmentSelector import QSegmentSelector
from interface import loadSound, cutSound, exportSound, balanceSound
from player import Player
import client
import design
import os,time

def notConnected():
    #when connection is lost
    #close convert-quality dialog
    if hasattr(Window.w,'quality'):
        Window.w.quality.close()
    #lock buttons, show disconnection message and try button
    Window.w.record()
    Window.w.lock()
    Window.w.label.setText('not connected')
    Window.w.do.setText('Converted Song will be Shown Here')
    Window.w.do.setStyleSheet('QLabel {background:transparent;color:white;background-image:url(%s)}'%design.OriginalSpec.back)
    Window.w.do.setAlignment(QtCore.Qt.AlignCenter)

    if Window.w.db_able!=True:
        Window.w.dfh.setText('Push retry Button to Connect the Server')
    Window.w.retry.show()
    return

#dialog to choose convertion quality
class ConvertQuality(QtGui.QDialog):

    def __init__(self,parent):

        super(ConvertQuality,self).__init__(parent=parent)
        #no help button
        self.setWindowFlags(self.windowFlags()&~QtCore.Qt.WindowContextHelpButtonHint)
        
        self.parent = parent
        self.setWindowTitle('Quality')
        self.setFixedSize(design.ConvertDialog.size_x,design.ConvertDialog.size_y)
        #three quality options
        self.btn1 = QtGui.QRadioButton('LOFI - 20 seconds',parent=self)
        self.btn2 = QtGui.QRadioButton('Standard - 30 seconds',parent=self)
        self.btn3 = QtGui.QRadioButton('HIFI - 45 seconds',parent=self)
        self.label = QtGui.QLabel('',parent=self)
        grp = QtGui.QButtonGroup(self)
        grp.addButton(self.btn1)
        grp.addButton(self.btn2)
        grp.addButton(self.btn3)
        
        #ok/cancel button
        self.ok = QtGui.QPushButton('OK',parent=self)
        self.cancel = QtGui.QPushButton('Cancel',parent=self)
        self.ok.setEnabled(False)

        #signal/slot
        self.ok.clicked.connect(self.confirm)
        self.cancel.clicked.connect(self.cancel_)
        self.btn1.clicked.connect(self.low)
        self.btn2.clicked.connect(self.medium)
        self.btn3.clicked.connect(self.high)

        #layout
        self.btn1.move(design.ConvertDialog.radio_pos_x,design.ConvertDialog.radio_pos_y)
        self.btn2.move(design.ConvertDialog.radio_pos_x,design.ConvertDialog.radio_pos_y+design.ConvertDialog.radio_pos_marg)
        self.btn3.move(design.ConvertDialog.radio_pos_x,design.ConvertDialog.radio_pos_y+2*design.ConvertDialog.radio_pos_marg)
        self.ok.setGeometry(design.ConvertDialog.ok_pos_x,design.ConvertDialog.button_pos_y,design.ConvertDialog.button_size_x,design.ConvertDialog.button_size_y)
        self.ok.setStyleSheet('QPushButton{background:transparent}')
        self.cancel.setGeometry(design.ConvertDialog.cancel_pos_x,design.ConvertDialog.button_pos_y,design.ConvertDialog.button_size_x,design.ConvertDialog.button_size_y)
        self.cancel.setStyleSheet('QPushButton{background:transparent}')

        self.setStyleSheet('QDialog{background-image:url(%s)}'%design.ConvertDialog.back)
        self.resize(design.ConvertDialog.size_x,design.ConvertDialog.size_y)

    #chose low
    def low(self):

        self.qt = 0
        self.ok.setEnabled(True)

    #chose medium
    def medium(self):

        self.qt = 1
        self.ok.setEnabled(True)

    #chose high
    def high(self):

        self.qt = 2
        self.ok.setEnabled(True)

    #ok clicked
    def confirm(self):

        self.done(self.qt)
        
    #cancel clicked
    def cancel_(self):

        self.done(-1)

    #x clicked
    def closeEvent(self,event):

        print('close event of convert dialog')
        self.done(-1)

#dialog to choose texture
class StyleDialog(QtGui.QDialog):

    #texture set
    styleSet = ['laser','water','future']
    #confirmed texture
    style = 'laser'

    def __init__(self,parent):

        super(StyleDialog,self).__init__(parent=parent)
        
        self.setWindowFlags(self.windowFlags()&~QtCore.Qt.WindowContextHelpButtonHint)
        
        self.setWindowTitle('Texture')
        self.setFixedSize(design.StyleDialog.size_x,design.StyleDialog.size_y)
        self.setStyleSheet('QDialog{background-image:url(%s)}'%design.StyleDialog.back)
        self.resize(design.StyleDialog.size_x,design.StyleDialog.size_y)

        #records style chosen now (combo box)
        self.style = StyleDialog.style

        #combo box
        self.cb = QtGui.QComboBox(self)
        self.cb.addItem(StyleDialog.style)
        for s in StyleDialog.styleSet:
            if s != StyleDialog.style:
                self.cb.addItem(s)
        self.cb.setStyleSheet('QComboBox{background-color:white}')

        #try button to listen to the sample
        tr = QtGui.QPushButton('Try',self)
        tr.setStyleSheet('QPushButton {background:transparent}')

        self.ok = QtGui.QPushButton('OK',self)
        self.ok.setStyleSheet('QPushButton{background:transparent}')

        #signal/slot
        self.cb.activated[str].connect(self.setStyle)
        tr.clicked.connect(self.tryStyle)
        self.ok.clicked.connect(self.confirm)

        #layout
        self.cb.setGeometry(design.StyleDialog.cb_pos_x,design.StyleDialog.cb_pos_y,design.StyleDialog.cb_size_x,design.StyleDialog.cb_size_y)
        tr.setGeometry(design.StyleDialog.try_pos_x,design.StyleDialog.button_pos_y,design.StyleDialog.button_size_x,design.StyleDialog.button_size_y)
        self.ok.setGeometry(design.StyleDialog.ok_pos_x,design.StyleDialog.button_pos_y,design.StyleDialog.button_size_x,design.StyleDialog.button_size_y)
        
    #change texture through combo box
    def setStyle(self,string):

        self.style = string

    #listen to the sample
    def tryStyle(self):

        #stop playing previous one if there is any
        self.stopMusic()
        if self.style=='future':
            styleMusic = loadSound('Style/'+str(self.style)+'_10.mp3')
        else:
            styleMusic = loadSound('Style/'+str(self.style)+'_10.wav')
        self.player = Player(styleMusic)
        self.player.play()

    def confirm(self):
        self.stopMusic()
        StyleDialog.style = self.style
        self.done(2)

    def closeEvent(self,event):
        self.stopMusic()
        event.accept()

    def stopMusic(self):
        if hasattr(self,'player'):
            if self.player.isPlay:
                self.player.close()
                
#define several signals to communicate with recieve-thread
class Communicate(QtCore.QObject):

    recieveFile = QtCore.pyqtSignal()
    receiveImageOrig = QtCore.pyqtSignal()
    receiveImageTrans = QtCore.pyqtSignal()
    receiveSound = QtCore.pyqtSignal()
    socketError = QtCore.pyqtSignal()

#where converted spectrum is shown
class DragOut(QtGui.QLabel):

    def __init__(self,parent):

        super(DragOut,self).__init__(parent)

        self.setText('Converted Song will be Shown Here')
        self.setStyleSheet('QLabel {background:transparent;color:white;background-image:url(%s)}'%design.OriginalSpec.back)
        self.setAlignment(QtCore.Qt.AlignCenter)

        self.dragable = False

    def showSpec(self,path):

        #scale the spec and show
        spec = QtGui.QImage(path)
        labelSize = self.size()        
        spec = spec.scaled(labelSize)

        self.setPixmap(QtGui.QPixmap.fromImage(spec))

        

#the delete button which will be shown in left spectrum area
class DeleteButton(QtGui.QPushButton):

    def __init__(self,parent):

        super(DeleteButton,self).__init__('',parent=parent)

        self.resize(design.DeleteButton.size_x,design.DeleteButton.size_y)
        self.move(design.OriginalSpec.size_x-design.DeleteButton.size_x,0)
        #invisible at first
        self.setFlat(True)
        self.setText('')

    #mouse enters
    def enterEvent(self,e):

        #button shows up
        self.setStyleSheet('QPushButton {background:transparent;background-image:url(%s)}' % design.DeleteButton.back)
        self.setFlat(False)

    #mouse leave
    def leaveEvent(self,e):

        #button gets invisble
        self.setStyleSheet('QPushButton{background:transparent}')
        self.setFlat(True)
        self.setText('')


#the area to accept drag-in music file, and show original spectrum
class DragFileHere(QtGui.QLabel):

    def __init__(self,parent):

        super(DragFileHere,self).__init__(parent)
        self.setAcceptDrops(False)
        
        self.setText('please wait...')
        self.setStyleSheet('QLabel {background:transparent;color:white;background-image:url(%s)}'%design.OriginalSpec.back)
        self.setAlignment(QtCore.Qt.AlignCenter)
        #delete button is hidden until a file is accepted
        self.db = DeleteButton(self)
        self.db.clicked.connect(self.dbClicked)
        self.db.hide()

        self.c = Communicate()

    #drag in file
    def dragEnterEvent(self, e):

        #only accept .mp3 and .wav file
        if e.mimeData().hasUrls()&e.mimeData().urls()[0].path().endsWith('.mp3'):
            e.accept()
        elif e.mimeData().hasUrls()&e.mimeData().urls()[0].path().endsWith('.wav'):
            e.accept()
        else:
            e.ignore()

    #drop file
    def dropEvent(self,e):

        #one file at a time
        if len(e.mimeData().urls())>1:
            self.em = QtGui.QErrorMessage()
            self.em.setWindowTitle('Error')
            self.em.showMessage('Drag ONE file at a time')
            return

        self.filePath = e.mimeData().urls()[0].path()
        self.c.recieveFile.emit()

    #DELETE button clicked
    def dbClicked(self):

        self.setText('Drag .mp3 .wav Files Here')
        self.db.hide()


#the main window
class Window(QtGui.QWidget):

    #record the Window object
    w = 0

    def __init__(self,app):

        super(Window,self).__init__()
        
        self.setAcceptDrops(True)
        self.setFixedSize(design.Window.size_x,design.Window.size_y)

        palet = QtGui.QPalette()
        back = QtGui.QImage(design.Window.back)
        back = back.scaled(self.size())
        palet.setBrush(QtGui.QPalette.Window,QtGui.QBrush(QtGui.QPixmap.fromImage(back)))
        self.setPalette(palet)
        
        self.setWindowTitle('Musicoder')
        #no maximize button, the size is fixed
        self.setWindowFlags(self.windowFlags()&~QtCore.Qt.WindowMaximizeButtonHint)
        self.setWindowIcon(QtGui.QIcon(design.Window.icon))

        self.app = app

        self.c = Communicate()
        
        self.init()
        self.show()

    def initClient(self,first):
        #init client during initialization, and when retry button is clicked
        
        print('init client')
        try:
            default_addr=('140.143.62.99',2333)
            if len(sys.argv)==1:
                self.client=client.connect(*default_addr)
            else:
                self.client=client.connect(sys.argv[1],int(sys.argv[2]))
            self.client.connectFail(self.c.socketError)
            self.c.socketError.connect(notConnected)
            self.app.processEvents()
            self.client.listen()
        except Exception as e:
            #set label, lock buttons if needed
            print('failed')
            print(e)
            if first:
                notConnected()
            self.label.setText('not connected')
            self.retry.show()
            self.app.processEvents()
            return
        
        #recover buttons, set labels and others
        print('connected')
        if first==False:
            self.recover()
        else:
            self.dfh.setAcceptDrops(True)
            self.dfh.setText('Drag .mp3 .wav Files Here')
            self.label.setText('connected')
        self.app.processEvents()

    def reConnect(self):
        #retry clicked
        print('reconnect')
        self.wait()
        self.initClient(False)

    def wait(self):
        #set some message label, init client procedure may take some time
        self.label.setText('please wait')
        self.label.repaint()
        self.retry.hide()
        self.app.processEvents()
   
    def init(self):
        
        self.filename_limit=50

        self.style = 'laser'

        self.db_able = False

        #the area to accept music file/ the area to show original spectrum
        self.dfh = DragFileHere(self)
      
        #the area to show converted spectrum
        self.do = DragOut(self)

        #convert button
        self.cv = QtGui.QPushButton('',parent=self)
        self.cv.setEnabled(False)
        self.cv.setStyleSheet('QPushButton{background:transparent;background-image:url(%s)}'%design.ConvertButton.back_unable)

        #help(info) button
        hp = QtGui.QPushButton('',parent=self)
        hp.setStyleSheet('QPushButton {background:transparent;background-image:url(%s)}' % design.HelpButton.back)

        #cut button
        self.sl = QtGui.QPushButton('',parent=self)
        self.sl.setStyleSheet('QPushButton {background:transparent;background-image:url(%s)}' % design.SelectButton.back_unable)
        self.sl.setEnabled(False)

        #save button
        self.sv = QtGui.QPushButton('',parent=self)
        self.sv.setEnabled(False)
        self.sv.setStyleSheet('QPushButton{background:transparent;background-image:url(%s)}'%design.SaveButton.back_unable)

        #texture button
        self.select_style = QtGui.QPushButton('',parent = self)
        self.select_style.setStyleSheet('QPushButton{background:transparent;background-image:url(%s)}'%design.StyleButton.back)

        #two players
        self.pl1 = QPlayer(parent=self)
        self.pl2 = QPlayer(parent=self)

        #label and button related to connection
        self.label = QtGui.QLabel('connecting...',parent=self)
        self.label.setStyleSheet('QLabel{background:transparent;color:white}')
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.retry = QtGui.QPushButton('retry',parent=self)
        self.retry.setStyleSheet('QPushButton{border:2px groove black;border-radius:10px;padding:2px 4px}''QPushButton:pressed{background-color:rgb(85, 170, 255);border-style: inset; }')
        self.retry.hide()
        font.setPointSize(11)
        self.retry.setFont(font)

        #sinals/slots
        self.dfh.db.clicked.connect(self.dbClicked)
        self.dfh.c.recieveFile.connect(self.enableCv)
        self.dfh.c.receiveImageOrig.connect(self.loadImageLeft)
        self.dfh.c.receiveImageTrans.connect(self.loadImageRight)
        self.dfh.c.receiveSound.connect(self.loadResultSound)
        
        hp.clicked.connect(self.helpInfo)
        self.sl.clicked.connect(self.selectSeg)
        self.sv.clicked.connect(self.save)
        self.cv.clicked.connect(self.convertClicked)
        self.select_style.clicked.connect(self.styleDialog)
        self.pl1.btn.clicked.connect(self.pausePl2)
        self.pl2.btn.clicked.connect(self.pausePl1)
        self.retry.clicked.connect(self.reConnect)

        #layout
        self.dfh.setGeometry(design.OriginalSpec.pos_x,design.OriginalSpec.pos_y,design.OriginalSpec.size_x,design.OriginalSpec.size_y)
        self.do.setGeometry(design.ConvertedSpec.pos_x,design.ConvertedSpec.pos_y,design.ConvertedSpec.size_x,design.ConvertedSpec.size_y)
        self.cv.setGeometry(design.ConvertButton.pos_x,design.ConvertButton.pos_y,design.ConvertButton.size_x,design.ConvertButton.size_y)
        hp.setGeometry(design.HelpButton.pos_x,design.HelpButton.pos_y,design.HelpButton.size_x,design.HelpButton.size_y)
        self.sl.setGeometry(design.SelectButton.pos_x,design.SelectButton.pos_y,design.SelectButton.size_x,design.SelectButton.size_y)
        self.sv.setGeometry(design.SaveButton.pos_x,design.SaveButton.pos_y,design.SaveButton.size_x,design.SaveButton.size_y)
        self.pl1.setGeometry(design.LeftPlayer.pos_x,design.LeftPlayer.pos_y,design.LeftPlayer.size_x,design.LeftPlayer.size_y)
        self.pl2.setGeometry(design.RightPlayer.pos_x,design.RightPlayer.pos_y,design.RightPlayer.size_x,design.RightPlayer.size_y)
        self.select_style.setGeometry(design.StyleButton.pos_x,design.StyleButton.pos_y,design.StyleButton.size_x,design.StyleButton.size_y)
        self.label.setGeometry(design.ConnectLabel.pos_x,design.ConnectLabel.pos_y,design.ConnectLabel.size_x,design.ConnectLabel.size_y)
        self.retry.setGeometry(design.RetryButton.pos_x,design.RetryButton.pos_y,design.RetryButton.size_x,design.RetryButton.size_y)
    
    # generate a temp filename based on current time and cut-window
    def genTempFileName(self,stv,edv):
        _,filename=os.path.split(self.filePath)
        name,ext=os.path.splitext(filename)
        time_str=time.strftime("%Y-%m-%d %H-%M-%S",time.localtime(time.time()))
        filename_temp="%s_%d_%d%s"%(time_str,stv,edv,ext)
        filename_temp=filename_temp.replace(" ","_")
        return filename_temp
    
    def styleDialog(self):
        #texture button clicked, show texture dialog, get result when it's closed

        self.pausePl1()
        self.pausePl2()
        style_dialog = StyleDialog(self)
        style_dialog.open()
        style_dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        style_dialog.exec_()
        if style_dialog.result()==2:
            self.style = StyleDialog.style

    def pausePl1(self):

        #pause left player
        if hasattr(self.pl1,'p'):
            if self.pl1.p.isPlay:
                self.pl1.pause()

    def pausePl2(self):

        #pause right player
        if hasattr(self.pl2,'p'):
            if self.pl2.p.isPlay:
                self.pl2.pause()

    #after recieving a music file
    def enableCv(self):

        self.filePath = unicode(self.dfh.filePath[1:].toUtf8(),'utf-8').encode('gbk')
        print(self.filePath)
        
        #balance volume first
        #self.filePath = balanceSound(self.filePath)
        print(self.filePath)
        self.originalSong = loadSound(self.filePath)
        self.pl1.addMusic(self.originalSong)
        self.length = int(self.originalSong.duration_seconds)
        
        #cut first 10 sec and get spectrum for the segment
        self.cutSong = cutSound(self.originalSong,0,min(10,self.length))
        self.edv = min(10,self.length)
        
        filename_temp=self.genTempFileName(0,self.edv)
        exportSound(self.cutSong,filename_temp)
        self.isOriginal = True
        try:
            self.client.sendSound(filename_temp)
            self.client.fileRecv(self.dfh.c.receiveImageOrig)
        except Exception:
            notConnected()
            return
        os.remove(filename_temp)
        
    #after origin image is received   
    def loadImageLeft(self):
        specPath=self.client.filepath
        spec = QtGui.QImage(specPath)
        labelSize = self.dfh.size()
        spec = spec.scaled(labelSize)
        self.dfh.setPixmap(QtGui.QPixmap.fromImage(spec))
        self.dfh.db.show()
        if self.isOriginal:
            #default (first 10 sec)
            self.sl.setEnabled(True)
            self.sl.setStyleSheet('QPushButton{background:transparent;background-image:url(%s)}'%design.SelectButton.back)
        else:
            #after cut by user
            self.cv.setEnabled(True)
            self.cv.setStyleSheet('QPushButton{background:transparent;background-image:url(%s)}'%design.ConvertButton.back)
            self.dfh.setAcceptDrops(False)
        self.db_able = True
    
    #after transfered image is received  
    def loadImageRight(self):
        filepath=self.client.filepath
        specPath2=filepath
        #load sound, show spectrum
        self.do.showSpec(specPath2)
        try:
            self.client.fileRecv(self.dfh.c.receiveSound)
        except Exception:
            notConnected()
            return
        self.dfh.db.show()
        #unlock texture button
        self.select_style.setEnabled(True)
        self.select_style.setStyleSheet('QPushButton{background:transparent;background-image:url(%s)}'%design.StyleButton.back)
        
    #after result sound is received 
    def loadResultSound(self):
        filepath=self.client.filepath
        self.musicPath=filepath
        convMusic = loadSound(filepath)
        self.pl2.addMusic(convMusic)
        #self.psc.setEnabled(True)
        self.sv.setEnabled(True)
        self.sv.setStyleSheet('QPushButton{background:transparent;background-image:url(%s)}'%design.SaveButton.back)

    #DELETE button clicked
    def dbClicked(self):

        #back to initial state, except for save function and other unrelated functions
        self.cv.setEnabled(False)
        self.cv.setStyleSheet('QPushButton{background:transparent;background-image:url(%s)}'%design.ConvertButton.back_unable)
        self.sl.setEnabled(False)
        self.sl.setStyleSheet('QPushButton{background:transparent;background-image:url(%s)}'%design.SelectButton.back_unable)
        self.pl1.removeMusic()
        self.pl1.show()
        self.dfh.setAcceptDrops(True)
        if hasattr(self,'seg_slc'):
            self.seg_slc.close()

        self.db_able = False

    #save result
    def save(self):

        fname = QtGui.QFileDialog.getSaveFileName(self,'Save','./song.mp3')
        print(self.musicPath)
        try:
            shutil.copy(self.musicPath,fname)
        except Exception:
            return

        self.do.setText('Converted Song will be Shown Here')
        self.pl2.removeMusic()
        self.sv.setEnabled(False)
        self.sv.setStyleSheet('QPushButton{background:transparent;background-image:url(%s)}'%design.SaveButton.back_unable)

    #convert button clicked, show convertion quality dialog
    def convertClicked(self):

        self.quality = ConvertQuality(self)
        self.quality.open()
        self.quality.exec_()
        r = self.quality.result()
        #r stands for quality; 0:low, 1:medium, 2:high
        #r is -1 when x or cancel is clicked
        if r==-1:
            print('cancel')
            return -1
        elif r==0:
            r='LOFI'
        elif r==1:
            r='STD'
        elif r==2:
            r='HIFI'

        #lock buttons and show gif
        self.lock()
        self.do.setStyleSheet('background:transparent')
        movie = QtGui.QMovie('Img/progress.gif')
        self.do.setMovie(movie)
        movie.start()
        
        try:
            self.client.convert(str(self.style),r)
            self.client.fileRecv(self.dfh.c.receiveImageTrans)
        except Exception:
            notConnected()

    #lock buttons, do not accept new file drops
    def lock(self):

        #will be called in case of disconnection
        #and when a convertion is started
        self.sl.setStyleSheet('QPushButton {background:transparent;background-image:url(%s)}' % design.SelectButton.back_unable)
        self.sl.setEnabled(False)
        self.cv.setEnabled(False)
        self.cv.setStyleSheet('QPushButton{background:transparent;background-image:url(%s)}'%design.ConvertButton.back_unable)
        self.select_style.setEnabled(False)
        self.select_style.setStyleSheet('QPushButton{background:transparent;background-image:url(%s)}'%design.StyleButton.back_unable)
        self.dfh.setAcceptDrops(False)
        self.dfh.db.hide()
        self.app.processEvents()

    #record the state befor locking buttons
    def record(self):

        self.sl_able = self.sl.isEnabled()

    #recover locked buttons after connection is rebuilt
    def recover(self):

        self.retry.hide()
        self.label.setText('connected')
        if self.sl_able:
            self.sl.setEnabled(True)
            self.sl.setStyleSheet('QPushButton{background:transparent;background-image:url(%s)}'%design.SelectButton.back)
        if self.db_able:
            self.dfh.db.show()
        else:
            self.dfh.setAcceptDrops(True)
            self.dfh.setText('Drag .mp3 .wav Files Here')
        self.select_style.setEnabled(True)
        self.select_style.setStyleSheet('QPushButton{background:transparent;background-image:url(%s)}'%design.StyleButton.back)
        self.app.processEvents()

    #help info, our sites can be visited by clicking on the hyperlinks
    def helpInfo(self):

        im = QtGui.QMessageBox.information(self,'info','&lt;MusiCoder: Corss-platform Music Texture'+
                                           ' Transfer System&gt;<br/><br/>For more info, please visit our '+
                                           '<a href="https://github.com/Pzoom522/MusiCoder">project site</a>, or '+
                                           'refer to our <a href="https://github.com/Pzoom522/MusiCoder/wiki">doc page</a>'+
                                           '.<br/><br/>&copy; 2018 MusiCoder')

    #cut the song, load the segment to player, send it to server to get spectrum
    def cut(self):
        
        #get time segment chosen by user, close segment selector, show player with segment loaded
        start = self.seg_slc.sld.value()
        end = min(self.length,start+10)
        self.seg_slc.close()
        self.cutSong = cutSound(self.originalSong,start,end)
        filename_temp=self.genTempFileName(start,end)
        filename_temp = 'Temp/'+filename_temp
        exportSound(self.cutSong,filename_temp)
        print('cut')
        try:
            song = loadSound(filename_temp)
        except Exception:
            print('exception')
            self.dfh.setPixmap(QtGui.QPixmap(design.OriginalSpec.warn))
            self.pl1.removeMusic()
            self.pl1.show()
            return
        self.pl1.removeMusic()
        self.pl1.addMusic(song)
        self.pl1.show()
        
        #send sound
        print('sendSound')
        self.isOriginal = False
        try:
            self.client.sendSound(filename_temp)
            os.remove(filename_temp)
            self.client.fileRecv(self.dfh.c.receiveImageOrig)
        except Exception:
            notConnected()
            return
   
    #cut button clicked
    def selectSeg(self):
        #get the position of player，hide player，show the segment selector
        
        self.sl.setEnabled(False)
        self.sl.setStyleSheet('QPushButton{background:transparent;background-image:url(%s)}'%design.SelectButton.back_unable)
        if self.pl1.p.isPlay:
            self.pl1.p.stop()
        pos = self.pl1.sld.value()
        self.pl1.hide()
        self.seg_slc = QSegmentSelector(pos,self.length,parent=self)
        self.seg_slc.show()
        self.seg_slc.setGeometry(design.LeftPlayer.pos_x,design.LeftPlayer.pos_y,design.LeftPlayer.size_x,design.LeftPlayer.size_y)
        self.seg_slc.ok.clicked.connect(self.cut)

    def closeEvent(self,event):
        #befor closing the window, clear the temp folder
        try:
            shutil.rmtree('Temp')
            os.mkdir('Temp')
        except:
            pass
        event.accept()
