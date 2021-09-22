import cv2
import csv


def is_empty(filename='results.csv'):
    with open(filename, 'r') as results_csv:
        csv_dict = [row for row in csv.DictReader(results_csv)]
        if len(csv_dict) == 0:
            write_file_head()


def write_file_head():
    with open('results.csv', 'w') as results_csv:
        writer = csv.writer(results_csv)
        writer.writerow(['Names', 'AreEqual', 'CountNonZero', 'GoodMatches', 'Matches'])


def write_results(data=[None, None, None, None, None]):
    with open('results.csv', 'a') as results_csv:
        writer = csv.writer(results_csv)
        writer.writerow(data)


is_empty()
result_data = list()
first_image, second_image = input("First image name: "), input("Second image name: ")
first_image, second_image = f'../Spectrum/eletronic/{first_image}.png', f'../Spectrum/eletronic/{second_image}.png'
result_data.append(f'{first_image} - {second_image}')
first_image, second_image = cv2.imread(first_image), cv2.imread(second_image)

diff = cv2.subtract(first_image, second_image)

cv2.imshow('diferenças encontradas', diff)
cv2.waitKey(1000)
cv2.imwrite('result.png', diff)
b, g, r = cv2.split(diff)
rgb = [
    cv2.countNonZero(r),
    cv2.countNonZero(g),
    cv2.countNonZero(b)
]
if diff.any():
    result_data.append(False)
    result_data.append(rgb)
else:
    result_data.append(True)
    result_data.append(rgb)

# second part. Checking similarities with ORB algorithm
orb = cv2.ORB_create()
keypoint_one, descriptor_one = orb.detectAndCompute(first_image, None)
keypoint_two, descriptor_two = orb.detectAndCompute(second_image, None)

matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
matches = matcher.knnMatch(descriptor_one, descriptor_two, k=2)
good_matches = []
for match, n in matches:
    if match.distance < 0.5 * n.distance:
        good_matches.append([match])
matches_image = cv2.drawMatchesKnn(first_image,
                                   keypoint_one,
                                   second_image,
                                   keypoint_two,
                                   good_matches,
                                   None)
cv2.imshow("matches image", matches_image)
cv2.imwrite('matches_image.png', matches_image)
cv2.waitKey(1000)
result_data.append(len(good_matches))
result_data.append(len(matches))
write_results(result_data)
