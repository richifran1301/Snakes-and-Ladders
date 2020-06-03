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
    
    def espere_repuesta_dados(self, boton_dados, dado):
        boton_dados.dibujar()
        pygame.display.update()
        resultado_dados = 0
        while resultado_dados == 0:
            for events in pygame.event.get():
                posicion_cursor = pygame.mouse.get_pos()

                if events.type == QUIT:
                    pygame.quit()
                    sys.exit(0)

                elif events.type == pygame.MOUSEBUTTONDOWN:
                    if boton_dados.isOver(posicion_cursor):
                        resultado_dados = dado.lanzar()     # esta variable contiene ahora el numero que lanzaron los dados. usar donde se necesite.

                elif events.type == pygame.MOUSEMOTION:

                    if boton_dados.isOver(posicion_cursor):
                        boton_dados.mi_color = (161,222,147) 
                    else:
                        boton_dados.mi_color = (54,57,63)
                boton_dados.dibujar()
                pygame.display.update()
        return resultado_dados
        