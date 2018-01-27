import pyaudio
import numpy as np
import time


# 暂时将播放器类独立出来，以后可能想办法修改成独立播放线程，使其不影响界面和其他计算，也可能更换其他的播放器库
class MusicPlayer:
    myThread = None

    p = pyaudio.PyAudio()

    sampleRate = 0

    dat = None

    # 用librosa默认的数据格式，32位浮点型数组（np.array)，单通道
    def play(self, musicData, sampleRate):
        self.sampleRate = sampleRate

        self.dat = musicData.astype(np.float32).tostring()
        
        self.playAudio()

    def playAudio(self):
        # PyAudio的媒体流
        # librosa读取的wave文件默认为float32格式，单通道
        stream = self.p.open(format=pyaudio.paFloat32,
                             channels=1, 
                             rate=self.sampleRate,
                            #  stream_callback=self.playCallback,
                             output=True)

        stream.write(self.dat)

        stream.stop_stream()
        stream.close()