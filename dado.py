import os
import time
import random
import itertools
import sys, pygame
from singleton import Singleton
from pygame.locals import *

class Dado():
    """
    Esta clase representa un dado de seis caras, y sus atributos y acciones necesarios 
    para su comportamiento en un tablero de juego.
    """

    def __init__(self):
        """
        :param ventana: Referencia a la ventana de pygame.
        :type ventana: pygame.display
        """
        self.valores_caras = [1,2,3,4,5,6]      # valores de las caras
        self.caras = None

    def lanzar(self):
        """
        Esta función dibuja los dados resultantes de un lanzamiento y arroja la suma de sus valores.
        :returns:  int -- Suma de las caras resultantes de ambos dados.
        """

        # genere dos números aleatorios entre 1 y 6, ambos inclusive
        resultados_por_dado = [self.valores_caras[random.randint(0, len(self.valores_caras) - 1)] for i in range(2)]
        # sume los resultados
        resultado_al_lanzar = sum(resultados_por_dado)
        # dibuje los resultados
        self.dibujar(resultados_por_dado)

        return resultado_al_lanzar

    def dibujar(self, resultados_por_dado):

        """
        Esta función dibuja dos dados según el resultado de sus caras.
        :returns:  None -- Procedimiento sin valor de retorno.
        """

        # dirección de las imágenes de los dados
        ruta_local = 'imagenes/'

        # haga el proceso de dibujo de la primera cara del dado, de pygame para imágenes
        ruta_imagen = os.path.join(ruta_local, str(resultados_por_dado[0]) + ".png")
        cara_temp = pygame.image.load(ruta_imagen)
        imagen_transformada = pygame.transform.scale(cara_temp, (60,60))
        cara_izq = imagen_transformada.convert()  # or .convert_alpha()
        rect_izq = cara_izq.get_rect()
        rect_izq.center = (780, 145)
        Singleton.ventana.blit(cara_izq, rect_izq)

        # lo mismo para la segunda cara
        ruta_imagen = os.path.join(ruta_local, str(resultados_por_dado[1]) + ".png")
        cara_temp = pygame.image.load(ruta_imagen)
        imagen_transformada = pygame.transform.scale(cara_temp, (60,60))
        cara_der = imagen_transformada.convert()  # or .convert_alpha()
        rect_der = cara_der.get_rect()
        rect_der.center = (870, 145)
        Singleton.ventana.blit(cara_der, rect_der)
    
    def espere_repuesta_dados(self, boton_dados):
        """
        Este metodo va a esperar que el usuario presione en la interfaz, el boton de tirar dados. Va a representar
        los dados graficamente tambien, y almacenar el valor guardado en una variable llamada resultado_dados.
        Ademas, cambia el color de la opcion del boton si se tiene el cursor sobre el. Por ultimo, tambien contempla 
        la opcion de que el usuario presione la equis para salir del juego y es una opcion normal para salirse.
        :param boton_dados: representacion del boton de los dados, cuando el usuario hace clic sobre el es que se 
        tiran los dados.
        :type boton_dados: Button
        :returns: variable que almaceno el valor sumado que salio en los dados
        """
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
                        resultado_dados = self.lanzar()     # esta variable contiene ahora el numero que lanzaron los dados. usar donde se necesite.

                elif events.type == pygame.MOUSEMOTION:

                    if boton_dados.isOver(posicion_cursor):
                        boton_dados.mi_color = (161,222,147) 
                    else:
                        boton_dados.mi_color = (54,57,63)
                boton_dados.dibujar()
                pygame.display.update()
        return resultado_dados
        
