import cv2  # импорт модуля cv2
from time import time

cap = cv2.VideoCapture(0)  # видео поток с камеры

h, w = 720, 1280
cap.set(3, w)  # установка размера окна
cap.set(4, h)

ret, frame1 = cap.read()
ret, frame2 = cap.read()
ret, frame3 = cap.read()
ret, frame4 = cap.read()

loop_time = time()
while cap.isOpened():  # метод isOpened() выводит статус видеопотока

    diff1 = cv2.absdiff(frame1,
                        frame2)  # нахождение разницы двух кадров, которая проявляется лишь при изменении одного из них, т.е. с этого момента наша программа реагирует на любое движение.

    diff2 = cv2.absdiff(frame2,
                        frame3)

    diff3 = cv2.absdiff(frame3,
                        frame4)

    res_diff = cv2.absdiff(diff1, diff2, diff3)

    gray = cv2.cvtColor(diff3, cv2.COLOR_BGR2GRAY)  # перевод кадров в черно-белую градацию

    blur = cv2.GaussianBlur(gray, (5, 5), 0)  # фильтрация лишних контуров

    _, thresh = cv2.threshold(blur, 20, 180, cv2.THRESH_BINARY)  # метод для выделения кромки объекта белым цветом

    dilated = cv2.dilate(thresh, None,
                         iterations=10)  # данный метод противоположен методу erosion(), т.е. эрозии объекта, и расширяет выделенную на предыдущем этапе область

    сontours, _ = cv2.findContours(dilated, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)  # нахождение массива контурных точек

    for contour in сontours:
        (x, y, w, h) = cv2.boundingRect(
            contour)  # преобразование массива из предыдущего этапа в кортеж из четырех координат

        # метод contourArea() по заданным contSSour точкам(кортежу), вычисляет площадь зафиксированного объекта в каждый момент времени
        print(cv2.contourArea(contour))

        if cv2.contourArea(contour) < 10000 or cv2.contourArea(contour) > 600000:  # условие при котором площадь выделенного объекта меньше N px
            continue
        # cv2.rectangle(frame1, (x, y), (x + w, y + h), (255, 0, 0), 2)  # получение прямоугольника из точек кортежа
        cv2.putText(frame1, "Motion - detected", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                    cv2.LINE_AA)  # вставляем текст

    print(f'FPS {(1 / (time() - loop_time))}')
    loop_time = time()

    cv2.drawContours(frame1, сontours, -1, (0, 255, 0), 2)
    cv2.imshow("Video", frame1)

    frame1 = frame2
    frame2 = frame3
    frame3 = frame4
    ret, frame4 = cap.read()

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
