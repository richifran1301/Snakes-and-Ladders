import pygame
import random
from singleton import Singleton
from arbitro import Arbitro
from inventario import Inventario, Ficha, ElementoInventario

class Jugador():
    """
    Esta clase corresponde a la del Jugador que participa en el juego. Realiza las 
    interacciones dadas por el usuario y depende totalmente de el. Van a haber entre 2 
    a 4 jugadores por juego.
    """
    def __init__(self,pos,x,y,a,l,mX, mY):
        """
        :param x: coordenada en X donde se posicionara el jugador
        :type x: int
        :param y: coordenada en Y donde se posicionara el jugador
        :type y: int
        :param a: medida del ancho del jugador
        :type a: int
        :param l: medida de la altura del jugador
        :type l: int
        :param mX: es que tanto tiene que moverse en X este jugador en especifico, para
        estar en una posicion despecifica en la casilla. Por ejemplo para quedar en una 
        esquina de abajo, o la de arriba...
        :type mX: int
        :param mY: es que tanto tiene que moverse en Y este jugador en especifico, para
        estar en una posicion despecifica en la casilla. Por ejemplo para quedar en una 
        esquina de abajo, o la de arriba...
        :type mY: int
        """
        self.x = x
        self.y = y
        self.largo = l
        self.ancho = a
        self.pos_tablero = pos
        self.movX = mX
        self.movY = mY
        self.inventario = Inventario()
        self.ganador = False
        self.crear_ficha()
        if not Singleton.es_partida_cargada:
            Singleton.cantidad_jugadores += 1
            self.setNombre("Jugador " + str(Singleton.cantidad_jugadores))
            Arbitro.setColorJugador(self)

    def crear_ficha(self):
        rect = pygame.rect.Rect((self.x, self.y, self.ancho, self.largo))
        ficha = Ficha(rect)
        self.rel_ficha = ficha
        self.inventario.agregar(ficha, 1)

    def setNombre(self, nombre):
        """
        Metodo que se encarga de darle nombre al Jugador y almacenarlo en la variable nombre.
        :param nombre: nombre para ponerle al Jugador
        :type nombre: string
        """
        self.nombre = nombre
        

    def getNombre(self):
        """
        Metodo que va a devolver el nombre del Jugador.
        :returns: nombre del jugador, es tipo string.
        """
        return self.nombre    

    def mover(self, distancia, coordenadas):
        """
        Metodo que se encarga de realizar el movimiento del jugador y requiere de la participacion del
        Arbitro para saber si: gano; si cayo en una escalera o serpiente y necesita moverse (tampoco sabe
        adonde habria que moverse, el Arbitro le indica);y por ultimo, si ya no tiene que moverse mas.
        :param distancia: cantidad de casillas a moverse, puede ser el numero que salio en los dados, o
        puede ser lo que debe moverse por haber caido en escalera o serpiente.
        :type distancia: int
        :param coordenadas: coordenadas en X y Y de la casilla (especificamente en el centro de ella) adonde 
        el Jugador tiene que moverse.
        :type coordenadas: tupla de int
        """
        excedido = False
        coordenadasNuevoMov = []
        distanciaN = 0
        if self.pos_tablero + distancia > 99:
            excedido = True
            self.pos_tablero = self.pos_tablero + distancia-100

        self.rel_ficha.mover(coordenadas[0] + self.movX, coordenadas[1] + self.movY)
       
        if not excedido:
            self.pos_tablero = self.pos_tablero + distancia
        Arbitro.comprobarGane(self.pos_tablero)                          #primero comprueba si el jugador en la nueva posicion gano
        if Arbitro.jugador_gano == False:
            distanciaN, coordenadasNuevoMov = Arbitro.aplicarReglasMovimiento(self.pos_tablero)        #si no gano, comprueba si esta en una serp o escalera
            if distanciaN != 0: #si esta en una serpiete o escalera, va a tener que moverse a la posicion indicada
                self.mover(distanciaN, coordenadasNuevoMov)

    

class VistaJugador():
    """
    Esta clase corresponde a la Vista del Jugador que participa en el juego. Lo va a dibujar en la pantalla de pygame
    para que pueda ser visible para los usuarios.
    """
    def __init__(self, jugador):
        """
        :param jugador: Objeto de jugador, que sera a quien tiene que dibujar. Es un jugador fijo, como una relacion 1 a 1.
        """
        self.jugador = jugador

    def muestre_turno_jugador(self):
        """
        Este metodo se va a encargar de desplegar en la ventana de pygame que jugador
        le toca jugar. El texto lo muestra en el color respectivo de cada jugador. 
        :param jugador: Objeto de jugador a realizar turno.
        :type jugador: Jugador object
        """
        X = 1650
        Y = 600
        font = pygame.font.Font('freesansbold.ttf', 20) 
        text = font.render('Turno: ' + self.jugador.nombre, True, self.jugador.mi_color, Singleton.colores_casillas["blanco"]) 
        textRect = text.get_rect()  
        textRect.center = (X // 2, Y // 2) 
        Singleton.ventana.blit(text, textRect)

    def dibujar(self):
        """
        Metodo que ilustra al jugador en la vetana de pygame. Lo dibuja para que el usuario
        pueda observarlo.
        """
        pygame.draw.rect(Singleton.ventana, self.jugador.mi_color, self.jugador.rel_ficha.figura)