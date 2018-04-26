# 客户端
请在满足要求的Window X64设备上安装试用。具体信息请参阅我们相关的 __[帮助文档](https://github.com/Pzoom522/MusiCoder/wiki/1-Client)__

近期将发布面向Mac OSX的版本

## 源代码说明：
- 实际代码为```client.py``` ```design.py``` ```gui.py``` ```interface.py``` ```player.py``` ```Qplayer.py``` ```QSegmentSelector.py```，其它均为图片文件（为了便于打包）
- 为了在调用ffmpeg进行音量平衡等操作时不出现命令行窗口，我们对 _pydub_ 库函数进行了修改，具体位置为```audio_segment.py```的[第512行](https://github.com/Pzoom522/MusiCoder/blob/master/client/lib_hack/pydub/audio_segment.py#L512)和[第678行](https://github.com/Pzoom522/MusiCoder/blob/master/client/lib_hack/pydub/audio_segment.py#L678)。
