from tkinter import *
from PIL import Image, ImageTk
import random
import sys, pygame
from pygame.locals import*
import time
import os
import itertools

class Tablero:
    #def __init__(self):

    def generar_serpientes(self, escaleras, casillas):
        serpientes = []
        generados = 0
        while generados < 12: #Son 6 serpientes generadas en tuplas de 2
            while True:
                valor = random.randint(1, len(casillas) - 2)
                if (valor not in escaleras) and (valor not in serpientes):
                    serpientes.append(valor)
                    break
            generados += 1
        
        print("Serpientes: ", serpientes)
        return serpientes

    def generar_escaleras(self, casillas):

        escaleras = []
        generados = 0

        while generados < 12: #Son 6 escaleras generadas en tuplas de 2
            while True:
                valor = random.randint(1, len(casillas) - 2)
                if valor not in escaleras:
                    escaleras.append(valor)
                    break
            generados += 1

        print("Escaleras: ", escaleras)
        return escaleras

    def generar_conexines(self, casillas):

        escaleras = generar_escaleras(casillas)
        serpientes = generar_serpientes(escaleras, casillas)
        return serpientes, escaleras

    def obtener_orden_coordenadas(self, centro_casillas_x, centro_casillas_y):

        casillas = []
        temp = centro_casillas_x

        for i in range(0, len(centro_casillas_y)):
            if(i % 2 == 0):
                for j in range(len(centro_casillas_x)):
                    tupla_temp = (centro_casillas_x[j], centro_casillas_y[i])
                    casillas.append(tupla_temp)
            else:
                for k in range(len(temp)):
                    tupla_temp = (temp[k], centro_casillas_y[i])
                    casillas.append(tupla_temp)    
            temp.reverse()
        
        #print(casillas)
        return casillas

    def obtener_casillas(self, x, max_iteracion):
        centro_casillas = []    
        for i in range(max_iteracion):
            centro_casillas.append(int(x/2) + (i*x))
        return centro_casillas

    def obtener_centro_casillas(self, ancho_total, alto_total):
    
        centro_casillas = []
        centro_casillas_x = []
        centro_casillas_y = []

        cantidad_casillas_x, cantidad_casillas_y = 10, 10
        ancho_casilla = int(ancho_total/cantidad_casillas_x)
        altura_casilla = int(alto_total/cantidad_casillas_y)
    
        centro_casillas_x = obtener_casillas(ancho_casilla, cantidad_casillas_x)
        centro_casillas_y = obtener_casillas(altura_casilla, cantidad_casillas_y)
    
        centro_casillas_y.reverse()
    
        centro_casillas = obtener_orden_coordenadas(centro_casillas_x, centro_casillas_y)
    
        return centro_casillas

    def main():

        ancho, alto = 700, 700
    
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        screen = pygame.display.set_mode((ancho, alto))
        screen.fill((0,0,0))
    
        casillas = obtener_centro_casillas(ancho, alto)
    
        serpientes, escaleras = generar_conexines(casillas)
    
        for pos in casillas:
            cuadrado = pygame.Rect(pos[0] - 35, pos[1] - 35, 70, 70)
            pygame.draw.rect(screen, (0,0,0), cuadrado)
            pygame.draw.rect(screen, (200,200,200), cuadrado, 1)
    
        prev = None
        for pos in casillas:
            if prev:
                pygame.draw.line(screen, (255,255,255), prev, pos, 4)
            prev = pos
    
        for i in range(0, len(serpientes), 2):
            pygame.draw.line(screen, (255,0,0), casillas[serpientes[i]], casillas[serpientes[i+1]], 4)
        
        for i in range(0, len(escaleras), 2):
            pygame.draw.line(screen, (0,128,0), casillas[escaleras[i]], casillas[escaleras[i+1]], 4)

        while True:
            for events in pygame.event.get():
                if events.type == QUIT:
                    sys.exit(0)
          
    main()