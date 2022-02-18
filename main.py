import cv2                              # библиотека opencv (получение и обработка изображения)
import mediapipe as mp                  # библиотека mediapipe (распознавание рук)
import json         
import webbrowser

camera = cv2.VideoCapture(0)            # получаем изображение с камеры (0 - порядковый номер камеры в системе)
mpHands = mp.solutions.hands            # подключаем раздел распознавания рук
hands = mpHands.Hands()                 # создаем объект класса "руки"
mpDraw = mp.solutions.drawing_utils     # подключаем инструменты для рисования


import LoadPoses

POSES = LoadPoses.GetAllPos()

p = [0 for i in range(21)]              # создаем массив из 21 ячейки для хранения высоты каждой точки
finger = [0 for i in range(5)]          # создаем массив из 5 ячеек для хранения положения каждого пальца

# функция, возвращающая расстояние по модулю (без знака)
def distance(x1,y1, x2,y2):

    return abs(((x1 - x2)+(y1 - y2))**0.5)


isOpen = False
def Openvideo1():
    global isOpen
    if not isOpen:
        webbrowser.open("https://youtu.be/Q-nFYbjYBJ8?t=9")
        isOpen = True

while True:
    good, img = camera.read()                                   # получаем один кадр из видеопотока
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)               # преобразуем кадр в RGB

    results = hands.process(imgRGB)                             # получаем результат распознавания
    if results.multi_hand_landmarks:                            # если обнаружили точки руки
        for handLms in results.multi_hand_landmarks:            # получаем координаты каждой точки

            # при помощи инструмента рисования проводим линии между точками
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)



            DataDistation = {}


            # работаем с каждой точкой по отдельности
            # создаем список от 0 до 21 с координатами точек
            for id, point in enumerate(handLms.landmark):
                # получаем размеры изображения с камеры и масштабируем
                width, height, color = img.shape
                width, height = int(point.x * height), int(point.y * width)

                p[id] = height           # заполняем массив высотой каждой точки



                if id in [0,4,8,12,16,20]:              # выбираем нужную точку
                    # рисуем нужного цвета кружок вокруг выбранной точки
                    cv2.circle(img, (width, height), 15, (255, 0, 255), cv2.FILLED)
                    cv2.putText(img, str(id), (width, height), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
                    DataDistation[str(id)] = {}
                    for id2, point2 in enumerate(handLms.landmark):
                        if id2 != id and id2 in [0,4,8,12,16,20]:
                            width2, height2, color = img.shape
                            x2, y2 = int(point2.x * height2), int(point2.y * width2)

                            DataDistation[str(id)][str(id2)] = distance(width,height,x2,y2)

            #print(DataDistation[0][8])

            for i in POSES.keys():
                k = LoadPoses.ComparePoses(DataDistation,POSES[i])
                #print(k)
                if k > 0.4:
                    print(i)
                    if i == "ZIG":
                        Openvideo1()

            

    cv2.imshow("Image", img)           # выводим окно с нашим изображением

    knop = cv2.waitKey(1)
    if knop == ord('q'):     # ждем нажатия клавиши q в течение 1 мс
        break                    # если нажмут, всё закрываем
    if knop == ord('s'):
        namepos = input("Имя для позы: ")
        with open(f'Poses/{namepos}.txt', 'w',encoding="utf-8") as а:
            json.dump(DataDistation, а,indent=4,ensure_ascii=False)