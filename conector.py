import os
import time
import random
import itertools
import sys, pygame
from tkinter import *
from pygame.locals import *
from PIL import Image, ImageTk
from casilla import Casilla, CasillaEstandar, CasillaEscalera, CasillaSerpiente

class Conector():
    pass

class ConectorEstandar(Conector):

    def __init__(self, casilla, ventana):
        Conector.__init__(self)
        self.casilla_inicio = casilla[0]
        self.casilla_final = casilla[1]
        self.ventana = ventana

    def getCasillaInicio(self):
        return self.casilla_inicio

    def getCasillaFinal(self):
        return self.casilla_final

    def getVentana(self):
        return self.ventana
    
class Escalera(Conector):

    def __init__(self, conector):
        Conector.__init__(self)
        self.conector = conector

    def dibujar(self):
        pygame.draw.line(self.conector.getVentana(), (0,128,0), self.conector.getCasillaInicio().casilla.getCoordenadas(), self.conector.getCasillaFinal().casilla.getCoordenadas(), 4)

class Serpiente(Conector):

    def __init__(self, conector):
        Conector.__init__(self)
        self.conector = conector

    def dibujar(self):
        pygame.draw.line(self.conector.getVentana(), (255,0,0), self.conector.getCasillaInicio().casilla.getCoordenadas(), self.conector.getCasillaFinal().casilla.getCoordenadas(), 4)
