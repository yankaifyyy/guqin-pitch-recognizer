import bisect
from constants import MTable, DTable


# 将频率依据当前散音频率转换为有效弦长
def freq_to_active_length(freq, chord_base):
    return chord_base / freq


# 将有效弦长转换为按音音位
# 返回二元组，第一项为徽位（不能演奏的音返回15徽0分），第二项为徽分
def active_length_to_stops(pos):
    if pos > 1:
        # 有效弦长大于1时，这个音不可能在这根弦上弹出，记为15徽0分
        return (15.0, 0.0)

    # 徽位：二分查找小于等于pos的最大徽值M
    x = bisect.bisect(MTable, pos) - 1
    # 计算对应徽分
    y = (pos - MTable[x]) / DTable[x]
    return (x, y * 10)


# 将时间-音高序列转换时间-音高&音位序列
# { 
#    timestamp: 时间
#    frequency: 频率
#    chord_positions: 长度为7的数组，其内容为每条弦上可能的有效弦长
#    stops: 长度为7的二元组，每个二元组的首项为按音的徽，末项为分
# }
def transform(data, Chords):
    results = []
    # 对每一行音高数据（存储为"时间 频率"格式），分别计算出它在七根弦上演奏时的有效弦长和音位
    for time, freq in data:
        pos = [0] * 7
        if freq > 0:
            # 分别基于7根弦的散音频率，求出该音在该弦上弹奏时，有效弦长为多少（全弦为1）
            pos = [freq_to_active_length(freq, Chords[i]) for i in range(7)]

        # 将7根弦上的有效弦长转为音位存储
        stops = list(map(active_length_to_stops, pos))
        results.append({
            'timestamp': time,
            'frequency': freq,
            'chord_positions': pos,
            'stops': stops
        })
    return results
