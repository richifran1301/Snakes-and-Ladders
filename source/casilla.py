import os
import time
import random
import itertools
import sys, pygame 
from pygame.locals import *
from singleton import Singleton
from abc import ABC, abstractmethod
from elementoTablero import ElementoTablero

class Casilla(ElementoTablero):
    def __init__(self):
        super().__init__()
        self.conector = None
        self.mi_indice = None
        
    def setIndice(self, indice):
        """
        :param indice: Índice de la casilla en el vector de casillas de Tablero.
        :type color: int
        :returns:  None -- Procedimiento set sin valor de retorno.
        """
        self.mi_indice = indice
        
    def setConector(self, conector):
        """
        :param conector: El conector que tiene una casilla con otra.
        :type conector: Conector
        :returns:  None -- Procedimiento set sin valor de retorno.
        """
        self.conector = conector
        
    def getConector(self):
        """
        :returns:  Conector -- El conector que tiene una casilla con otra.
        """
        return self.conector 
        
    def getIndice(self):
        """
        :returns:  int -- La posicion de la casilla en la lista 'casillas' de Tablero.
        """
        return self.mi_indice
            
class CasillaSE(Casilla):
    """
    Clase genérica de casilla para implementar decoradores.
    """

    def __init__(self, mis_coordenadas, mi_color, mi_forma, mi_indice, ventana):
        """
        :param mis_coordenadas: Coordenadas en tupla (x, y) del centro de la casilla.
        :type mis_coordenadas: tuple
        :param mi_color: Color de la casilla.
        :type mi_color: tuple
        :param mi_forma: Forma de pygame de la casilla (rectangular).
        :type mi_forma: pygame.Rect
        :param mi_indice: Índice de la casilla en el vector de casillas de Tablero.
        :type mi_indice: int
        :param ventana: Referencia a la ventana de pygame.
        :type ventana: pygame.display
        """
        super().__init__()
        super().setIndice(mi_indice)
        
        self.mis_coordenadas = mis_coordenadas
        self.mi_color = mi_color
        self.mi_forma = mi_forma
        self.ventana = ventana

    def getCoordenadas(self):
        """
        :returns:  tuple -- Una tupla con las coordenadas x, y del centro de la casilla.
        """
        return self.mis_coordenadas
    
    def getColor(self):
        """
        :returns:  tuple -- Una tupla con el color r, g, b de la casilla.
        """
        return self.mi_color

    def getForma(self):
        """
        :returns:  pygame.Rect -- Una tupla con el color r, g, b de la casilla.
        """
        return self.mi_forma
    
    def setColor(self, color):
        """
        :param color: El color para la casilla en RGB (a,b,c).
        :type color: tuple
        :returns:  None -- Procedimiento set sin valor de retorno.
        """
        self.mi_color = Singleton.colores_casillas[color]

    def esInicio(self):
        """
        Este método indica si una casilla es el inicio de un conector o no.
        :returns:  bool -- Será True si la casilla es inicio en su respectivo conector.
        """
        return self.conector.getCasillaInicio().getIndice() == self.mi_indice

    def getFinal(self):
        """
        Este método devuelve la casilla a la que un jugador debe desplazarse si está en una de inicio.
        Es útil usarla en conjunto con la función esInicio() cuando devuelve verdadero.
        :returns:  CasillaEstandar -- Casilla final en el conector de la casilla actual.
        """
        return self.conector.getCasillaFinal()

    def dibujar(self):
        """
        Este método dibuja la casilla en la ventana de pygame.
        :returns:  None -- Procedimiento sin valor de retorno.
        """
        pygame.draw.rect(self.ventana, self.mi_color, self.mi_forma) # se pasan las referencias estéticas
        pygame.draw.rect(self.ventana, (0,0,0), self.mi_forma, 1)

        font = pygame.font.SysFont('arialblack', 20)                                # parametros de fuente del texto (num. casilla)
        text = font.render(str(self.mi_indice + 1), True, (0,0,0), self.mi_color)   # procesamiento del texto para pygame
        textRect = text.get_rect() 
        textRect.center = (self.mis_coordenadas[0], self.mis_coordenadas[1])        # coordenadas del texto
        self.ventana.blit(text, textRect)

class CasillaEstandar(CasillaSE):
    """
    Esta clase representa una casilla de tablero, y contiene los
    atributos y acciones necesarios para su graficación y comportamiento
    en un tablero de juego.
    """

    def __init__(self, mis_coordenadas, mi_color, mi_forma, mi_indice, ventana):
        super().__init__(mis_coordenadas, mi_color, mi_forma, mi_indice, ventana)

class CasillaEscalera(CasillaSE):
    """
    Esta clase representa una casilla de tablero, y contiene los
    atributos y acciones necesarios para su graficación y comportamiento
    en un tablero de juego.
    """

    def __init__(self, mis_coordenadas, mi_color, mi_forma, mi_indice, ventana):
        super().__init__(mis_coordenadas, mi_color, mi_forma, mi_indice, ventana)

class CasillaSerpiente(CasillaSE):
    """
    Esta clase representa una casilla de tablero, y contiene los
    atributos y acciones necesarios para su graficación y comportamiento
    en un tablero de juego.
    """

    def __init__(self, mis_coordenadas, mi_color, mi_forma, mi_indice, ventana):
        super().__init__(mis_coordenadas, mi_color, mi_forma, mi_indice, ventana)