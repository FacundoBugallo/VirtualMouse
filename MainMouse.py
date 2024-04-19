#-----ImportLib.-----

import math
import cv2
import mediapipe as mp
import time

#-----Work with classes.-----
class handdetector():
        #-----Initialize Detection Parameters-----
    def __init__(self, mode=False, maxhands=2, Confdeteccion = 0.5, Confsegui = 0.5):
        self.mode = mode
        self.maxhands = maxhands
        self.Confdeteccion = Confdeteccion
        self.Confsegui = Confsegui
