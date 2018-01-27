# import sounddevice as sd
from application import Application
from constants import DefaultFreq7, MTable

from canvasPainter import FingerTrajPainter
from musicPlayer import MusicPlayer

import tkinter
import tkinter.messagebox
import tkinter.filedialog
from tkinter import ttk


# 程序界面管理
class GUI:
    tk = tkinter.Tk()

    player = MusicPlayer()

    def __init__(self, app):
        self.app = app

        self.initializeControls()
        self.initializeCanvas()

        self.retuneCommand()

    def initializeControls(self):
        ctrlFrame = tkinter.Frame(self.tk)
        ctrlFrame.pack()

        self.openBtn = tkinter.Button(
            ctrlFrame, text='打开', command=self.openFileCommand)
        self.openBtn.pack(side=tkinter.LEFT)

        self.playPauseBtn = tkinter.Button(
            ctrlFrame, text='播放', command=self.playAndStopWaveCommand)
        self.playPauseBtn.pack(side=tkinter.LEFT)

        freqFrame = tkinter.Frame(self.tk)
        freqFrame.pack()
        lb = tkinter.Label(freqFrame, text='七弦频率')
        lb.pack(side=tkinter.LEFT)

        self.freq7Variable = tkinter.DoubleVar(value=DefaultFreq7)
        self.freq7Entry = tkinter.Entry(
            freqFrame, textvariable=self.freq7Variable)
        self.freq7Entry.pack(side=tkinter.LEFT)

        self.retuneBtn = tkinter.Button(
            freqFrame, text='调弦设置', command=self.retuneCommand)
        self.retuneBtn.pack(side=tkinter.LEFT)

        chordFrame = tkinter.Frame(self.tk)
        chordFrame.pack()
        lb2 = tkinter.Label(chordFrame, text='当前使用的弦：')
        lb2.pack(side=tkinter.LEFT)
        possibleChords = ('一', '二', '三', '四', '五', '六', '七')
        self.chordList = ttk.Combobox(
            chordFrame, values=possibleChords, state='readonly')
        self.chordList.current(6)
        self.chordList.pack(side=tkinter.LEFT)
        self.chordList.bind('<<ComboboxSelected>>', self.chordChanged)

        self.analyzeBtn = tkinter.Button(
            chordFrame, text='分析指迹', command=self.analyzeCommand)
        self.analyzeBtn.pack()

    # 图形画在Canvas上
    def initializeCanvas(self):
        width = 1000
        height = 800

        self.canvas = tkinter.Canvas(
            self.tk, width=width, height=height, bg='white')
        self.canvas.pack(padx=50, pady=0)

        self.painter = FingerTrajPainter(self.canvas, width, height)
        self.painter.updateQin(self.app.qin)

        self.drawAxes()

    def drawAxes(self):
        self.painter.drawAxes()

    def createScale(self, domain, rg):
        k = (rg[1] - rg[0]) / (domain[1] - domain[0])

        def scaleFunc(val):
            return k * (val - domain[0]) + rg[0]

        return scaleFunc

    def run(self):
        self.tk.mainloop()

    def openFileCommand(self):
        filename = tkinter.filedialog.askopenfilename(
            filetypes=(('音频文件', '*.wav'), ('All files', '*.*'))
        )

        if filename != '':
            try:
                self.app.load(filename)

                info = '读取音频文件 ' + filename + ' 成功\n采样率=' + \
                    str(self.app.sampleRate) + 'Hz。'
                tkinter.messagebox.showinfo(title='读取成功！', message=info)
            except:
                tkinter.messagebox.showerror(
                    title='读取失败！', message='加载音频文件失败！')

    def playAndStopWaveCommand(self):
        if not self.app.waveData is None:
            self.player.play(self.app.waveData, self.app.sampleRate)

    def retuneCommand(self):
        currentFrequency7 = self.app.currentFrequency7()
        try:
            freq7 = self.freq7Variable.get()
            self.app.retune(freq7)
        except:
            self.app.retune(currentFrequency7)
            tkinter.messagebox.showerror(title='调弦失败！', message='不合理的七弦散音频率！')

        # 重新绘制图形
        self.painter.updateQin(self.app.qin)

    def chordChanged(self, event):
        # 更换弦时重绘指迹图
        if not self.app.pitchData is None:
            self.painter.drawCurve(
                self.app.pitchData, self.chordList.current())

    def analyzeCommand(self):
        self.app.analyze()

        if not self.app.pitchData is None:
            self.painter.drawCurve(
                self.app.pitchData, self.chordList.current())


def main():
    app = Application()
    gui = GUI(app)

    gui.run()


if __name__ == '__main__':
    main()
