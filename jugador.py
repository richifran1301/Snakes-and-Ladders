import pygame
import random
from singleton import Singleton
from arbitro import Arbitro

class Jugador():
    def __init__(self,ventana,pos,x,y,a,l,mX, mY):
        self.ventana = ventana
        self.x = x
        self.y = y
        self.largo = l
        self.ancho = a
        self.pos_tablero = pos
        self.movX = mX
        self.movY = mY
        self.ganador = False
        self.rect = pygame.rect.Rect((self.x, self.y, self.ancho, self.largo))
        self.setColor()
        self.dibujar()

    def setNombre(self, nombre):
        self.nombre = nombre
    
    def setColor(self):
        salga = False
        while not salga:
            color = input("Colores disponibles:\nmagenta, azul, naranja, negro, gris, verde, aqua, dorado, rojo\nEscoja el color de su jugador: ")
            repetido = self.esColorRepetido(color)
            existe = self.existeColor(color)
            if  existe and not repetido:
                Singleton.colores_jugadores_usados.append(color)
                self.mi_color = Singleton.colores_jugadores[color]
                salga = True
            else:
                print("---Escoja un color valido--- -> escogido: ", color)
        
    def esColorRepetido(self, color):     
        if color in Singleton.colores_jugadores_usados:
            return True
        else:
            return False
    
    def existeColor(self, color):
        for llave in Singleton.colores_jugadores:
            if llave == color:
                return True
        return False
            

    def getNombre(self):
        return self.nombre    

    def mover(self, distancia, coordenadas):
        excedido = False
        coordenadasNuevoMov = []
        distanciaN = 0
        if self.pos_tablero + distancia > 99:
            excedido = True
            self.pos_tablero = self.pos_tablero + distancia-100
        
        self.rect.x = coordenadas[0] + self.movX            # + para evitar complicaciones con numeros en centro de casilla    
        self.rect.y = coordenadas[1] + self.movY             # -  para evitar posibles choques con escaleras o serpientes
       
        if not excedido:
            self.pos_tablero = self.pos_tablero + distancia
        gano = Arbitro.comprobarGane(self.pos_tablero)                          #primero comprueba si el jugador en la nueva posicion gano
        if gano == False:
            distanciaN, coordenadasNuevoMov = Arbitro.aplicarReglasMovimiento(self.pos_tablero)        #si no gano, comprueba si esta en una serp o escalera
            if distanciaN != 0: #si esta en una serpiete o escalera, va a tener que moverse a la posicion indicada
                gano = self.mover(distanciaN,coordenadasNuevoMov)
        return gano #retorna el bool si gano, para cerrar el juego

    def dibujar(self):
        pygame.draw.rect(self.ventana, self.mi_color, self.rect)
    
    