import librosa
import sounddevice as sd
from chord import 三分损益, 正调
import extractPitch
import stoppedNote
from constants import DefaultFreq7

import tkinter
import tkinter.filedialog

QinChords = [0] * 7
Freq7 = DefaultFreq7

wavData = None
sampleRate = 0

tkInstance = None
playPauseBtn = None
freq7Variable = None
isPlaying = False


# 初始化弦数、调弦等
def initialiseQin():
    global QinChords

    QinChords = 正调(DefaultFreq7, 三分损益)


# 设置GUI界面
def initialiseWindow():
    global tkInstance
    global freq7Variable

    tkInstance = tkinter.Tk()

    lb = tkinter.Label(tkInstance, text='选择音频文件')
    lb.pack()
    openBtn = tkinter.Button(tkInstance, text='浏览', command=openFileCommand)
    openBtn.pack()

    lb2 = tkinter.Label(tkInstance, text='设置七弦频率')
    lb2.pack()
    freq7Variable = tkinter.DoubleVar(value=Freq7)
    freq7Entry = tkinter.Entry(tkInstance, textvariable=freq7Variable)
    freq7Entry.pack()
    setQinBtn = tkinter.Button(tkInstance, text='设置', command=setQinCommand)
    setQinBtn.pack()

    global playPauseBtn
    playPauseBtn = tkinter.Button(
        tkInstance, text='播放', command=playOrPauseWavCommand)
    playPauseBtn.pack()

    analyseBtn = tkinter.Button(
        tkInstance, text='分析', command=analyseCommand
    )
    analyseBtn.pack()


def initialise():
    initialiseQin()
    initialiseWindow()


def load(fname):
    global wavData
    global sampleRate

    print('======Loading=====')
    wavData, sampleRate = librosa.load(fname, sr=None)
    print('采样率：', sampleRate)


def setQinCommand():
    global freq7Variable
    global Freq7
    global QinChords

    Freq7 = freq7Variable.get()

    QinChords = 正调(Freq7, 三分损益)


def playOrPauseWavCommand():
    global wavData
    global isPlaying
    global playPauseBtn

    # 切换播放状态（没有暂停功能）
    if isPlaying:
        sd.stop()
        playPauseBtn['text'] = '播放'
        isPlaying = False
    else:
        if not wavData is None:
            sd.play(wavData)
            playPauseBtn['text'] = '停止'
            isPlaying = True


def openFileCommand():
    filename = tkinter.filedialog.askopenfilename(
        filetypes=(("wave files", "*.wav"), ("all files", "*.*")))
    if filename != '':
        load(filename)


def analyseCommand():
    if not wavData is None:
        print('=====Extracting pitch=====')
        pitchData = extractPitch.extract_pitch(wavData, sampleRate)

        print('Pitch extracted!')

        results = stoppedNote.transform(pitchData, QinChords)

        # 保存到"locations.tsv"文件中，每行格式：
        # 时间    频率  一弦有效弦长  一弦音位（徽位，徽分） ... 七弦徽分
        with open('locations.tsv', 'w') as f:
            for item in results:
                ss = ''
                pos = item['chord_positions']
                stops = item['stops']
                for i in range(7):
                    ss += str(pos[i]) + '\t' + str(stops[i]) + '\t'
                line = '{0}\t{1}Hz\t{2}\n'.format(
                    item['timestamp'], item['frequency'], ss)
                f.write(line)


def main():
    initialise()

    tkInstance.mainloop()


if __name__ == '__main__':
    main()
