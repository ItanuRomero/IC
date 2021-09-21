import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def create_spectrum(file_name):
    # sr -> sampling frequency
    data, fs = librosa.load(file_name, sr=44100)
    plt.figure(figsize=(12, 5))
    processed_data = librosa.amplitude_to_db(np.abs(librosa.stft(data)))
    librosa.display.specshow(processed_data, x_axis='time', y_axis='linear', sr=fs, cmap='CMRmap')
    save_spectrum_image(file_name)
    show_spectrum_image()


def save_spectrum_image(file_name):
    plt.axis('off')
    # maybe we can remove all black pixels with opencv
    plt.savefig(f'{file_name[:-4]}.png', format='png', bbox_inches='tight', transparent="True", pad_inches=0)


def show_spectrum_image():
    plt.axis('on')
    plt.xlabel('Time [s]')
    plt.ylabel('Frequency [Hz]')
    plt.xticks([], [])
    plt.yticks([], [])
    plt.colorbar(format='%+2.0f dB')
    plt.show()


def remove_all_black_pixels(file_name):
    img = Image.open(file_name)
    img = img.convert("RGBA")
    datas = img.getdata()
    new_data = []
    for item in datas:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(item)
    img.putdata(new_data)
    img.save(f'{file_name}_without_black_pixels.png')


filename = input('Type file name: ')
create_spectrum(file_name=f'../Music/eletronic/{filename}.mp3')
remove_all_black_pixels(file_name=f'../Music/eletronic/{filename}.png')
