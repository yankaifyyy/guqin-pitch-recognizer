from librosa import load as rosaload

import extractPitch

from chord import 三分损益, 正调
from guqin import GuQin


# 程序逻辑管理
class Application:
    qin = GuQin()

    waveData = None
    sampleRate = 0

    pitchData = None

    def load(self, filename):
        self.waveData, self.sampleRate = rosaload(filename, sr=None, res_type='scipy')

    def retune(self, 七弦散音, 琴调=正调, 调弦法=三分损益):
        self.qin.tune(七弦散音, 琴调, 调弦法)

    def currentFrequency7(self):
        return self.qin.Chords[6]

    def analyze(self):
        if not self.waveData is None:
            self.pitchData = extractPitch.extract_pitch(
                self.waveData, self.sampleRate)
