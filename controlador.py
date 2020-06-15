import sys, pygame
import os
import time
from pygame.locals import *
from button import Button
from sidebar import Sidebar
from conector import Conector, Escalera, Serpiente
from casilla import Casilla, CasillaEstandar, CasillaEscalera, CasillaSerpiente
from dado import Dado
from jugador import Jugador
from tablero import Tablero
from singleton import Singleton
from arbitro import Arbitro
from vista import Vista

ANCHO_BARRA = 250
ANCHO = 700 + ANCHO_BARRA
ALTO = 700
CANTIDAD_X = 10
CANTIDAD_Y = 10

class Controlador:

    def __init__(self):
        self.eventos = [1, 2, 3, 4]
        self.ventana = self.genere_ventana_pygame()
        self.vista = Vista(self.ventana)
        self.listeners = []
        self.registerListener(self.vista)

    def genere_ventana_pygame(self):
        """
        Esta funcion genera la ventana grafica de pygame. Para poder hacerle 
        modificaciones luego.
        :returns: pygame window object -- Devuelve la ventana grafica recien creada
        """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Serpientes y escaleras")
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        ventana = pygame.display.set_mode((ANCHO, ALTO))
        assert (ANCHO - ANCHO_BARRA) % CANTIDAD_X == 0 and ALTO % CANTIDAD_Y == 0
        
        return ventana

    def registerListener(self, listener):
        self.listeners.append(listener)
        
    def postEvent(self, event, type):
        for listener in self.listeners:
            if isinstance(listener, type):
                listener.notify(event)

def run():

    controlador = Controlador()

    while True:
        for events in pygame.event.get():

            if events.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            elif events.type == pygame.MOUSEBUTTONDOWN:
                '''
                #Event 1: click on dice button
                postEvent(eventos[1])
                if boton_dados.isOver(posicion_cursor):
                    resultado_dados = self.lanzar()     # esta variable contiene ahora el numero que lanzaron los dados. usar donde se necesite.
                '''
                controlador.postEvent(events.type, Vista)

            elif events.type == pygame.MOUSEMOTION:
                '''
                if boton_dados.isOver(posicion_cursor):
                    #Event 2: Change dice color (isOver)
                    postEvent(eventos[2])
                    boton_dados.mi_color = (161,222,147) 
                else:
                    #Event 3: Change dice color (isNotOver)
                    postEvent(eventos[3])
                    boton_dados.mi_color = (54,57,63)
                '''

                controlador.postEvent(events.type, Vista)
            
            '''
            #Event 4: redibujar los dados
            postEvent(eventos[4])
            boton_dados.dibujar()
            '''
            pygame.display.update()

run()