import librosa
import sounddevice as sd

data, sr = librosa.load('356.wav', sr=None)

sd.play(data)
sd.wait()

print(len(data))

