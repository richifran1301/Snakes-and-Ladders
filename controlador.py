import sys, pygame
import os
from pygame.locals import *
from button import Button
from sidebar import Sidebar
from conector import Conector, ConectorEstandar, Escalera, Serpiente
from casilla import Casilla, CasillaEstandar, CasillaEscalera, CasillaSerpiente
from dado import Dado
from jugador import Jugador
from tablero import Tablero
from singleton import Singleton


ANCHO_BARRA = 250
ANCHO = 700 + ANCHO_BARRA
ALTO = 700
CANTIDAD_X = 10
CANTIDAD_Y = 10

def genere_ventana_pygame():
    #Pygame condiciones iniciales
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Serpientes y escaleras")

    #ruta_local = os.path.dirname(__file__)
    #ruta_icono = os.path.join(ruta_local, "000.jpg")
    #icono = pygame.image.load(ruta_icono)
    #pygame.display.set_icon(icono)

    #Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>

    os.environ['SDL_VIDEO_CENTERED'] = '1'
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    #ventana.fill((0,0,0))

    assert (ANCHO - ANCHO_BARRA) % CANTIDAD_X == 0 and ALTO % CANTIDAD_Y == 0

    return ventana

def genere_tablero(_ventana):
    t = Tablero((CANTIDAD_X, CANTIDAD_Y), _ventana, ANCHO_BARRA)
    t.colorearCasillas()
    t.dibujarCasillas()
    return t

def genere_dados(_ventana):
    boton_dados = Button(_ventana, (255,255,255), 750, 35, 150, 40, "Lanzar dados")
    dado = Dado(_ventana)
    elementos_sidebar = [boton_dados, dado]
    sidebar = Sidebar(_ventana, 700, 700, 250, (255,255,255), elementos_sidebar)
    return boton_dados,dado,elementos_sidebar,sidebar

def agregue_jugadores(cant_jugadores, tablero,  _ventana):
    #TODO agregar diferencias de jugador. Como color
    for _ in range(cant_jugadores):
        jugador = Jugador(_ventana, 0, tablero.casillas[0].getCoordenadas()[0] + ((Singleton.getAlto()//Singleton.getCantX())//6),
                    tablero.casillas[0].getCoordenadas()[1] - ((Singleton.getAlto()//Singleton.getCantY())//6),
                    (ALTO//CANTIDAD_X)//4, (ALTO/CANTIDAD_Y)//4)
        Singleton.agregar_jugador(jugador)

def juegue(jugador, boton_dados, dado, tablero, Singleton): #ESTE ES EL TURNO DE UN SOLO JUGADOR, QUE RECIBE POR PARAMETRO
    #clock.tick(40)                          #TODO buscar mas info sobre el uso
        boton_dados.dibujar()
        pygame.display.update()
        resultado_dados = 0
        gano = False
        for events in pygame.event.get():
            posicion_cursor = pygame.mouse.get_pos()

            if events.type == QUIT:
                pygame.quit()
                sys.exit(0)

            elif events.type == pygame.MOUSEBUTTONDOWN:
                if boton_dados.isOver(posicion_cursor):
                    resultado_dados = dado.lanzar()     # esta variable contiene ahora el numero que lanzaron los dados. usar donde se necesite.

            elif events.type == pygame.MOUSEMOTION:

                if boton_dados.isOver(posicion_cursor):
                    boton_dados.mi_color = (161,222,147)
                else:
                    boton_dados.mi_color = (54,57,63)
            if resultado_dados > 0:
                tablero.limpar_casilla(jugador.pos_tablero)           #limpia ficha de jugador
                coordenadas = tablero.obtener_destino(jugador.pos_tablero, resultado_dados)
                gano = jugador.mover(resultado_dados, coordenadas)

            #dibuja todos los jugadores en el tablero    
            Singleton.dibujar_jugadores()
        return gano

def run():
    #Inicializa Ventana de Pygame
    ventana = genere_ventana_pygame()
    gano = False
    jugadorGanador = 0
   
    #Inicializa tablero
    tablero = genere_tablero(ventana)
    POS_GANADORA = (CANTIDAD_X * CANTIDAD_Y)-1
    #Inicializa Singleton
    Singleton.init(ANCHO, ALTO, CANTIDAD_X, CANTIDAD_Y, POS_GANADORA, tablero.casillas) #el singleton guarda las coordenadas de la casilla 100
    #Inicializa dados
    boton_dados,dado,elementos_sidebar,sidebar = genere_dados(ventana)

    #Inicializa jugador
    agregue_jugadores(1, tablero, ventana)
    while gano == False: # mientras no haya un ganador, siguen los turnos
        for jugador in Singleton.jugadores: #recorre el vector de jugadores, y le da el turno a cada uno
           gano = juegue(jugador, boton_dados, dado, tablero, Singleton)#manda al jugador por el cual va iterando a que realice su jugada
           if gano == True:#comprueba si ese jugador gano y cierra el programa, dando el nombre del ganador
                jugadorGanador = jugador.getNombre()
                break
    
    print("EL JUGADOR GANADOR ES: ", jugadorGanador) 
    pygame.quit()
    sys.exit(0)
    
run() 