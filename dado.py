import os
import time
import random
import itertools
import sys, pygame
from pygame.locals import *

class Dado():

    def __init__(self, ventana):
        self.valores_caras = [1,2,3,4,5,6]
        self.caras = None
        self.ventana = ventana

    def lanzar(self):
        resultados_por_dado = [self.valores_caras[random.randint(0, len(self.valores_caras) - 1)] for i in range(2)]
        resultado_al_lanzar = sum(resultados_por_dado)
        self.dibujar(resultados_por_dado)
        return resultado_al_lanzar

    def dibujar(self, resultados_por_dado):
        ruta_local = os.path.dirname(__file__)

        ruta_imagen = os.path.join(ruta_local, str(resultados_por_dado[0]) + ".png")
        cara_temp = pygame.image.load(ruta_imagen)
        imagen_transformada = pygame.transform.scale(cara_temp, (60,60))
        cara_izq = imagen_transformada.convert()  # or .convert_alpha()
        rect_izq = cara_izq.get_rect()
        rect_izq.center = (780, 145)
        self.ventana.blit(cara_izq, rect_izq)

        ruta_imagen = os.path.join(ruta_local, str(resultados_por_dado[1]) + ".png")
        cara_temp = pygame.image.load(ruta_imagen)
        imagen_transformada = pygame.transform.scale(cara_temp, (60,60))
        cara_der = imagen_transformada.convert()  # or .convert_alpha()
        rect_der = cara_der.get_rect()
        rect_der.center = (870, 145)
        self.ventana.blit(cara_der, rect_der)
        