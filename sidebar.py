import os
import time
import random
import itertools
import sys, pygame
from dado import Dado
from button import Button
from pygame.locals import *

class Sidebar():
    def __init__(self, ventana, alto_total, ancho_total, ancho_sidebar, mi_color, elementos):
        self.ventana = ventana
        self.alto_total = alto_total
        self.ancho_total = ancho_total
        self.ancho_sidebar = ancho_sidebar
        self.mi_color = mi_color
        self.mi_forma = pygame.Rect(700, 0, ancho_sidebar, alto_total)
        self.elementos = elementos
        self.dibujar()

    def dibujar(self):
        pygame.draw.rect(self.ventana, self.mi_color, self.mi_forma)
        pygame.draw.rect(self.ventana, (0,0,0), self.mi_forma, 1)
        #for elementos
        self.elementos[0].dibujar() #boton "lanzar dados"
