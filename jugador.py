import pygame
from singleton import Singleton
from arbitro import Arbitro

class Jugador():
    def __init__(self,ventana,pos,x,y,a,l):
        self.ventana = ventana
        self.x = x
        self.y = y
        self.largo = l
        self.ancho = a
        self.pos_tablero = pos
        self.ganador = False
        self.rect = pygame.rect.Rect((self.x, self.y, self.ancho, self.largo))
        self.dibujar()

    def setNombre(self, nombre):
        self.nombre = nombre

    def getNombre(self):
        return self.nombre    

    def mover(self, distancia, coordenadas):
        excedido = False
        coordenadasNuevoMov = []
        distanciaN = 0
        if self.pos_tablero + distancia > 99:
            excedido = True
            self.pos_tablero = self.pos_tablero + distancia-100
        
        self.rect.x = coordenadas[0] + ((Singleton.getAlto()//Singleton.getCantX())//6)             # + para evitar complicaciones con numeros en centro de casilla    
        self.rect.y = coordenadas[1]- ((Singleton.getAlto()//Singleton.getCantY())//6)              # -  para evitar posibles choques con escaleras o serpientes
       
        if not excedido:
            print("DISTANCIA EN JUGADOR: ",distancia)
            self.pos_tablero = self.pos_tablero + distancia
        gano = Arbitro.comprobarGane(self.pos_tablero)                          #primero comprueba si el jugador en la nueva posicion gano
        if gano == False:
            distanciaN, coordenadasNuevoMov = Arbitro.aplicarReglas(self.pos_tablero)        #si no gano, comprueba si esta en una serp o escalera
            if distanciaN != 0: #si esta en una serpiete o escalera, va a tener que moverse a la posicion indicada
                gano = self.mover(distanciaN,coordenadasNuevoMov)
        return gano #retorna el bool si gano, para cerrar el juego

    def dibujar(self):
        pygame.draw.rect(self.ventana, (0, 0, 128), self.rect)
    
    