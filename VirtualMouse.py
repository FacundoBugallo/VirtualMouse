# -----Iniciamos Libreria.-----

import cv2
import numpy as np
# Nuestro programa que contiene los datos y seguimiento de las manos
import MainMouse as sm
import autopy  # libreria que nos permite manipular el mouse
import time
# -----Declaracion de variables.-----
anchocam, altocam = 840, 550
cuadro = 150  # donde podemos interacctuar
# obtenemos las dimensiones de nuestra pantalla
anchopanta, altopanta = autopy.screen.size()
sua = 5
pubix, pubiy = 0, 0
cubix, cubiy = 0, 0
print("Valores de pantalla")
print(anchopanta, altopanta)

# -----Lectura de camara.-----
print("Lectura de pantalla")
cap = cv2.VideoCapture(0)
cap.release()
print("Release", cap)
cap = cv2.VideoCapture(1)

cap.set(3, anchocam)  # -----Defiinimos un ancho para la camara.-----
cap.set(4, altocam)
print("Sets", cap)
# -----Declaramos el detector-----

detector = sm.detectormanos(maxhands=1)  # utilzaremos una mano
print("==Maximo de damons : ", detector.maxhands, "==")

ultimoclick = 0  # Inicializamos el tiempo del último clic

while True:
    ret, frame = cap.read()
    frame = detector.encontrarmanos(frame)  # encontramos las manos
    lista, bbox = detector.encontrarposicion(frame)  # Mostramos posiciones

    if len(lista) != 0:
        x1, y1, = lista[8][1:]  # índice
        x2, y2, = lista[12][1:]  # corazón

        dedos = detector.dedosarriba()
        cv2.rectangle(frame, (cuadro, cuadro), (anchocam - cuadro,
                      altocam - cuadro), (0, 0, 0), 2)  # Generamos cuadro

        if dedos[1] == 1 and dedos[2] == 0:
            x3 = np.interp(x1, (cuadro, anchocam - cuadro), (0, anchopanta))
            y3 = np.interp(y1, (cuadro, altocam - cuadro), (0, altopanta))

            cubix = pubix + (x3 - pubix) / sua
            cubiy = pubiy + (y3 - pubiy) / sua

            autopy.mouse.move(anchopanta - cubix, cubiy)  # Enviar cords
            cv2.circle(frame, (x1, y1), 10, (0, 0, 0), cv2.FILLED)
            pubix, pubiy = cubix, cubiy

        if dedos[2] == 1 and dedos[2] == 1:
            longitud, frame, linea = detector.distancia(8, 12, frame)
            if longitud < 60:
                current_time = time.time()
                if current_time - ultimoclick > 2:  # Verifica si han pasado al menos 2 segundos
                    cv2.circle(frame, (linea[4], linea[5]), 10, (0, 255, 0), cv2.FILLED)
                    autopy.mouse.click()
                    ultimoclick = current_time  # Actualiza el tiempo del último clic

    cv2.imshow("Mouse", frame)
    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
