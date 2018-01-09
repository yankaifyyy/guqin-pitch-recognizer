import vamp
import numpy as np

# melodia plugin参数列表：
#   minfqr: The minimum frequency allowed for the melody([55.0, 1760.0]Hz, default: 55.0Hz).
#   maxfqr: The maximum frequency allowed for the melody([55.0, 1760.0]Hz, default: 1760.0Hz).
#   voicing: Determine the tolerance of the voicing filter. Higher values mean more tolerance([-2.6, 3.0], default: 0.2, step: 0.01).
#   minpeaksalience: For monophonic recordings only. Increase this value to filter out background noise. Always set to 0 for polyphonic recordings! ([0.0, 100.0], default: 0.0, step: 1.0).


def audio_to_pitch_melodia(wav_data, fs=44100, minfqr=55.0, maxfqr=1760.0, voicing=0.2, minpeaksalience=0.0):
    # 用代码调用mtg-melodia时只能使用默认的block=2048，step=128

    params = dict(minfqr=minfqr, maxfqr=maxfqr, voicing=voicing,
                  minpeaksalience=minpeaksalience)
    melody = vamp.collect(wav_data, fs, 'mtg-melodia:melodia', parameters=params)

    timestep = melody['vector'][0].to_float()
    pitch = melody['vector'][1]
    
    # 采样时间的起点是第8个timestep
    starttime = timestep * 8

    # 列表：(时间，频率)
    result = []
    for i, p in enumerate(pitch):
        result.append((starttime + i * timestep, p))

    return result
