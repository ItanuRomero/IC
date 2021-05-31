import cv2

first_image, second_image = input("First image name: "), input("First image name: ")
first_image, second_image = cv2.imread(first_image), cv2.imread(second_image)
diff = cv2.subtract(first_image, second_image)
if diff.any():
    print("As imagens são diferentes")
else:
    print("As imagens são iguais")