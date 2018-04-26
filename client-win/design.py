# -*- coding: utf-8 -*-
from PyQt4 import QtGui
import base64
import os
#these are modules that contain background images of widgets
import convert,convert_unable,delete,dialog,help_,icon,label_back
import pause,play_unable,play,save,save_unable,select_segment,ok,warn
import select_segment_unable,style,window_back,area,style_unable

#making sure a folder named Img exist in current path
if os.path.exists('Img')!=True:
    os.mkdir('Img')
#write images into Img folder
tmp = open('Img/dialog.png','wb+')
tmp.write(base64.b64decode(dialog.img))
tmp.close()
tmp = open('Img/label_back.png','wb+')
tmp.write(base64.b64decode(label_back.img))
tmp.close()

#designs for each widgets of gui, including size, position and image path

class ConvertDialog():

    back = 'Img/dialog.png'
    size_x = 505
    size_y = 290
    radio_pos_x = 100
    radio_pos_y = 40
    radio_pos_marg = 50
    button_size_x = 150
    button_size_y = 40
    button_pos_y = 205
    ok_pos_x = 68
    cancel_pos_x = 290

class StyleDialog():

    back = 'Img/dialog.png'
    size_x = 505
    size_y = 290
    button_pos_y = 205
    try_pos_x = 68
    ok_pos_x = 290
    button_size_x = 150
    button_size_y = 40
    cb_pos_x = 150
    cb_pos_y = 80
    cb_size_x = 200
    cb_size_y = 50

class SelectDialog():

    tmp = open('Img/area.png','wb+')
    tmp.write(base64.b64decode(area.img))
    tmp.close()
    area = 'Img/area.png'
    tmp = open('Img/ok.png','wb+')
    tmp.write(base64.b64decode(ok.img))
    tmp.close()
    ok = 'Img/ok.png'
    button_size_x = 150
    button_size_y = 40

class Window():

    tmp = open('Img/window_back.png','wb+')
    tmp.write(base64.b64decode(window_back.img))
    tmp.close()
    back = 'Img/window_back.png'
    tmp = open('Img/icon.png','wb+')
    tmp.write(base64.b64decode(icon.img))
    tmp.close()
    icon = 'Img/icon.png'
    button_color = QtGui.QColor(240,240,240)
    size_x = 1600
    size_y = 1000

class DeleteButton():

    tmp = open('Img/delete.png','wb+')
    tmp.write(base64.b64decode(delete.img))
    tmp.close()
    back = 'Img/delete.png'
    size_x = 150
    size_y = 175
    back_color = QtGui.QColor(255,60,60)


class ComboBox():
    
    pos_x = 430
    pos_y = 200
    size_x = 230
    size_y = 70

class HelpButton():

    tmp = open('Img/help.png','wb+')
    tmp.write(base64.b64decode(help_.img))
    tmp.close()
    back = 'Img/help.png'
    pos_x = 1450
    pos_y = 50
    size_x = 95
    size_y = 95

class TryButton():
    
    pos_x = 610
    pos_y = 300
    size_x = 100
    size_y = 50

class SelectButton():

    tmp = open('Img/select_segment.png','wb+')
    tmp.write(base64.b64decode(select_segment.img))
    tmp.close()
    back = 'Img/select_segment.png'
    tmp = open('Img/select_segment_unable.png','wb+')
    tmp.write(base64.b64decode(select_segment_unable.img))
    tmp.close()
    back_unable = 'Img/select_segment_unable.png'
    pos_x = 750
    pos_y = 290
    size_x = 102
    size_y = 103

class StyleButton():

    tmp = open('Img/style.png','wb+')
    tmp.write(base64.b64decode(style.img))
    tmp.close()
    back = 'Img/style.png'
    tmp = open('Img/style_unable.png','wb+')
    tmp.write(base64.b64decode(style_unable.img))
    tmp.close()
    back_unable = 'Img/style_unable.png'
    pos_x = 750
    pos_y = 430
    size_x = 102
    size_y = 103

class ConvertButton():

    tmp = open('Img/convert.png','wb+')
    tmp.write(base64.b64decode(convert.img))
    tmp.close()
    back = 'Img/convert.png'
    tmp = open('Img/convert_unable.png','wb+')
    tmp.write(base64.b64decode(convert_unable.img))
    tmp.close()
    back_unable = 'Img/convert_unable.png'
    pos_x = 750
    pos_y = 570
    size_x = 102
    size_y = 103

class SaveButton():

    tmp = open('Img/save.png','wb+')
    tmp.write(base64.b64decode(save.img))
    tmp.close()
    back = 'Img/save.png'
    tmp = open('Img/save_unable.png','wb+')
    tmp.write(base64.b64decode(save_unable.img))
    tmp.close()
    back_unable = 'Img/save_unable.png'
    pos_x = 750
    pos_y = 710
    size_x = 102
    size_y = 103

class OriginalSpec():

    back = 'Img/label_back.png'
    tmp = open('Img/warn.png','wb+')
    tmp.write(base64.b64decode(warn.img))
    tmp.close()
    warn = 'Img/warn.png'
    pos_x = 100
    pos_y = 300
    size_x = 535
    size_y = 423

class ConvertedSpec():

    back = 'Img/label_back.png'
    pos_x = 975
    pos_y = 300
    size_x = 535
    size_y = 423


class LeftPlayer():

    pos_x = -20
    pos_y = 770
    size_x = 660
    size_y = 100

class RightPlayer():

    pos_x = 860
    pos_y = 770
    size_x = 660
    size_y = 100

class PlayTimeNow():

    pos_x = 182
    pos_y = 40
    size_x = 80
    size_y = 40

class PlayTimeTotal():

    pos_x = 580
    pos_y = 40
    size_x = 80
    size_y = 40

class PlayBar():

    pos_x = 192
    pos_y = 30
    size_x = 450
    size_y = 20

class PlayButton():

    tmp = open('Img/play.png','wb+')
    tmp.write(base64.b64decode(play.img))
    tmp.close()
    play = 'Img/play.png'
    tmp = open('Img/play_unable.png','wb+')
    tmp.write(base64.b64decode(play_unable.img))
    tmp.close()
    play_unable = 'Img/play_unable.png'
    tmp = open('Img/pause.png','wb+')
    tmp.write(base64.b64decode(pause.img))
    tmp.close()
    pause = 'Img/pause.png'
    pos_x = 129
    pos_y = 13
    size_x = 44
    size_y = 50

class ConnectLabel():

    pos_x = 1000
    pos_y = 150
    size_x = 430
    size_y = 60

class RetryButton():

    pos_x = 1460
    pos_y = 200
    size_x = 100
    size_y = 40
