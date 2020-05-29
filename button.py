import os
import time
import random
import itertools
import sys, pygame
from pygame.locals import *

class Button():
    def __init__(self, ventana, mi_color, x ,y , ancho, alto, text=''):
        self.x = x
        self.y = y
        self.text = text
        self.alto = alto
        self.ancho = ancho
        self.ventana = ventana
        self.mi_color = mi_color
        self.mi_forma = pygame.Rect(x, y, ancho, alto)

    def dibujar(self):

        pygame.draw.rect(self.ventana, self.mi_color, self.mi_forma)
        pygame.draw.rect(self.ventana, (54,57,63), self.mi_forma, 1)
        
        if self.text != '':
            font = pygame.font.SysFont('verdana', 15, bold=True)
            text = font.render(self.text, True, (255,255,255), self.mi_color)
            textRect = text.get_rect() 
            textRect.center = (self.x + self.ancho // 2, self.y + self.alto // 2) 

            self.ventana.blit(text, textRect)

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.ancho:
            if pos[1] > self.y and pos[1] < self.y + self.alto:
                return True
            
        return False