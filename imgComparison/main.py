import cv2

# first part. Report rgb from the file
results_file = open('results.txt', 'a')

# first_image, second_image = input("First image name: "), input("First image name: ")
first_image, second_image = 'original.png', 'remix.png'
results_file.write(f'\n{first_image} and image {second_image}\n')
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
    message = f'Images are different:\nRGB countNonZero: {rgb}\n'
else:
    message = 'Images are the same\n'
print(message)

# second part. Checking similarities with ORB algorithm
orb = cv2.ORB_create()
keypoint_one, descriptor_one = orb.detectAndCompute(first_image, None)
keypoint_two, descriptor_two = orb.detectAndCompute(second_image, None)

matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
matches = matcher.knnMatch(descriptor_one, descriptor_two, k=2)
good_matches = []
for match, n in matches:
    if match.distance < 0.7* n.distance:
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
message += f'ORB Algorithm matches: {len(good_matches)}\n'
results_file.write(message)
results_file.close()
