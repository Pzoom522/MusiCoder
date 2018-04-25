# -*- coding: utf-8 -*-
from PyQt4 import QtGui,QtCore
import sys
import design

#the segment selector which will be shown when cut button is clicked
class QSegmentSelector(QtGui.QWidget):

    def __init__(self,pos,total,parent=None):
        super(QSegmentSelector,self).__init__(parent=parent)
        self.setStyleSheet('QLabel{background:transparent}')
        self.init(pos,total)

    def init(self,pos,total):
        self.total = total
        
        #the background slider, shows the full length of the music
        self.sld_back = QtGui.QSlider(QtCore.Qt.Horizontal,self)
        self.sld_back.setMaximum(total)
        self.sld_back.setGeometry(design.PlayBar.pos_x,design.PlayBar.pos_y,design.PlayBar.size_x-2,design.PlayBar.size_y)
        self.sld_back.setStyleSheet('QSlider::handle:horizontal{border:1px}')
        self.sld_back.setEnabled(False)

        #the actual slider, usually 10 sec shorter than the music length
        self.sld = QtGui.QSlider(QtCore.Qt.Horizontal,self)
        if total-10<=0:
            self.sliderLen = 0
            self.sld.setGeometry(design.PlayBar.pos_x,design.PlayBar.pos_y,15,design.PlayBar.size_y)
            self.sld.setMaximum(0)
            self.sld.setValue(0)
        else:
            self.sliderLen = design.PlayBar.size_x*float((total-10))/total
            self.sld.setGeometry(design.PlayBar.pos_x,design.PlayBar.pos_y,self.sliderLen,design.PlayBar.size_y)
            self.zero = False
            self.sld.setMaximum(total-10)
            if(pos<total-10):
                self.sld.setValue(pos)
            else:
                self.sld.setValue(total-10)
        self.sld.valueChanged[int].connect(self.changeValue)

        #the label showing the chosen segment
        self.lbl_now = QtGui.QLabel(self)
        st = '%02d:%02d'%divmod(self.sld.value(),60)
        ed = '%02d:%02d'%divmod(self.sld.value()+min(total,10),60)
        self.lbl_now.setText(st+' - '+ed)
        self.lbl_now.setGeometry(design.PlayTimeNow.pos_x,design.PlayTimeNow.pos_y,design.PlayTimeNow.size_x*2,design.PlayTimeNow.size_y)

        #total length of music
        self.lbl_end = QtGui.QLabel(self)
        self.lbl_end.setText('%02d:%02d'%divmod(total,60))
        self.lbl_end.setGeometry(design.PlayTimeTotal.pos_x,design.PlayTimeTotal.pos_y,design.PlayTimeTotal.size_x,design.PlayTimeTotal.size_y)

        #confirm button
        self.ok = QtGui.QPushButton(self)
        self.ok.setText('OK')
        self.ok.setGeometry(20,design.PlayButton.pos_y,162,50)
        self.ok.setStyleSheet('QPushButton{background-image:url(%s);border:none}'%design.SelectDialog.ok)

        #a translucent widget indicating the chosen segment on the slider
        self.area = QtGui.QLabel(self)
        self.area.setStyleSheet('QLabel{background:transparent}')
        img = QtGui.QImage(design.SelectDialog.area)
        
###################position adjustment which makes sure that handle and translucent widget won't fall apart#######################
        self.length = design.PlayBar.size_x*(float(min(total,10))/total)
        if total<=10:
            self.length-=15
        self.pos = design.PlayBar.pos_x+(self.sliderLen-15)*(float(self.sld.value())/max(total-10,1))
        self.area.setGeometry(self.pos+14,design.PlayBar.pos_y-16,self.length,50)
        img = img.scaled(design.PlayBar.size_x*10/total,23)
        self.area.setPixmap(QtGui.QPixmap(img))

    #called when handle is moved
    def changeValue(self,value):

        #change label value and adjust position
        st = '%02d:%02d'%divmod(self.sld.value(),60)
        ed = '%02d:%02d'%divmod(self.sld.value()+min(self.total,10),60)
        self.lbl_now.setText(st+' - '+ed)
        self.pos = design.PlayBar.pos_x+(self.sliderLen-15)*(float(self.sld.value())/max(self.total-10,1))
        self.area.move(self.pos+14,design.PlayBar.pos_y-16)

if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    widget = QSegmentSelector(0,8)
    widget.show()
    sys.exit(app.exec_())
            
