# MusiCoder-服务器端
## 数据流与架构
![img](https://github.com/Pzoom522/MusiCoder/blob/master/img/mttn.png?raw=true)
## 配置及环境要求
### 基本配置
- Ubuntu 12.04 LTS 及以上
- 内存4G及以上
- Python 3 环境

### 所需主要依赖
- 科学计算与数据可视化：[matplotlib](https://matplotlib.org/)+[scipy](https://scipy.github.io)(numpy/pylab/etc)
- 图形图像：[PIL.Image](https://pillow.readthedocs.io)
- 音频处理：[librosa](https://librosa.github.io)+[pydub](https://github.com/jiaaro/pydub/)+[ffmpeg](https://ffmpeg.org)(配置为环境变量)

### 模型文件
__请分别解压并放置在 _converter/models_ 下__

[未来感音效](https://github.com/Pzoom522/MusiCoder/blob/master/audio/future_10.mp3?raw=true)|[水流音效](https://github.com/Pzoom522/MusiCoder/blob/master/audio/water_10.mp3?raw=true)|[镭射音效](https://github.com/Pzoom522/MusiCoder/blob/master/audio/laser_10.mp3?raw=true)
:-: | :-: | :-:
[future.ckpt](https://www.dropbox.com/s/6xhg6ipsn0fq7yy/future.ckpt.zip?dl=0)|[water.ckpt](https://www.dropbox.com/s/y2rstqwq21xph99/water.ckpt.zip?dl=0)|[laser.ckpt](https://www.dropbox.com/s/wln82c3c6ibhbfx/laser.ckpt.zip?dl=0)
![img](https://github.com/Pzoom522/MusiCoder/blob/master/img/future.jpg?raw=true)|![img](https://github.com/Pzoom522/MusiCoder/blob/master/img/water.jpg?raw=true)| ![img](https://github.com/Pzoom522/MusiCoder/blob/master/img/laser.jpg?raw=true)

## 运行
 1. 开放端口 ___[port]___
 2. 执行命令，运行程序（后台静默模式）```nohup python3 server.py [port] &```

## 性能预估
在配置为双核Intel® Xeon® CPU E5-26xx v4 CPU和4G内存的机子上，极限负载为同时承受约20个客户端的峰值任务。
在正常连接情况下，服务器端程序应当可以对各类情况做出正确反馈。但是在客户端中途掉线时，可能会导致 ___temp___ 目录下出现残留文件，建议定时进行清除。
