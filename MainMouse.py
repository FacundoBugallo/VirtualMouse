# -----ImportLib.-----

import math
import cv2
import mediapipe as mp
import time

# -----Work with classes.-----


class detectormanos():
    # -----Initialize Detection Parameters.-----
    def __init__(self, mode=False, maxhands=2, Confdeteccion=1, Confsegui=0.5):
        self.mode = mode  # -----Creamos el objeto y el tendra su propia variable.-----
        self.maxhands = maxhands  # -----Lo mismo haremos con todos los objetos.-----
        self.Confdeteccion = Confdeteccion
        self.Confsegui = Confsegui

        # -----Creamos los objetos que detectaran las manos y las dibujaran.---
        self.mpmanos = mp.solutions.hands
        self.manos = self.mpmanos.Hands(
            self.mode,
            self.maxhands,
            self.Confdeteccion,
            self.Confsegui)
        self.dibujo = mp.solutions.drawing_utils
        self.tip = [4, 8, 12, 16, 20]

        # -----funcion para encontrar la mano-----
    def encontrarmanos(self, frame, dibujar=True):
        imgcolor = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.resultados = self.manos.process(imgcolor)

        # Verifica si se detectaron manos
        if self.resultados.multi_hand_landmarks:
            print("True")
            for mano in self.resultados.multi_hand_landmarks:
                if dibujar:
                    self.dibujo.draw_landmarks(
                        frame, mano, self.mpmanos.HAND_CONNECTIONS)
        else:
            print("No se detectaron manos")

        return frame

        # -----funcion para encontrar la posicion-----
    def encontrarposicion(self, frame, ManoNum=0, dibujar=True):
        xlista = []
        ylista = []
        bbox = []
        self.lista = []  # almacenaremos cordenadas de x e y.
        if self.resultados.multi_hand_landmarks:
            miMano = self.resultados.multi_hand_landmarks[ManoNum]
            for id, lm in enumerate(miMano.landmark):
                alto, ancho, c = frame.shape  # Extraemos dimenciones
                # convertimos la info en pixeles
                cx, cy = int(lm.x * ancho), int(lm.y * alto)
                xlista.append(cx)
                ylista.append(cy)
                self.lista.append([id, cx, cy])
                if dibujar:
                    cv2.circle(frame, (cx, cy), 5, (0, 0, 0),
                               cv2.FILLED)  # creamos un circulo

            xmin, xmax = min(xlista), max(xlista)
            ymin, ymax = min(ylista), max(ylista)
            bbox = xmin, ymin, xmax, ymax
            if dibujar:
                cv2.rectangle(frame, (xmin - 20, ymin - 20),
                              (xmax + 20, ymax + 20), (0, 255, 0), 2)
        return self.lista, bbox

    # funcion de deteccion de dedos
    def dedosarriba(self):
        dedos = []
        if self.lista[self.tip[0]][1] > self.lista[self.tip[0] - 1][1]:
            dedos.append(1)
        else:
            dedos.append(0)

        for id in range(1, 5):
            if self.lista[self.tip[id]][2] < self.lista[self.tip[id] - 2][2]:
                dedos.append(1)
            else:
                dedos.append(0)
        return dedos

    # detectar la distancia entre los dedos
    def distancia(self, p1, p2, frame, dibujar=True, r=15, t=3):

        x1, y1 = self.lista[p1][1:]
        x2, y2 = self.lista[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        if dibujar:
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 250), t)
            cv2.circle(frame, (x1, y1), r, (0, 0, 250), cv2.FILLED)
            cv2.circle(frame, (x2, y2), r, (0, 0, 250), cv2.FILLED)
            cv2.circle(frame, (cx, cy), r, (0, 0, 250), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)
        return length, frame, [x1, y1, x2, y2, cx, cy]
# funcion principal


def main():
    ptiempo = 0
    ctiempo = 0
    # lee    mos camara
    cap = cv2.VideoCapture(1)
    # creamos objt
    detector = detectormanos()
    # realizamos la deteccion de manos
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # una ves tenemos imagen la enviamos
        frame = detector.encontrarmanos(frame)
        lista, bbox = detector.encontrarposicion(frame)
        if len(lista) != 0:
            print(lista[4])
        # mostramos fps
        ctiempo = time.time()
        fps = 1 / (ctiempo - ptiempo)
        ptiempo = ctiempo
        print(fps)
        cv2.putText(frame, str(int(fps)), (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Manos", frame)
        # Cambiado a 1 para permitir que el bucle continúe leyendo desde la
        # cámara
        k = cv2.waitKey(1)

        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
