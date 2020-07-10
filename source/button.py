import os
import time
import random
import itertools
import sys, pygame
from pygame.locals import *

class Boton():
    """
    Clase que equivale a un boton para la interfaz
    """
    def __init__(self, ventana, mi_color,x ,y , ancho, alto, text=''):
        """
        :param ventana: Referencia a la ventana de pygame.
        :type ventana: pygame.display
        :param mi_color: Color del botón.
        :type mi_color: tuple
        :param x = Posicion en el eje x en la cual se excuentra el mouse 
        :type x: int
        :param x = Posicion en el eje y en la cual se excuentra el mouse 
        :type x: int
        :param ancho: Ancho del botón
        :type ancho: int
        :param alto: Alto del botón
        :type alto: int
        :param text: Texto opcional que tendrá el botón, el cual tiene como valor predeterminado ''
        :type text: string
        :atribute mi_forma: forma del botón
        :type mi_forma: pygame.Rect
        """
        self.x = x
        self.y = y
        self.text = text
        self.alto = alto
        self.ancho = ancho
        self.ventana = ventana
        self.mi_color = mi_color
        self.mi_forma = pygame.Rect(x, y, ancho, alto)

    def dibujar(self):
        """
        Esta función se encarga de dibujar el botón en la posición dada al inicializarse
        :returns:  None -- Procedimiento sin valor de retorno.
        """
        pygame.draw.rect(self.ventana, self.mi_color, self.mi_forma)                # Se dibuja un pygame.Rect el cual corresponde a la forma del botón
        pygame.draw.rect(self.ventana, (54,57,63), self.mi_forma, 1)                # Se dibuja un pygame.Rect que corresponde al borde del botón
        
        if self.text != '':
            font = pygame.font.SysFont('verdana', 15, bold=True)                    # Se seleciona el font deseado para el texto del botón
            text = font.render(self.text, True, (255,255,255), self.mi_color)       # Se le aplica el formato al texto y un color para este
            textRect = text.get_rect()                                              # Se obtiene un cuadrado pygame.Rect a partir del texto
            textRect.center = (self.x + self.ancho // 2, self.y + self.alto // 2)   # Se establece la posición central del pygame.Rect que se acaba de obtener

            self.ventana.blit(text, textRect)                                       # Se dibuja en la ventana el botón.

    def isOver(self, pos):
        """
        Esta función se encarga de averiguar si el mouse se encuentra por encima del botón.
        :param pos: Posicion (x,y) en la que se encuentra el mouse en un momento dado
        :type pos: tuple
        :returns:  None -- Procedimiento sin valor de retorno.
        """
        #Pos is the mouse position or a tuple of (x,y) coordinates                  
        if pos[0] > self.x and pos[0] < self.x + self.ancho:                        # Si el mouse se encuentra en el interior del botón
            if pos[1] > self.y and pos[1] < self.y + self.alto:                     
                return True                                                         # Se retorna true
            
        return False                                                                # En cualquier otro caso, false