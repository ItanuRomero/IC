import cv2
import csv
from os import listdir

FILENAME = 'results.csv'
RESULTS_HEAD = [
    'FirstImage', 'SecondImage',
    'NonZeroR', 'NonZeroG', 'NonZeroB',
    'Matches0.5', 'Matches0.6', 'Matches0.7',
    'Matches0.8', 'Matches0.9', 'Matches1.0',
    'Matches'
]


def is_empty(filename: str = FILENAME):
    with open(filename, 'r') as results_csv:
        csv_dict = [row for row in csv.DictReader(results_csv)]
        if len(csv_dict) == 0:
            write_file_head()


def write_file_head():
    with open('results.csv', 'w', newline='') as results_in_csv:
        writer = csv.writer(results_in_csv)
        writer.writerow(RESULTS_HEAD)


def write_results(data=RESULTS_HEAD):
    with open('results.csv', 'a', newline='') as results_in_csv:
        writer = csv.writer(results_in_csv)
        writer.writerow(data)


def analyze_and_save_results(first_image: str, second_image: str, flag_show_images=False):
    result_data = []
    names = [
        first_image.split('_')[0].replace('.png', ''),
        second_image.split('_')[0].replace('.png', '')
    ]
    for name in names:
        result_data.append(name)
    first_image, second_image = f'../Spectrum/{first_image}', f'../Spectrum/{second_image}'
    first_image, second_image = cv2.imread(first_image), cv2.imread(second_image)
    # first part. Getting the absolute difference between the files and split by rgb
    absolute_diff = cv2.absdiff(first_image, second_image)
    cv2.imwrite('result_absolute.png', absolute_diff)
    b, g, r = cv2.split(absolute_diff)
    rgb = [
        cv2.countNonZero(r),
        cv2.countNonZero(g),
        cv2.countNonZero(b)
    ]
    for color in rgb:
        result_data.append(color)

    # second part. Checking similarities with ORB algorithm
    orb = cv2.ORB_create()
    keypoint_one, descriptor_one = orb.detectAndCompute(first_image, None)
    keypoint_two, descriptor_two = orb.detectAndCompute(second_image, None)

    matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = matcher.knnMatch(descriptor_one, descriptor_two, k=2)

    good_matches_list = []
    for distance in range(5, 11):
        good_matches = []
        for match, n in matches:
            if match.distance < (distance / 10) * n.distance:
                good_matches.append([match])
        if flag_show_images:
            matches_image = cv2.drawMatchesKnn(first_image,
                                               keypoint_one,
                                               second_image,
                                               keypoint_two,
                                               good_matches,
                                               None)
            cv2.imwrite(f'matches_image_{distance}.png', matches_image)
        good_matches_list.append(len(good_matches))
    for matches_distance in good_matches_list:
        result_data.append(matches_distance)
    result_data.append(len(matches))
    write_results(result_data)


try:
    is_empty()
except FileNotFoundError:
    with open(FILENAME, 'x') as _:
        print("File hasn't been created, until now.")
    is_empty()

all_paths = []
all_comparisons = []
music_gender_paths = [path for path in listdir('../Spectrum')]
for path in music_gender_paths:
    files_paths = [f'{path}/{file}' for file in listdir(f'../Spectrum/{path}')]
    all_paths.append(files_paths)
for directory in all_paths:
    for second_directory in all_paths:
        for first_image_path in directory:
            for second_image_path in second_directory:
                if f'{first_image_path} and {second_image_path}' not in all_comparisons \
                        and f'{second_image_path} and {first_image_path}' not in all_comparisons \
                        and first_image_path != second_image_path:
                    try:
                        analyze_and_save_results(first_image_path, second_image_path)
                    except Exception as err:
                        print(err)
                        print(first_image_path, second_image_path)
                    all_comparisons.append(f'{first_image_path} and {second_image_path}')
