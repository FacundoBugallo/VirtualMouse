#-----Iniciamos Libreria.-----

import cv2
import numpy as np
import MainMouse as sm #Nuestro programa que contiene los datos y seguimiento de las manos
import autopy #libreria que nos permite manipular el mouse

#-----Declaracion de variables.-----
anchocam, altocam = 1280, 960
cuadro = 150 #donde podemos interacctuar
anchopanta , altopanta = autopy.screen.size()#obtenemos las dimensiones de nuestra pantalla
sua = 5
pubix, pubiy = 0,0
cubix, cubiy = 0,0
print("Valores de pantalla")
print(anchopanta , altopanta)

#-----Lectura de camara.-----
print("Lectura de pantalla")
cap = cv2.VideoCapture(0)
cap.release()
print("Release",cap)
cap = cv2.VideoCapture(1)

cap.set(3, anchocam) #-----Defiinimos un ancho para la camara.-----
cap.set(4, altocam)
print("Sets", cap)
#-----Declaramos el detector-----

detector = sm.detectormanos(maxhands=1)#utilzaremos una mano
print( "==Maximo de damons : ", detector.maxhands, "==")

clic_activo = False

while True:
    ret, frame = cap.read()
    frame = detector.encontrarmanos(frame)
    lista, bbox = detector.encontrarposicion(frame)

    if len(lista) != 0:
        x1, y1 = lista[8][1:]  # Coordenadas del dedo índice
        x2, y2 = lista[12][1:]  # Coordenadas del dedo corazón
        dedos = detector.dedosarriba()

        # Si los dedos índice y corazón están levantados, activa el clic
        if dedos[1] == 1 and dedos[2] == 1:
            clic_activo = True
            autopy.mouse.toggle(True)  # Activar el clic

        # Si el clic está activo, mueve el mouse
        if clic_activo:
            x3 = np.interp(x1, (cuadro, anchocam - cuadro), (0, anchopanta))
            y3 = np.interp(y1, (cuadro, altocam - cuadro), (0, altopanta))
            cubix = pubix + (x3 - pubix) / sua
            cubiy = pubiy + (y3 - pubiy) / sua
            autopy.mouse.move(anchopanta - cubix, cubiy)
            cv2.circle(frame, (x1, y1), 10, (0, 0, 0), cv2.FILLED)
            pubix, pubiy = cubix, cubiy

        # Si los dedos índice y corazón no están levantados, desactiva el clic
        if dedos[1] == 0 and dedos[2] == 0:
            clic_activo = False
            autopy.mouse.toggle(False)  # Desactivar el clic

    cv2.imshow("Mouse", frame)
    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
