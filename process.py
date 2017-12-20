FileName = '356.csv' # 从Sonic Visualiser导出的数据文件
Freq7 = 136 # 7弦散音，人工确定

MTable = 徽值表 = [
    0, # 以岳山为0徽
    1.0 / 8, 
    1.0 / 6, 
    1.0 / 5,
    1.0 / 4, 
    1.0 / 3, 
    2.0 / 5, 
    1.0 / 2, 
    3.0 / 5, 
    2.0 / 3, 
    3.0 / 4, 
    4.0 / 5, 
    5.0 / 6, 
    7.0 / 8, 
    1.0 # 以龙龈为14徽
]
DTable = 徽距表 = [
    1.0 / 8,
    1.0 / 24,
    1.0 / 30,
    1.0 / 20,
    1.0 / 12,
    1.0 / 15,
    1.0 / 10,
    1.0 / 10,
    1.0 / 15,
    1.0 / 12,
    1.0 / 20,
    1.0 / 30,
    1.0 / 24,
    1.0 / 8,
    1.0
]

# 使用正调定弦5612356，计算7根弦的散音频率（正调定弦5612356）
def 正调定弦(七弦散音频率):
    律数 = {
        '宫': 81.0,
        '商': 72.0,
        '角': 64.0,
        '徵': 54.0,
        '羽': 48.0
    }

    羽 = 七弦散音频率
    宫 = 羽 * 律数['羽'] / 律数['宫'] 
    商 = 羽 * 律数['羽'] / 律数['商'] 
    角 = 羽 * 律数['羽'] / 律数['角'] 
    徵 = 羽 * 律数['羽'] / 律数['徵'] 
    下徵 = 0.5 * 徵
    下羽 = 0.5 * 羽

    # 下标从0开始，0代表一弦，依次类推，6代表七弦
    return [下徵, 下羽, 宫, 商, 角, 徵, 羽]

# 读取Sonic Visualiser导出的音高曲线数据
def readSonicFileCSV(filename):
    with open(filename) as f:
        lines = [tuple(map(float, l.strip().split(','))) for l in f]
    return lines

# 过滤负频率
def filterOutNegFreqs(vals):
    results = []
    for v in vals:
        if v[1] > 0:
            results.append(v)
        else:
            results.append((v[0], 0))
    return results

# 将频率依据当前散音频率转换为有效弦长
def freqToChordPosition(freq, chord_base):
    return chord_base / freq

import bisect
# 将有效弦长转换为按音音位
# 返回二元组，第一项为徽位（不能演奏的音返回15徽0分），第二项为徽分
def chordPositionToStops(pos):
    if pos > 1:
        # 有效弦长大于1时，这个音不可能在这根弦上弹出，记为15徽0分
        return (15.0, 0.0)
    
    # 徽位：二分查找小于等于pos的最大徽值M
    x = bisect.bisect(MTable, pos) - 1
    # 计算对应徽分
    y = (pos - MTable[x]) / DTable[x]
    return (x, y * 10)

def main():
    # 初始化各弦频率，使用正调定弦
    Chords = 正调定弦(Freq7)

    # 读取文件名为FileName的音高数据文件
    data = readSonicFileCSV(FileName)
    # 将音高曲线中的负频率过滤为0
    data = filterOutNegFreqs(data)

    # result 结构：
    # { 
    #    timestamp: 时间
    #    frequency: 频率
    #    chord_positions: 长度为7的数组，其内容为每条弦上可能的有效弦长
    #    stops: 长度为7的二元组，每个二元组的首项为按音的徽，末项为分
    # }
    results = []
    # 对每一行音高数据（存储为"时间 频率"格式），分别计算出它在七根弦上演奏时的有效弦长和音位
    for time, freq in data:
        pos = [0] * 7
        if freq > 0:
            # 分别基于7根弦的散音频率，求出该音在该弦上弹奏时，有效弦长为多少（全弦为1）
            pos = [freqToChordPosition(freq, Chords[i]) for i in range(7)]
    
        # 将7根弦上的有效弦长转为音位存储
        stops = list(map(chordPositionToStops, pos))
        results.append({
            'timestamp': time, 
            'frequency': freq, 
            'chord_positions': pos,
            'stops': stops
            })

    # 保存到"position.tsv"文件中，每行格式：
    # 时间    频率  一弦有效弦长  一弦音位（徽位，徽分） ... 七弦徽分
    with open('position.tsv', 'w') as f:
        for item in results:
            ss = ''
            pos = item['chord_positions']
            stops = item['stops']
            for i in range(7):
                ss += str(pos[i]) + '\t' + str(stops[i]) + '\t'
            line = '{0}\t{1}Hz\t{2}\n'.format(item['timestamp'], item['frequency'], ss)
            f.write(line)

if __name__ == '__main__':
    main()