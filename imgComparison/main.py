import cv2
import csv


def is_empty(filename='results.csv'):
    with open(filename, 'r') as results_csv:
        csv_dict = [row for row in csv.DictReader(results_csv)]
        if len(csv_dict) == 0:
            write_file_head()


def write_file_head():
    with open('results.csv', 'w', newline='') as results_csv:
        writer = csv.writer(results_csv)
        writer.writerow(['Names', 'AreEqual', 'CountNonZero',
                         'CountNonZeroReverse', 'CountNonZeroAbsolute', 'GoodMatchesDistance0.5To1', 'Matches'])


def write_results(data=[None, None, None, None, None]):
    with open('results.csv', 'a', newline='') as results_csv:
        writer = csv.writer(results_csv)
        writer.writerow(data)


def analyze_and_save_results(first_image_path, second_image_path):
    result_data = list()
    first_image, second_image = f'../Spectrum/{first_image_path}', f'../Spectrum/{second_image_path}'
    result_data.append(f'{first_image.split("Spectrum/")[-1]} - {second_image.split("Spectrum/")[-1]}')
    first_image, second_image = cv2.imread(first_image), cv2.imread(second_image)

    diff = cv2.subtract(first_image, second_image)
    diff_reverse = cv2.subtract(second_image, first_image)
    diff_absolute = cv2.absdiff(first_image, second_image)

    cv2.imshow('diferenças encontradas', diff)
    cv2.waitKey(1000)
    cv2.imwrite('result.png', diff)
    cv2.imwrite('result_reverse.png', diff_reverse)
    cv2.imwrite('result_absolute.png', diff_absolute)

    if diff.any():
        result_data.append(False)
    else:
        result_data.append(True)
    diffs = [diff, diff_reverse, diff_absolute]
    for d in diffs:
        b, g, r = cv2.split(d)
        rgb = [
            cv2.countNonZero(r),
            cv2.countNonZero(g),
            cv2.countNonZero(b)
        ]
        result_data.append(rgb)

    # second part. Checking similarities with ORB algorithm
    orb = cv2.ORB_create()
    keypoint_one, descriptor_one = orb.detectAndCompute(first_image, None)
    keypoint_two, descriptor_two = orb.detectAndCompute(second_image, None)

    matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = matcher.knnMatch(descriptor_one, descriptor_two, k=2)
    good_matches_list = list()
    for distance in range(5, 11):
        good_matches = []
        for match, n in matches:
            if match.distance < (distance / 10) * n.distance:
                good_matches.append([match])
        matches_image = cv2.drawMatchesKnn(first_image,
                                           keypoint_one,
                                           second_image,
                                           keypoint_two,
                                           good_matches,
                                           None)
        cv2.imshow("matches image", matches_image)
        cv2.imwrite(f'matches_image_{distance}.png', matches_image)
        cv2.waitKey(1000)
        good_matches_list.append(len(good_matches))
    result_data.append(good_matches_list)
    result_data.append(len(matches))
    write_results(result_data)


is_empty()
from os import listdir
from os.path import isfile, join
import numpy

all_paths = list()
music_gender_paths = [path for path in listdir('../Spectrum')]
for path in music_gender_paths:
    files_paths = [f'{path}/{file}' for file in listdir(f'../Spectrum/{path}')]
    all_paths.append(files_paths)
for directory in all_paths:
    for other_directory in all_paths:
        for first_image in directory:
            for second_image in other_directory:
                if first_image.split('/')[0] != second_image.split('/')[0]:
                    print(first_image, second_image)
                    try:
                        analyze_and_save_results(first_image, second_image)
                    except Exception as err:
                        print(err)
