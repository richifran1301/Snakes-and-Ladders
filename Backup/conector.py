import os
import time
import random
import itertools
import sys, pygame
from pygame.locals import *
from casilla import Casilla, CasillaEstandar, CasillaEscalera, CasillaSerpiente

class Conector():
    """
    Clase genérica de conector para implementar decoradores.
    """
    pass

class ConectorEstandar(Conector):
    """
    Esta clase representa una conector entre dos casillas de tablero, y contiene los
    atributos y acciones necesarios para su comportamiento en un tablero de juego.
    En el juego Serpientes y escaleras estos pueden decorarse como serpientes o escaleras.
    """

    def __init__(self, casilla, ventana):
        """
        :param casilla: Casillas relacionadas con un conector, en pos 0 la de inicio, pos 1 la de fin.
        :type casilla: tuple
        :param ventana: Referencia a la ventana de pygame.
        :type ventana: pygame.display
        """
        Conector.__init__(self)
        self.casilla_inicio = casilla[0]    
        self.casilla_final = casilla[1]
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
        self.casilla_inicio.casilla.setConector(self)
        self.casilla_final.casilla.setConector(self)

class Escalera(Conector):
    """
    Decorador de un ConectorEstandar como una escalera.
    """

    def __init__(self, conector):
        """
        :param conector: Objeto ConectorEstandar que se decora.
        :type conector: ConectorEstandar
        """
        Conector.__init__(self)
        self.conector = conector

    def dibujar(self):
        """
        Este método dibuja el conector como una escalera en la ventana de pygame.
        :returns:  None -- Procedimiento sin valor de retorno.
        """
        pygame.draw.line(self.conector.getVentana(), (0,128,0), self.conector.getCasillaInicio().casilla.getCoordenadas(), self.conector.getCasillaFinal().casilla.getCoordenadas(), 4)

class Serpiente(Conector):
    """
    Decorador de un ConectorEstandar como una serpiente.
    """

    def __init__(self, conector):
        """
        :param conector: Objeto ConectorEstandar que se decora.
        :type conector: ConectorEstandar
        """
        Conector.__init__(self)
        self.conector = conector

    def dibujar(self):
        """
        Este método dibuja el conector como una escalera en la ventana de pygame.
        :returns:  None -- Procedimiento sin valor de retorno.
        """
        pygame.draw.line(self.conector.getVentana(), (255,0,0), self.conector.getCasillaInicio().casilla.getCoordenadas(), self.conector.getCasillaFinal().casilla.getCoordenadas(), 4)
