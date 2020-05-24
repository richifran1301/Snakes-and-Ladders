import os
import time
import random
import itertools
import sys, pygame
from tkinter import *
from pygame.locals import*
from PIL import Image, ImageTk
from interface import implements, Interface

class Casilla(Interface):
    pass

class CasillaEstandar(implements(Casilla)):

    def __init__(self, mis_coordenadas, color, mi_forma):
        self.mis_coordenadas = mis_coordenadas
        self.color = color
        self.mi_forma = mi_forma

    def getCoordenadas(self):
        return self.mis_coordenadas

    def getColor(self):
        return self.color

    def getForma(self):
        return self.mi_forma
  
    
class CasillaEscalera(implements(Casilla)):

    def __init__(self, casilla):
        self.casilla = casilla

class CasillaSerpiente(implements(Casilla)):

    def __init__(self, casilla):
        self.casilla = casilla