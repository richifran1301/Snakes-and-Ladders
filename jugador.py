import pygame
from singleton import Singleton

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
        if self.pos_tablero + distancia > 99:
            excedido = True
            self.pos_tablero = self.pos_tablero + distancia-100
        
        self.rect.x = coordenadas[0] + ((Singleton.getAlto()//Singleton.getCantX())//6)             # + para evitar complicaciones con numeros en centro de casilla    
        self.rect.y = coordenadas[1]- ((Singleton.getAlto()//Singleton.getCantY())//6)              # -  para evitar posibles choques con escaleras o serpientes
        if not excedido:
            self.pos_tablero += distancia

    def dibujar(self):
        pygame.draw.rect(self.ventana, (0, 0, 128), self.rect)
    
    