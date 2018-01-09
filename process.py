import bisect
import librosa
import sounddevice as sd
from chord import 三分损益, 正调
from extractPitch import audio_to_pitch_melodia
from constants import MTable, DTable

FileName = '356.wav'  # 从Sonic Visualiser导出的数据文件
Freq7 = 136  # 7弦散音，人工确定


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
    print('=====Configuring=====')
    print('文件: ', FileName)
    print('调弦：', '三分损益法-正调定弦')

    # 初始化各弦频率，正调定弦，基于三分损益
    Chords = 正调(Freq7, 三分损益)

    print('======Loading=====')
    wavData, sampleRate = librosa.load(FileName, sr=None)
    print('采样率：', sampleRate)

    print('\nPlayback? (yY/nN, default: n): n')
    ch = input()
    if ch == 'y' or ch == 'Y':
        sd.play(wavData)
        sd.wait()
        print('Played!')

    
    print('=====Extracting pitch=====')
    # 调用Melodia提取音高
    pitchData = audio_to_pitch_melodia(wavData, sampleRate)
    
    # 将音高曲线中的负频率过滤为0
    data = filterOutNegFreqs(pitchData)

    print('Pitch extracted!')

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

    # 保存到"locations.tsv"文件中，每行格式：
    # 时间    频率  一弦有效弦长  一弦音位（徽位，徽分） ... 七弦徽分
    with open('locations.tsv', 'w') as f:
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
