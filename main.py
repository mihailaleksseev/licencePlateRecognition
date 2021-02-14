import cv2
import os
from imutils import contours
import pytesseract


# process image
file_names = os.listdir("images/todo/")
file_names.sort()
for file in file_names:
    print(file)
    image = cv2.imread("images/todo/" + file)
    height, width, _ = image.shape
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("images/done/" + file + "_grey.jpg", gray_image)
    image_without_thrash = cv2.threshold(gray_image, 100, 255, cv2.THRESH_BINARY)[1]
    cv2.imwrite("images/done/" + file + "_grey_otsu_100.jpg", image_without_thrash)
    cnts = cv2.findContours(image_without_thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts, _ = contours.sort_contours(cnts[0])

    for c in cnts:
        area = cv2.contourArea(c)
        x, y, w, h = cv2.boundingRect(c)
        # поиск номера по длине контура, значение 5000 нужно реглировать и искать оптимальное
        if area > 5000:
            img = image_without_thrash[y:y+h, x:x+w]
            cv2.imwrite("images/done/" + file + "_licence_plate.jpg", img)
            result = pytesseract.image_to_string(img, lang="rus+eng")
            if len(result) > 7:
                print(area)


    # Нужно эксперементировать и подбирать кодировку под определенные уловия маста получения изображения
    # Также стоит прогонять изображение несколько раз обработанное разными фильтрами
    # image_without_thrash = cv2.threshold(gray_image, 80, 255, cv2.THRESH_BINARY)[1]
    # cv2.imwrite("images/done/" + file + "_grey_otsu_80.jpg", image_without_thrash)
    #
    # image_without_thrash = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)[1]
    # cv2.imwrite("images/done/" + file + "_grey_otsu_127.jpg", image_without_thrash)
    #
    # image_without_thrash = cv2.threshold(gray_image, 140, 255, cv2.THRESH_BINARY)[1]
    # cv2.imwrite("images/done/" + file + "_grey_otsu_140.jpg" + file, image_without_thrash)

