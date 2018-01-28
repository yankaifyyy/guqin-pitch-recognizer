from constants import MTable


def createScale(from_domain, to_range):
    k = (to_range[1] - to_range[0]) / (from_domain[1] - from_domain[0])

    def scaleFunc(val):
        return k * (val - from_domain[0]) + to_range[0]

    return scaleFunc


BadgeNames = ['岳山', '一', '二', '三', '四', '五', '六',
              '七', '八', '九', '十', '十一', '十二', '十三', '龙龈']


# 画图主程序
class FingerTrajPainter:
    LeftOffset = 70
    TopOffset = 50
    QinHeight = 100
    AxesTickSize = 15

    ChordLength = 900

    CurveHeight = 800
    CurvePadBottom = 30

    qin = None

    pitchCache = None
    chordIndexCache = -1
    timeExtent = None

    playingIndicator = None

    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height

    def updateQin(self, guqin):
        self.qin = guqin

        # 重新调弦后需要重绘
        self.canvas.delete('all')
        self.drawQin()
        self.drawAxes()

        if not self.pitchCache is None:
            self.drawCurve(self.pitchCache, self.chordIndexCache)

    def drawQin(self):
        gap = self.QinHeight / 7.0
        xoffset = self.LeftOffset
        yoffset = self.TopOffset
        chordLength = self.ChordLength

        xScale = createScale((0, 1), (chordLength + xoffset, xoffset))

        # 十五个”徽位“
        for i, badge in enumerate(BadgeNames):
            x = xScale(MTable[i])
            y = 0.5 * self.TopOffset
            radius = 7 * (1 + (1 - abs(i - 7) / 7))

            self.canvas.create_oval(
                x - radius, y - radius, x + radius, y + radius, fill='goldenrod', outline='')
            self.canvas.create_text(x, y, text=badge)

        # 七根弦
        for i, hz in enumerate(self.qin.Chords):
            y = i * gap + yoffset
            self.canvas.create_line(
                xoffset, y, xoffset + chordLength, y, fill='darkgrey')

            text = str(round(hz, 2)) + 'Hz'
            self.canvas.create_text(
                xoffset - 5, y, anchor='e', text=text)

    def drawAxes(self):
        xoffset = self.LeftOffset
        yoffset = self.TopOffset + self.QinHeight
        tickSize = self.AxesTickSize

        chordLength = self.ChordLength

        # 水平坐标轴
        self.canvas.create_line(xoffset, yoffset + tickSize,
                                xoffset + chordLength, yoffset + tickSize, fill='green')

        # 十五个水平刻度
        for i, pos in enumerate(MTable):
            x = (1 - MTable[i]) * chordLength + xoffset
            self.canvas.create_line(
                x, yoffset, x, yoffset + tickSize, fill='green', width=2)

        # 垂直坐标轴（时间轴）
        self.canvas.create_line(
            xoffset, yoffset + tickSize, xoffset, 10000, fill='green')

    def drawCurve(self, timePitchData, chordIndex):
        # 把pitch数据保留下来，万一重新调弦，重画需要用到
        self.pitchCache = timePitchData
        self.chordIndexCache = chordIndex

        if chordIndex == -1:
            # 异常情况，不会出现的
            return

        # 先清理掉所有标签为'curve-dot'的点
        self.canvas.delete('curve-dot')

        xoffset = self.LeftOffset
        yoffset = self.TopOffset + self.QinHeight + self.AxesTickSize

        maxHeight = self.CurveHeight - yoffset - self.CurvePadBottom

        chordLength = self.ChordLength

        # 画出来的圆点的大小
        radius = 1

        # 时间区间
        maxTime = max(timePitchData, key=lambda v: v[0])[0]
        self.timeExtent = (0, maxTime)

        # x坐标据有效弦长计算得出
        xScale = createScale((0, 1), (xoffset + chordLength, xoffset))
        # y坐标据时间计算得出
        yScale = createScale(self.timeExtent, (yoffset, yoffset + maxHeight))

        for tm, pitch in timePitchData:
            # 只画有频率的采样点
            if pitch > 0:
                pos = self.qin.activeLength(pitch, chordIndex)
                # 只画能弹的音符
                if pos > 0 and pos <= 1:
                    x = xScale(pos)
                    y = yScale(tm)
                    self.canvas.create_oval(
                        x - radius, y - radius, x + radius, y + radius, fill='#555', outline='', tags='curve-dot')
