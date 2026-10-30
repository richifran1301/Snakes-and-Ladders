import os
import math
import time
import random
import itertools
import sys, pygame
from pygame.locals import *
from abc import ABC, abstractmethod
from elementoTablero import ElementoTablero
from casilla import CasillaSE, CasillaEstandar, CasillaEscalera, CasillaSerpiente

# parametros graficos de las escaleras
MEDIO_ANCHO_ESCALERA = 9
SEPARACION_PELDANIOS = 16
COLOR_RIEL = (150,95,40)
COLOR_PELDANIO = (196,140,80)
COLOR_BORDE_MADERA = (70,40,15)

# parametros graficos de las serpientes
AMPLITUD_SERPIENTE = 12
LARGO_ONDA_SERPIENTE = 110
RADIO_CUERPO_SERPIENTE = 7
RADIO_COLA_SERPIENTE = 2
RADIO_CABEZA_SERPIENTE = 9
COLOR_BORDE_SERPIENTE = (30,30,30)
COLOR_LENGUA = (200,0,0)
COLORES_SERPIENTES = [((60,150,60), (230,200,40)),      # (color del cuerpo, color de las manchas)
                      ((200,60,40), (250,220,120)),
                      ((120,60,160), (240,170,220)),
                      ((40,110,180), (250,250,250))]

def vectorUnitario(inicio, final):
    """
    Calcula la dirección y la distancia entre dos puntos.
    :param inicio: Punto (x, y) de partida.
    :type inicio: tuple
    :param final: Punto (x, y) de llegada.
    :type final: tuple
    :returns:  tuple -- (ux, uy, largo) con el vector unitario de inicio a final y su largo en píxeles.
    """
    dx, dy = final[0] - inicio[0], final[1] - inicio[1]
    largo = math.hypot(dx, dy) or 1
    return dx / largo, dy / largo, largo

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
        Este método dibuja el conector como una escalera (dos rieles con peldaños) en la ventana de pygame.
        :returns:  None -- Procedimiento sin valor de retorno.
        """
        x0, y0 = self.getCasillaInicio().getCoordenadas()
        x1, y1 = self.getCasillaFinal().getCoordenadas()
        ux, uy, largo = vectorUnitario((x0, y0), (x1, y1))
        px, py = -uy * MEDIO_ANCHO_ESCALERA, ux * MEDIO_ANCHO_ESCALERA     # desplazamiento perpendicular hacia cada riel

        # peldaños primero, para que los rieles queden por encima
        cantidad_peldanios = max(2, int(largo // SEPARACION_PELDANIOS))
        for i in range(1, cantidad_peldanios):
            t = i / cantidad_peldanios
            cx, cy = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            pygame.draw.line(self.getVentana(), COLOR_BORDE_MADERA, (cx - px, cy - py), (cx + px, cy + py), 5)
            pygame.draw.line(self.getVentana(), COLOR_PELDANIO, (cx - px, cy - py), (cx + px, cy + py), 3)

        for signo in (-1, 1):
            inicio = (x0 + px * signo, y0 + py * signo)
            final = (x1 + px * signo, y1 + py * signo)
            pygame.draw.line(self.getVentana(), COLOR_BORDE_MADERA, inicio, final, 7)
            pygame.draw.line(self.getVentana(), COLOR_RIEL, inicio, final, 4)

class Serpiente(ConectorSE):
    """
    Esta clase representa un conector entre dos casillas de tablero, y contiene los
    atributos y acciones necesarios para su comportamiento en un tablero de juego.
    """

    def __init__(self, casilla, ventana):
        super().__init__(casilla, ventana)

    def dibujar(self):
        """
        Este método dibuja el conector como una serpiente ondulada en la ventana de pygame,
        con la cabeza en la casilla de inicio y la cola en la casilla final.
        :returns:  None -- Procedimiento sin valor de retorno.
        """
        cabeza = self.getCasillaInicio().getCoordenadas()
        cola = self.getCasillaFinal().getCoordenadas()
        ux, uy, largo = vectorUnitario(cabeza, cola)
        px, py = -uy, ux
        ondas = max(1, round(largo / LARGO_ONDA_SERPIENTE))
        color, color_manchas = COLORES_SERPIENTES[self.getCasillaInicio().getIndice() % len(COLORES_SERPIENTES)]

        # puntos del cuerpo como (x, y, radio), desde la cabeza (t = 0) hasta la cola (t = 1)
        cantidad_puntos = max(2, int(largo // 2))
        cuerpo = []
        for i in range(cantidad_puntos + 1):
            t = i / cantidad_puntos
            desvio = AMPLITUD_SERPIENTE * math.sin(2 * math.pi * ondas * t)
            x = cabeza[0] + (cola[0] - cabeza[0]) * t + px * desvio
            y = cabeza[1] + (cola[1] - cabeza[1]) * t + py * desvio
            radio = RADIO_CUERPO_SERPIENTE - (RADIO_CUERPO_SERPIENTE - RADIO_COLA_SERPIENTE) * t
            cuerpo.append((x, y, radio))

        # se dibuja de la cola a la cabeza para que la parte gruesa quede encima
        for x, y, radio in reversed(cuerpo):
            pygame.draw.circle(self.getVentana(), COLOR_BORDE_SERPIENTE, (int(x), int(y)), int(radio) + 2)
        for i, (x, y, radio) in enumerate(reversed(cuerpo)):
            relleno = color_manchas if (i // 6) % 3 == 0 else color
            pygame.draw.circle(self.getVentana(), relleno, (int(x), int(y)), int(radio))

        # cabeza mirando en dirección contraria al cuerpo
        hx, hy = cabeza
        lengua = (hx - ux * (RADIO_CABEZA_SERPIENTE + 8), hy - uy * (RADIO_CABEZA_SERPIENTE + 8))
        pygame.draw.line(self.getVentana(), COLOR_LENGUA, (hx, hy), lengua, 2)
        pygame.draw.line(self.getVentana(), COLOR_LENGUA, lengua, (lengua[0] - ux * 4 + px * 3, lengua[1] - uy * 4 + py * 3), 2)
        pygame.draw.line(self.getVentana(), COLOR_LENGUA, lengua, (lengua[0] - ux * 4 - px * 3, lengua[1] - uy * 4 - py * 3), 2)
        pygame.draw.circle(self.getVentana(), COLOR_BORDE_SERPIENTE, (int(hx), int(hy)), RADIO_CABEZA_SERPIENTE + 2)
        pygame.draw.circle(self.getVentana(), color, (int(hx), int(hy)), RADIO_CABEZA_SERPIENTE)
        for signo in (-1, 1):
            ojo = (int(hx - ux * 4 + px * 5 * signo), int(hy - uy * 4 + py * 5 * signo))
            pygame.draw.circle(self.getVentana(), (255,255,255), ojo, 3)
            pygame.draw.circle(self.getVentana(), (0,0,0), ojo, 1)