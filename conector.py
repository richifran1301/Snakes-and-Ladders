import os
import time
import random
import itertools
import sys, pygame
from pygame.locals import *
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

    def sendConector(self):
        self.casilla_inicio.casilla.setConector(self)
        self.casilla_final.casilla.setConector(self)

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
