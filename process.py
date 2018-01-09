import librosa
import sounddevice as sd
from chord import 三分损益, 正调
import extractPitch
import stoppedNote
from constants import FileName, DefaultFreq7


def main():
    print('=====Configuring=====')
    print('文件: ', FileName)
    print('调弦：', '三分损益法-正调定弦')

    # 初始化各弦频率，正调定弦，基于三分损益
    Chords = 正调(DefaultFreq7, 三分损益)

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
    pitchData = extractPitch.extract_pitch(wavData, sampleRate)

    print('Pitch extracted!')

    results = stoppedNote.transform(pitchData, Chords)

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
