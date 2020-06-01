import os
import time
import random
import itertools
import sys, pygame 
from pygame.locals import *

class Casilla():
    def __init__(self):
        self.colores = {"rojo": (244,124,124), "amarillo": (247,244,139), "verde": (161,222,147), "azul": (112,161,215), "blanco": (255,255,255)}

class CasillaEstandar(Casilla):

    def __init__(self, mis_coordenadas, mi_color, mi_forma, mi_indice, ventana):
        Casilla.__init__(self)
        self.mis_coordenadas = mis_coordenadas
        self.mi_color = mi_color
        self.mi_forma = mi_forma
        self.mi_indice = mi_indice
        self.ventana = ventana
        self.conector = None

    def getCoordenadas(self):
        return self.mis_coordenadas
    
    def getColor(self):
        return self.mi_color

    def getForma(self):
        return self.mi_forma

    def getIndice(self):
        return self.mi_indice

    def setColor(self, color):
        self.mi_color = self.colores[color]

    def setConector(self, conector):
        self.conector = conector


    # Usar para saber si una casilla es el inicio de un conector de 
    # Serpiente/Escalera, osea, para saber si tiene que moverse
    def esInicio(self):
        return self.conector.getCasillaInicio().casilla.getIndice() == self.mi_indice


    # Retorna la casilla a la que tiene que moverse en caso de que 
    # esInicio retorne un True
    def getFinal(self):
        return self.conector.getCasillaFinal().casilla.getIndice()

    def dibujar(self):
        pygame.draw.rect(self.ventana, self.mi_color, self.mi_forma)
        pygame.draw.rect(self.ventana, (0,0,0), self.mi_forma, 1)

        #pygame.font.init()
        font = pygame.font.SysFont('arialblack', 20) 
        text = font.render(str(self.mi_indice + 1), True, (0,0,0), self.mi_color)
        textRect = text.get_rect() 
        textRect.center = (self.mis_coordenadas[0], self.mis_coordenadas[1]) 
        self.ventana.blit(text, textRect) 
  
class CasillaEscalera(Casilla):

    def __init__(self, casilla):
        Casilla.__init__(self)
        self.casilla = casilla    

class CasillaSerpiente(Casilla):

    def __init__(self, casilla):
        Casilla.__init__(self)
        self.casilla = casilla
