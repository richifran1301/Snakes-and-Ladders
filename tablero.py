import os
import time
import random
import itertools
import sys, pygame
from tkinter import *
from pygame.locals import *
from PIL import Image, ImageTk
from casilla import Casilla, CasillaEstandar, CasillaEscalera, CasillaSerpiente
from conector import Conector, ConectorEstandar, Escalera, Serpiente

class Tablero():
    def __init__(self, tamanio, ventana):
        self.tamanio = tamanio # x * y = z
        self.ventana = ventana
        self.casillas = []
        self.serpientes = []
        self.escaleras = []
        self.generarCasillas()

    def generarCasillas(self):
        
        alto, ancho = 700, 700 # del tablero
        
        cantidad_serpientes = int((self.tamanio[0] * self.tamanio[1]) * ((random.randint(5, 7)) * 0.01))
        cantidad_escaleras = int((self.tamanio[0] * self.tamanio[1]) * ((random.randint(5, 7)) * 0.01))

        centros_casillas = self.obtener_centro_casillas(alto, ancho)
        
        posiciones_serpientes, posiciones_escaleras = self.generar_conexiones(centros_casillas, cantidad_serpientes, cantidad_escaleras)

        for i in range(len(centros_casillas)):
            encontrado = False
            for j in range(len(posiciones_serpientes)):
                if not encontrado and i in posiciones_serpientes[j]:
                    figura = pygame.Rect(centros_casillas[i][0] - int((alto/self.tamanio[0])/2), centros_casillas[i][1] - int((ancho/self.tamanio[1])/2), alto/self.tamanio[0], ancho/self.tamanio[1])
                    temp = CasillaEstandar(centros_casillas[i], (255,255,255), figura, i, self.ventana)
                    serpiente = CasillaSerpiente(temp)
                    self.casillas.append(serpiente)
                    encontrado = True
                if encontrado:
                    break

            for k in range(len(posiciones_escaleras)):
                if not encontrado and i in posiciones_escaleras[k]:
                    figura = pygame.Rect(centros_casillas[i][0] - int((alto/self.tamanio[0])/2), centros_casillas[i][1] - int((ancho/self.tamanio[1])/2), alto/self.tamanio[0], ancho/self.tamanio[1])
                    temp = CasillaEstandar(centros_casillas[i], (255,255,255), figura, i, self.ventana)
                    escalera = CasillaEscalera(temp)
                    self.casillas.append(escalera)
                    encontrado = True
                if encontrado:
                    break

            if not encontrado:
                figura = pygame.Rect(centros_casillas[i][0] - int((alto/self.tamanio[0])/2), centros_casillas[i][1] - int((ancho/self.tamanio[1])/2), alto/self.tamanio[0], ancho/self.tamanio[1])
                casillaEstandar = CasillaEstandar(centros_casillas[i], (255,255,255), figura, i, self.ventana)
                self.casillas.append(casillaEstandar)

        for i in self.casillas:
            if isinstance(i, CasillaSerpiente):
                if not self.existeConexion(i.casilla.getIndice()):
                    conector = ConectorEstandar(self.getPar(i.casilla.getIndice(), posiciones_serpientes), self.ventana)
                    self.serpientes.append(Serpiente(conector))

            elif isinstance(i, CasillaEscalera):
                if not self.existeConexion(i.casilla.getIndice()):
                    conector = ConectorEstandar(self.getPar(i.casilla.getIndice(), posiciones_escaleras), self.ventana)
                    self.escaleras.append(Escalera(conector))

    def getPosicionesEnTupla(self, indice, posiciones):
        #print("Indice: ", indice, "\n", "Posiciones: ", posiciones)
        for i in posiciones:
            if indice in i:
                #print("i = ", i)
                return i
        return

    def getPar(self, indice, posiciones):
        temp_par = self.getPosicionesEnTupla(indice, posiciones)

        tupla = (self.casillas[temp_par[0]], self.casillas[temp_par[1]])

        return tupla

    def existeConexion(self, indice):

        for i in range(len(self.serpientes)):
            if indice == self.serpientes[i].conector.getCasillaInicio().casilla.getIndice() or indice == self.serpientes[i].conector.getCasillaFinal().casilla.getIndice():
                return True

        for i in range(len(self.escaleras)):
            if indice == self.escaleras[i].conector.getCasillaInicio().casilla.getIndice() or indice == self.escaleras[i].conector.getCasillaFinal().casilla.getIndice():
                return True

        return False

    def generar_serpientes(self, escaleras, casillas, cantidad):
        serpientes_temp = []
        generados = 0
        while generados < cantidad * 2: #Son cantidad serpientes generadas en tuplas de 2
            while True:
                valor = random.randint(1, len(casillas) - 2)
                if (valor not in escaleras) and (valor not in serpientes_temp):
                    serpientes_temp.append(valor)
                    break
            generados += 1
        
        return serpientes_temp

    def generar_escaleras(self, casillas, cantidad):
        escaleras_temp = []
        generados = 0

        while generados < cantidad * 2: #Son cantidad escaleras generadas en tuplas de 2
            while True:
                valor = random.randint(1, len(casillas) - 2)
                if valor not in escaleras_temp:
                    escaleras_temp.append(valor)
                    break
            generados += 1

        return escaleras_temp

    def generar_conexiones(self, casillas, cantidad_serpientes, cantidad_escaleras):

        escaleras_temp = self.generar_escaleras(casillas, cantidad_escaleras)
        serpientes_temp = self.generar_serpientes(escaleras_temp, casillas, cantidad_serpientes)

        escaleras = []
        serpientes = []

        for i in range(0, len(escaleras_temp), 2):
            tupla = (escaleras_temp[i], escaleras_temp[i+1])
            escaleras.append(tupla)

        for i in range(0, len(serpientes_temp), 2):
            tupla = (serpientes_temp[i], serpientes_temp[i+1])
            #print(tupla)
            serpientes.append(tupla)

        #print("Escaleras: ", escaleras)
        #print("Serpientes: ", serpientes)

        return serpientes, escaleras

    def obtener_orden_coordenadas(self, centro_casillas_x, centro_casillas_y):

        casillas_temp = []
        temp = centro_casillas_x

        for i in range(0, len(centro_casillas_y)):
            if(i % 2 == 0):
                for j in range(len(centro_casillas_x)):
                    tupla_temp = (centro_casillas_x[j], centro_casillas_y[i])
                    casillas_temp.append(tupla_temp)
            else:
                for k in range(len(temp)):
                    tupla_temp = (temp[k], centro_casillas_y[i])
                    casillas_temp.append(tupla_temp)
            temp.reverse()
        
        return casillas_temp

    def obtener_casillas(self, x, max_iteracion):
        centro_casillas = []    
        for i in range(max_iteracion):
            centro_casillas.append(int(x/2) + (i*x))
        return centro_casillas

    def obtener_centro_casillas(self, ancho_total, alto_total):
    
        centro_casillas = []
        centro_casillas_x = []
        centro_casillas_y = []

        cantidad_casillas_x, cantidad_casillas_y = self.tamanio[0], self.tamanio[1]
        ancho_casilla = int(ancho_total/cantidad_casillas_x)
        altura_casilla = int(alto_total/cantidad_casillas_y)
    
        centro_casillas_x = self.obtener_casillas(ancho_casilla, cantidad_casillas_x)
        centro_casillas_y = self.obtener_casillas(altura_casilla, cantidad_casillas_y)
    
        centro_casillas_y.reverse()
    
        centro_casillas = self.obtener_orden_coordenadas(centro_casillas_x, centro_casillas_y)
    
        return centro_casillas

    def colorearCasillas(self):
        colores_x = ["amarillo", "blanco", "rojo", "azul", "verde"]

        i = 0
        indice_color_x = 0
        indice_color_y = 0
        par_actual, par_final = 0, self.tamanio[0]
        impar_actual, impar_final = self.tamanio[0] * 2 - 1, self.tamanio[0] - 1

        while i < self.tamanio[1] // 2: 
            #Coloreado filas pares
            for j in range (par_actual, par_final):
                if isinstance(self.casillas[j], CasillaEstandar):
                    self.casillas[j].setColor(colores_x[indice_color_x])
                else:
                    self.casillas[j].casilla.setColor(colores_x[indice_color_x])
                
                indice_color_x += 1
                if indice_color_x > 4:
                    indice_color_x = 0

            #Coloreado filas impares
            for j in range (impar_actual, impar_final, -1):
                if isinstance(self.casillas[j], CasillaEstandar):
                    self.casillas[j].setColor(colores_x[(indice_color_x + 3) % 5])
                else:
                    self.casillas[j].casilla.setColor(colores_x[(indice_color_x + 3) % 5])
                
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
 
        return

    def dibujarCasillas(self):

        for c in self.casillas:
            if isinstance(c, CasillaSerpiente) or isinstance(c, CasillaEscalera):
                c.casilla.dibujar()
            else:
                c.dibujar()

        """
        casilla_previa = None
        for casilla_actual in self.casillas:
            if casilla_previa:
                if (isinstance(casilla_previa, CasillaEscalera) or isinstance(casilla_previa, CasillaSerpiente)) and (isinstance(casilla_actual, CasillaEstandar)):
                    pygame.draw.line(self.ventana, (0,0,0), casilla_previa.casilla.getCoordenadas(), casilla_actual.getCoordenadas(), 4)

                elif (isinstance(casilla_previa, CasillaEstandar)) and (isinstance(casilla_actual, CasillaSerpiente) or isinstance(casilla_actual, CasillaEscalera)):
                    pygame.draw.line(self.ventana, (0,0,0), casilla_previa.getCoordenadas(), casilla_actual.casilla.getCoordenadas(), 4)

                elif isinstance(casilla_previa, CasillaEstandar) and isinstance(casilla_actual, CasillaEstandar):
                    pygame.draw.line(self.ventana, (0,0,0), casilla_previa.getCoordenadas(), casilla_actual.getCoordenadas(), 4)

                elif (isinstance(casilla_previa, CasillaEscalera) or isinstance(casilla_previa, CasillaSerpiente)) and (isinstance(casilla_actual, CasillaSerpiente) or isinstance(casilla_actual, CasillaEscalera)):
                    pygame.draw.line(self.ventana, (0,0,0), casilla_previa.casilla.getCoordenadas(), casilla_actual.casilla.getCoordenadas(), 4)

            casilla_previa = casilla_actual
        """

        for i in self.serpientes:
            i.dibujar()
        
        for i in self.escaleras:
            i.dibujar()

def main():

    ancho, alto = 700, 700

    pygame.init()

    os.environ['SDL_VIDEO_CENTERED'] = '1'
    ventana = pygame.display.set_mode((ancho, alto))
    #ventana.fill((0,0,0))

    t = Tablero((10, 10), ventana)
    t.colorearCasillas()
    t.dibujarCasillas()

    while True:
        for events in pygame.event.get():
            if events.type == QUIT:
                sys.exit(0)

main()