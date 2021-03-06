import numpy as np
import matplotlib.pyplot as plt
import cv2
img_name = 'remix'
# showing the original image
img = plt.imread(f'{img_name}.png')
plt.xticks([], [])
plt.yticks([], [])
plt.imshow(img)
plt.show()
# showing only yellow lines
try_yellow = cv2.imread(f'{img_name}.png')
img_hsv = cv2.cvtColor(try_yellow, cv2.COLOR_BGR2HSV)
# filter to white and yellow
white = np.asarray([0, 0, 255])
yellow = np.asarray([30, 255, 255])

mask = cv2.inRange(img_hsv, white, yellow)
plt.imshow(mask, cmap='gray')
plt.savefig(f'yellow_{img_name}.png')
plt.show()

for counter in range(0, 3):
    img_separated = img.copy()
    if counter == 0:
        # taking red only
        img_separated[:, :, [1, 2]] = 0
        plt.imshow(img_separated)
        plt.xticks([], [])
        plt.yticks([], [])
    elif counter == 1:
        # green only
        img_separated[:, :, [0, 2]] = 0
        plt.imshow(img_separated, cmap='gray')
        plt.xticks([], [])
        plt.yticks([], [])
        plt.savefig(f'green_{img_name}.png')
    else:
        # blue only
        img_separated[:, :, [0, 1]] = 0
        plt.imshow(img_separated)
        plt.xticks([], [])
        plt.yticks([], [])
    plt.show()
