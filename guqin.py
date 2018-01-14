import bisect
from constants import MTable, DTable

from chord import 三分损益, 正调


class GuQin:
    Chords = [0, 0, 0, 0, 0, 0, 0]

    def __init__(self):
        self.tune(82.5, 正调, 三分损益) # 默认设置为标准音高下的七弦频率

    def tune(self, 七弦散音, 琴调, 调弦法):
        self.Chords = 琴调(七弦散音, 调弦法)
    
    # 根据频率与弦序计算有效弦长，这里的弦序为0-6
    def activeLength(self, frequency, chordIndex):
        return self.Chords[chordIndex] / frequency

    # 将有效弦长转换为按音位
    # 返回(徽位，徽分)二元组，散音为14徽0分，不能弹出时记为15徽0分
    def activeLengthToStops(self, length):
        if length > 1:
            # 有效弦长大于1时，这个音不在这根弦上弹出，记为15徽0分
            return (15.0, 0.0)
    
        # 徽位：二分查找小于等于length的最大徽值M
        x = bisect.bisect(MTable, length) - 1
        # 计算对应徽分
        y = (pos - MTable[x]) / DTable[x]
        
        return (x, y * 10)

    # 计算某个频率的音在某条弦上的音位
    def pitchStops(self, frequency, chordIndex):
        return self.activeLengthToStops(self.activeLength(frequency, chordIndex))
