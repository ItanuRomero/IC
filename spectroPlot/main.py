import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from os import listdir, mkdir
import os


def create_spectrum(file_name):
    # sr -> sampling frequency
    file_path = file_name.split('/Music')[1].split('.mp3')[0]
    if os.path.isfile(f'../Spectrum/{file_path}.png'):
        return
    data, fs = librosa.load(file_name, sr=44100)
    plt.figure(figsize=(12, 5))
    processed_data = librosa.amplitude_to_db(np.abs(librosa.stft(data)))
    librosa.display.specshow(processed_data,
                             x_axis='time',
                             y_axis='linear',
                             sr=fs,
                             cmap='CMRmap')
    save_spectrum_image(file_path)
    plt.clf()
    # show_spectrum_image()


def save_spectrum_image(file_name):
    print('Saving ', file_name)
    plt.axis('off')
    plt.savefig(f'../Spectrum/{file_name}.png',
                format='png',
                bbox_inches='tight',
                transparent="True",
                pad_inches=0)


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


all_paths = list()
music_gender_paths = [path for path in listdir('../Music')]
for path in music_gender_paths:
    files_paths = [f'{path}/{file}' for file in listdir(f'../Music/{path}')]
    all_paths.append(files_paths)
for directory in all_paths:
    for music_path in directory:
        try:
            create_spectrum(file_name=f'../Music/{music_path}')
        except FileNotFoundError:
            try:
                create_directory = music_path.split('/')[0]
                print('Creating dir for Spectrum/', create_directory)
                mkdir(f'../Spectrum/{create_directory}')
                create_spectrum(file_name=f'../Music/{music_path}')
            except FileExistsError:
                pass
