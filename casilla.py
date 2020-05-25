import os
import time
import random
import itertools
import sys, pygame 
from tkinter import *
from pygame.locals import*
from PIL import Image, ImageTk
#rom interface import implements, Interface

class Casilla():
    pass

class CasillaEstandar(Casilla):

    def __init__(self, mis_coordenadas, color, mi_forma, mi_indice, ventana):
        self.mis_coordenadas = mis_coordenadas
        self.color = color
        self.mi_forma = mi_forma
        self.mi_indice = mi_indice
        self.ventana = ventana

    def getCoordenadas(self):
        return self.mis_coordenadas

    def getColor(self):
        return self.color

    def getForma(self):
        return self.mi_forma

    def getIndice(self):
        return self.mi_indice

    def dibujar(self):
        pygame.draw.rect(self.ventana, (0,0,0), self.mi_forma)
        pygame.draw.rect(self.ventana, (200,200,200), self.mi_forma, 1)
        return
  
    
class CasillaEscalera(Casilla):

    def __init__(self, casilla):
        self.casilla = casilla

class CasillaSerpiente(Casilla):

    def __init__(self, casilla):
        self.casilla = casilla