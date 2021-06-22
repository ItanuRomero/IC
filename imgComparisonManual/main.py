import numpy as np
import matplotlib.pyplot as plt
img = plt.imread('original.png')
plt.xticks([], [])
plt.yticks([], [])
plt.imshow(img)
plt.show()

for counter in range(0, 3):
    img_separated = img.copy()
    if counter == 0:
        # taking red only
        img_separated[:, :, [1, 2]] = 0
    elif counter == 1:
        # green only
        img_separated[:, :, [0, 2]] = 0
    else:
        # blue only
        img_separated[:, :, [0, 1]] = 0
    plt.imshow(img_separated)
    plt.xticks([], [])
    plt.yticks([], [])
    plt.show()


