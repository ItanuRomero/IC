import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# sr -> frequência de amostragem
file_name = 'cardio.mp3'
data, fs = librosa.load(file_name, sr=44100)
plt.figure(figsize=(12, 5))
D = librosa.amplitude_to_db(np.abs(librosa.stft(data)))
librosa.display.specshow(D, x_axis='time', y_axis='linear', sr=fs, cmap='CMRmap')
plt.xlabel('Time [s]')
plt.ylabel('Frequency [Hz]')
# remove other information
plt.xticks([], [])
plt.yticks([], [])
plt.colorbar(format='%+2.0f dB')
plt.savefig(f'{file_name[:-4]}.png', format='png')
plt.show()
