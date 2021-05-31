import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# sr -> frequência de amostragem
data, fs = librosa.load('cardio.wav', sr=44100)
plt.figure(figsize=(12, 5))
D = librosa.amplitude_to_db(np.abs(librosa.stft(data)))
librosa.display.specshow(D, x_axis='time', y_axis='linear', sr=fs, cmap='CMRmap')
plt.xlabel('Time [s]')
plt.ylabel('Frequency [Hz]')
plt.colorbar(format='%+2.0f dB')
plt.show()
