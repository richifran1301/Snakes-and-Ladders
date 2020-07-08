import os
import time
import random
import itertools
import sys, pygame
from dado import Dado
#from button import Button
from pygame.locals import *
from singleton import Singleton

class Sidebar():
    """
    Clase que representa al espacio extra en la ventana de pygame, que no pertenece al tablero.
    Contiene informacion valiosa que le comuncia al jugador el turno, quien gana, como moverse...
    Ademas, en este espacio se juega con los dados para decidir turnos y permitir al jugador moverse
    en el juego. 
    """
    def __init__(self, alto_total, ancho_total, ancho_sidebar, mi_color, elementos):
        """
        :param alto_total = medida del alto de la ventana de pygame 
        :type alto_total: int
        :param ancho_total = medida del ancho de la ventana de pygame
        :type ancho_total: int
        :param alto_sidebar = medida del alto de este espacio al lado del tablero 
        :type alto_sidebar: int
        :param ancho_sidebar = medida del ancho de este espacio al lado del tablero 
        :type ancho_sidebar: int
        :param mi_color: codigo del color a escoger
        :type color: codigo de color perteneciente a la lista de colores de Singleton.
        :param elementos: lista que contiene al boton de los dados, y los dados.
        :type elementos: lista
        """
        self.alto_total = alto_total
        self.ancho_total = ancho_total
        self.ancho_sidebar = ancho_sidebar
        self.mi_color = mi_color
        self.mi_forma = pygame.Rect(700, 0, ancho_sidebar, alto_total)
        self.elementos = elementos
        self.dibujar()

    def dibujar(self):
        """
        Metodo que ilustra visualmente el espacio al lado del tablero.
        """
        pygame.draw.rect(Singleton.ventana, self.mi_color, self.mi_forma)
        pygame.draw.rect(Singleton.ventana, Singleton.colores_casillas["negro"], self.mi_forma, 1)
        #for elementos
        self.elementos[0].dibujar() #boton "lanzar dados"
