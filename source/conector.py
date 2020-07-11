import os
import time
import random
import itertools
import sys, pygame
from pygame.locals import *
from abc import ABC, abstractmethod
from elementoTablero import ElementoTablero
from casilla import CasillaSE, CasillaEstandar, CasillaEscalera, CasillaSerpiente

class Conector(ABC):
    def __init__(self):
        super().__init__()
        self.casilla_inicio = None
        self.casilla_final = None
        
    def setCasillas(self, inicio, final):
        """
        :param inicio: El conector inicial de una casilla con otra
        :type conector: Conector
        :param final: El conector final de una casilla con otra
        :type conector: Conector
        :returns:  None -- Procedimiento set sin valor de retorno.
        """
        self.casilla_inicio = inicio
        self.casilla_final = final
    
class ConectorSE(Conector):
    """
    Clase genérica de conector para implementar decoradores.
    """
    def __init__(self, casilla, ventana):
        """
        :param casilla: Casillas relacionadas con un conector, en pos 0 la de inicio, pos 1 la de fin.
        :type casilla: tuple
        :param ventana: Referencia a la ventana de pygame.
        :type ventana: pygame.display
        """
        super().__init__()
        super().setCasillas(casilla[0], casilla[1])
        self.ventana = ventana

    def getCasillaInicio(self):
        """
        :returns:  CasillaEstandar -- Referencia a la casilla donde inicia el conector.
        """
        return self.casilla_inicio

    def getCasillaFinal(self):
        """
        :returns:  CasillaEstandar -- Referencia a la casilla donde termina el conector.
        """
        return self.casilla_final

    def getVentana(self):
        """
        :returns:  pygame.display -- Referencia a la ventana de pygame.
        """
        return self.ventana

    def sendConector(self):
        """
        Esta función envía el mismo conector (self) a sus casillas relacionadas de inicio y fin.
        :returns:  None -- Procedimiento sin valor de retorno.
        """
        self.casilla_inicio.setConector(self)
        self.casilla_final.setConector(self)

class Escalera(ConectorSE):
    """
    Esta clase representa un conector entre dos casillas de tablero, y contiene los
    atributos y acciones necesarios para su comportamiento en un tablero de juego.
    """

    def __init__(self, casilla, ventana):
        super().__init__(casilla, ventana)

    def dibujar(self):
        """
        Este método dibuja el conector como una escalera en la ventana de pygame.
        :returns:  None -- Procedimiento sin valor de retorno.
        """
        pygame.draw.line(self.getVentana(), (0,128,0), self.getCasillaInicio().getCoordenadas(), self.getCasillaFinal().getCoordenadas(), 4)

class Serpiente(ConectorSE):
    """
    Esta clase representa un conector entre dos casillas de tablero, y contiene los
    atributos y acciones necesarios para su comportamiento en un tablero de juego.
    """

    def __init__(self, casilla, ventana):
        super().__init__(casilla, ventana)

    def dibujar(self):
        """
        Este método dibuja el conector como una escalera en la ventana de pygame.
        :returns:  None -- Procedimiento sin valor de retorno.
        """
        pygame.draw.line(self.getVentana(), (255,0,0), self.getCasillaInicio().getCoordenadas(), self.getCasillaFinal().getCoordenadas(), 4)