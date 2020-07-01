import cv2
import time
import pandas
import requests
from datetime import datetime, timezone
from timeloop import Timeloop
from datetime import timedelta

static_back = None
motion_list = [None, None]
time = []
counter1 = 0
counter2 = 0 

print("Oprogramowanie Kamery")
print("*****************************************************")
print("Wybierz jedna z opcji i zatwierdz przyciskiem Enter:")


print("1 -> Wybierz kamere")
print("2 -> Wybierz plik wideo do odtworzenia")
x = int(input())
y = 0

if x == 1:
    print("Jesli korzystasz z kamery wbudowanej wybierz 0. Dla kazdej kolejnej podlaczonej kamery wybierz 1, 2, 3 itd.")
    input_file = int(input("Podaj nr kamery i zatwierdz przyciskiem Enter:"))
    y=1
elif x == 2:
    input_file = input("Wpisz nazwe pliku (jesli jest w folderze z programem) lub sciezke do pliku i zatwierdz przyciskiem Enter:")
    y=1
else:
    input_file = input("Nie ma takiej opcji! Nacisnij Enter, aby zamknac.")
    y=0
    

if y != 0:
    video = cv2.VideoCapture(input_file)

    while True:

        check, frame = video.read()
        motion = 0
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if static_back is None:
            static_back = gray
            continue

        diff_frame = cv2.absdiff(static_back, gray)
        thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
        thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

        cnts, _ = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in cnts:
            if cv2.contourArea(contour) < 12000:
                continue
            motion = 1

            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            
            

        motion_list.append(motion)
        motion_list = motion_list[-2:]

        if motion_list[-1] == 1 and motion_list[-2] == 0:
            time.append(datetime.now())

        if motion_list[-1] == 0 and motion_list[-2] == 1:
            time.append(datetime.now())
            counter1 += 1
            counter2 += 1

        cv2.putText(frame, "Licznik: {}".format(counter2), (10, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        cv2.putText(frame, "Nacisnij Q aby zamknac", (10, 460),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        cv2.imshow("Oprogramowanie Kamery", frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            if motion == 1:
                time.append(datetime.now())
            break

    video.release()

    # Destroying all the windows
    cv2.destroyAllWindows()
else:
    print("Zamkniecie aplikacji. Uruchom ponownie.")