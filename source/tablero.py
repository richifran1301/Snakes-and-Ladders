import os
import time
import random
import itertools
import sys, pygame
from pygame.locals import *
from sidebar import Sidebar
from conector import ConectorSE, Escalera, Serpiente
from fabrica import FabricaTableros, FabricaTablerosSE
from casilla import CasillaSE, CasillaEstandar, CasillaEscalera, CasillaSerpiente
from singleton import Singleton
from abc import ABC, abstractmethod
    
class Tablero(ABC):
    """
    Clase virtual de tablero disenada para el correcto uso del MARDA.
    """
    def __init__(self):
        """
        Constructor abstracto de la clase Tablero.
        """
        super().__init__()
        self.casillas = []

    def initCasillas(self, casillas):
        """
        Este método se encarga de incilizar el vector de casillas de juego.
        :param casillas: casillas del tablero de juego
        :type CasillaSE[]: array
        :returns:  None -- Procedimiento init sin valor de retorno.
        """
        self.casillas = casillas
        
    def appendCasilla(self, casilla):
        """
        Este método se encarga de agregar al array de casillas algunas casilla que se quiera agregar a este
        :param casilla: casilla del tablero de juego
        :type CasillaSE: casilla
        :returns:  None -- Procedimiento append sin valor de retorno.
        """
        self.casillas.append(casilla)

class TableroSE(Tablero):
    """
    Esta clase representa un tablero de juego, y contiene los
    atributos y acciones necesarios para su graficación y comportamiento.
    """

    def __init__(self, tamanio, ventana, ancho_barra, es_partida_cargada):
        """
        :param tamanio: Tamaño del tablero en píxeles como tupla (ancho, alto).
        :type tamanio: tuple
        :param ventana: Referencia a la ventana de pygame.
        :type ventana: pygame.display
        :param ancho_barra: Ancho de la sidebar junto al tablero.
        :type ancho_barra: int
        """
        super().__init__()
        self.tamanio = tamanio
        self.ventana = ventana
        Singleton.tamanio = tamanio
        self.es_partida_cargada = es_partida_cargada
        fabricaSE = FabricaTablerosSE()
        self.casillas, self.serpientes, self.escaleras = fabricaSE.crearElementosTablero()        # lista de casillas del tablero
        self.ancho_barra = ancho_barra

    def cargarCasillas(self):
        """
        Este metodo va a cear las casillas estandar y las va a guardar dentro del vector de casillas.
        """
        centros_casillas = self.obtener_centro_casillas(Singleton.alto_tablero, Singleton.ancho_tablero)
        for i in range(len(centros_casillas)):
            figura = pygame.Rect(centros_casillas[i][0] - int((Singleton.alto_tablero//self.tamanio[0])//2),
                                centros_casillas[i][1] - int((Singleton.ancho_tablero//self.tamanio[1])//2),
                                Singleton.alto_tablero//self.tamanio[0], Singleton.ancho_tablero//self.tamanio[1])
            casillaEstandar = CasillaEstandar(centros_casillas[i], (255,255,255), figura, i, self.ventana)
            self.casillas.append(casillaEstandar)

    def colorearCasillas(self):
        """
        Esta función colorea las casillas con un algoritmo que impide colores consecutivos. 
        :returns:  None -- Procedimiento sin valor de retorno.
        """
        colores_x = ["amarillo", "blanco", "rojo", "azul", "verde"]

        i = 0
        indice_color_x = 0
        indice_color_y = 0
        par_actual, par_final = 0, self.tamanio[0]
        impar_actual, impar_final = self.tamanio[0] * 2 - 1, self.tamanio[0] - 1

        # favor documentar este algoritmo
        while i < self.tamanio[1] // 2: 
            #Coloreado filas pares
            for j in range (par_actual, par_final):
                if isinstance(self.casillas[j], CasillaEstandar):
                    self.casillas[j].setColor(colores_x[indice_color_x])
                else:
                    self.casillas[j].setColor(colores_x[indice_color_x])
                
                indice_color_x += 1
                if indice_color_x > 4:
                    indice_color_x = 0

            #Coloreado filas impares
            for j in range (impar_actual, impar_final, -1):
                if isinstance(self.casillas[j], CasillaEstandar):
                    self.casillas[j].setColor(colores_x[(indice_color_x + 3) % 5])
                else:
                    self.casillas[j].setColor(colores_x[(indice_color_x + 3) % 5])
                
                indice_color_x += 1
                if indice_color_x > 4:
                    indice_color_x = 0
            
            indice_color_y += 1 
            if indice_color_y > 4:
                indice_color_y = 0

            indice_color_x = indice_color_y

            par_actual += self.tamanio[0] * 2
            par_final += self.tamanio[0] * 2

            impar_actual += self.tamanio[0] * 2
            impar_final += self.tamanio[0] * 2

            i += 1

class VistaTablero:
    """
    Esta clase representa un tablero de juego, y contiene los
    atributos y acciones necesarios para su graficación y comportamiento.
    """
    def __init__(self, controlador, tamanio, ventana, ancho_barra, es_partida_cargada):
        self.casillas = []              # lista de casillas del tablero
        self.controlador = controlador
        controlador.crear_tablero_logico(tamanio, ventana, ancho_barra, es_partida_cargada)
        if not es_partida_cargada:
            self.casillas = controlador.colorear_casillas_tablero()
            self.dibujarCasillas()

    def actualizar(self):
        """
        Funcion que se encarga de actualizar el tablero si se llegara a cargar un apartida.
        """
        casillas_nuevas = self.controlador.actualizar_tablero()
        self.casillas = casillas_nuevas
        self.dibujarCasillas()

    def dibujarCasillas(self):
        """
        Esta función dibuja las casillas y sus conectores en la ventana.
        :returns:  None -- Procedimiento sin valor de retorno.
        """
        for c in self.casillas:
            c.dibujar()             # y las estándar

        for i in Singleton.serpientes:   # para cada serpiente
            i.dibujar()             # dibújese
        
        for i in Singleton.escaleras:    # para cada escalera
            i.dibujar()             # dibújese