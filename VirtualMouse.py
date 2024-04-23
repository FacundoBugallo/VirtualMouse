# -----Iniciamos Libreria.-----

import cv2
import numpy as np
# Nuestro programa que contiene los datos y seguimiento de las manos
import MainMouse as sm
import autopy  # libreria que nos permite manipular el mouse

# -----Declaracion de variables.-----
anchocam, altocam = 1000, 600
cuadro = 50  # donde podemos interacctuar
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

while True:
    ret, frame = cap.read()
    frame = detector.encontrarmanos(frame)  # encontramos las manos
    lista, bbox = detector.encontrarposicion(frame)  # Mostramos posiciones
    # print(frame,ret)|
    # print("Lista", lista)
    # punta de dedos del indice y corazon
    if len(lista) != 0:
        x1, y1, = lista[8][1:]  # indice
        x2, y2, = lista[12][1:]  # corazon
        # print("Lista", x1, y1, x1, x2)

    # -----Comprobamos que los deos estan levantados-----
        # contamos 5 posiciones nos indica si se levanta cualquier dedo
        dedos = detector.dedosarriba()
        cv2.rectangle(frame, (cuadro, cuadro), (anchocam - cuadro,
                      altocam - cuadro), (0, 0, 0), 2)  # Generamos cuadro
        print("==Dedos arriba :", dedos, "==")

        # moviemiento un dedo
        if dedos[1] == 1 and dedos[2] == 0:
            # Convercion a pixeles
            x3 = np.interp(x1, (cuadro, anchocam - cuadro), (0, anchopanta))
            y3 = np.interp(y1, (cuadro, altocam - cuadro), (0, altopanta))

            # suabizat valores
            # Hubicacion actual = ubi anterior + x3 divididas al valor
            # suabizado
            cubix = pubix + (x3 - pubix) / sua
            cubiy = pubiy + (y3 - pubiy) / sua

            # Mover Mouse
            autopy.mouse.move(anchopanta - cubix, cubiy)  # Enviar cords
            cv2.circle(frame, (x1, y1), 10, (0, 0, 0), cv2.FILLED)
            pubix, pubiy = cubix, cubiy

        # Comprobamos que este en modo click

        if dedos[2] == 1 and dedos[2] == 1:
            longitud, frame, linea = detector.distancia(8, 12, frame)
            print(longitud)
            if longitud < 30:
                cv2.circle(frame, (linea[4], linea[5]),
                           10, (0, 255, 0), cv2.FILLED)
                # si la distancia es correcta hacemos click
                autopy.mouse.click()

    cv2.imshow("Mouse", frame)
    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
