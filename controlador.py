import sys, pygame
import os
import time
from pygame.locals import *
from button import Button
from sidebar import Sidebar
from conector import Conector, ConectorEstandar, Escalera, Serpiente
from casilla import Casilla, CasillaEstandar, CasillaEscalera, CasillaSerpiente
from dado import Dado
from jugador import Jugador
from tablero import Tablero
from singleton import Singleton
from arbitro import Arbitro


ANCHO_BARRA = 250
ANCHO = 700 + ANCHO_BARRA
ALTO = 700
CANTIDAD_X = 10
CANTIDAD_Y = 10

def genere_ventana_pygame():
    """
    Esta funcion genera la ventana grafica de pygame. Para poder hacerle 
    modificaciones luego.
    :returns: pygame window object -- Devuelve la ventana grafica recien creada
    """
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Serpientes y escaleras")
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    assert (ANCHO - ANCHO_BARRA) % CANTIDAD_X == 0 and ALTO % CANTIDAD_Y == 0
    return ventana

def genere_tablero(ventana):
    """
    Llama el constructor de Tablero y sus metodos para generar tanto las casillas, como 
    las serpientes y escaleras respectivas en estas casillas.
    :param _ventana: Ventana grafica del juego
    :type _ventana: pygame window object
    :returns: Tablero object -- Devuelve el objeto de tablero recien creado para luego
    utilizar sus metodos en otras funciones.
    """
    t = Tablero((CANTIDAD_X, CANTIDAD_Y),ventana,ANCHO_BARRA)
    t.colorearCasillas()
    t.dibujarCasillas()
    return t

def genere_dados():
    """
    Llama el constructor de Dado y sus metodos para agregar el icono de los 
    dados en pantalla y poder obtener el resultado aleatorio que ellos generen.
    :param _ventana: Ventana grafica del juego
    :type _ventana: pygame window object
    :returns: tuple -- Devuelve como tupla el objeto de Button, que va a ser el boton 
    grafico de los dados, de primero y de segundo, el objeto de Dado para poder utilizar sus funciones.
    """
    boton_dados = Button(Singleton.ventana, Singleton.colores_casillas["blanco"], 750, 35, 150, 40, "Lanzar dados")
    dado = Dado()
    elementos_sidebar = [boton_dados, dado]
    Sidebar(700, 700, 250, Singleton.colores_casillas["blanco"], elementos_sidebar)
    return boton_dados, dado

def dibujar_jugadores():
    """
    Metodo del controlador que llama a cada jugador presente en el tablero a dibujarse en la ventana
    de pygame para que pueda seguir siendo visible en el jueego.
    """
    for jugador in Singleton.jugadores:
        jugador.dibujar()


def juegue(jugador, boton_dados, dado, tablero):
    """
    Este es el metodo principal del controlador que se va a encargar de hacer un turno
    del jugador que se reciba por parametro. Por lo que, este metodo va a estar dentro de un ciclo que
    va a representar la duracion del juego.
    :param jugador: Objeto de jugador a realizar turno.
    :type jugador: Jugador object
    :param boton_dados: El boton grafico en la ventana de pygame.
    :type boton_dados: Button object.
    :param dado: Objeto de Dado que va a tener sus respectivas funciones.
    :type dado: Dado object
    :param tablero: Objeto de Tablero que va a tener sus respectivas funciones.
    :type tablero: Tablero object
    :returns: bool -- Devuelve si el jugador, haciendo el turno actual, gano o no.
    """
    gano = False
    muestre_turno_jugador(jugador)
    resultado_dados = dado.espere_repuesta_dados(boton_dados)
    muestre_presionar_espacio()
    coordenadas = Arbitro.obtener_destino(jugador.pos_tablero, resultado_dados)
    gano = jugador.mover(resultado_dados, coordenadas)
    return gano


def muestre_turno_jugador(jugador):
    """
    Este metodo se va a encargar de desplegar en la ventana de pygame que jugador
    le toca jugar. El texto lo muestra en el color respectivo de cada jugador. 
    :param jugador: Objeto de jugador a realizar turno.
    :type jugador: Jugador object
    """
    X = 1650
    Y = 600
    font = pygame.font.Font('freesansbold.ttf', 20) 
    text = font.render('Turno: ' + jugador.nombre, True, jugador.mi_color, Singleton.colores_casillas["blanco"]) 
    textRect = text.get_rect()  
    textRect.center = (X // 2, Y // 2) 
    Singleton.ventana.blit(text, textRect)

def muestre_presionar_espacio():
    """
    Este metodo se va a encargar de desplegar en la ventana de pygame que
    el usuario necesita presionar la tecla espacio para mover la ficha. Esto
    lo hace al final de cada turno.
    """
    X = 1650
    Y = 1000
    font = pygame.font.Font('freesansbold.ttf', 15) 
    text = font.render('Presione "SPACE" para moverse', True, Singleton.colores_casillas["rojo"], Singleton.colores_casillas["blanco"]) 
    textRect = text.get_rect()  
    textRect.center = (X // 2, Y // 2) 
    Singleton.ventana.blit(text, textRect)
    pygame.display.update()


def muestre_mensaje_ganador():
    """
    Este metodo se va a encargar de desplegar en la ventana de pygame
    el usuario ganador durante 4 segundos,  antes de que se cierre el juego.
    """
    X = 1650
    Y = 800
    font = pygame.font.Font('freesansbold.ttf', 15) 
    text = font.render("El jugador ganador es: "+ str(Singleton.getJugadorGanador()), True, Singleton.colores_casillas["azul"], Singleton.colores_casillas["blanco"]) 
    textRect = text.get_rect()  
    textRect.center = (X // 2, Y // 2) 
    Singleton.ventana.blit(text, textRect)
    pygame.display.update()
    time.sleep(4)                   #4 segundos para que los demas jugadores puedan apreciar al ganador


def espere_boton_espacio():
    """
    Este metodo se encarga tener el programa "en espera" hasta que el usuario
    presione la tecla de espacio. Esto para proseguir con el turno.
    """
    condicion = True
    while condicion:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                dibujar_jugadores()
                condicion = False


def run():
    """
    Metodo main que va a correr todo el programa.
    """
    gano = False
    jugadorGanador = 0
    cantidad_jugadores = 0

    #Inicializa Ventana de Pygame
    ventana = genere_ventana_pygame()

    #Inicializa tablero
    tablero = genere_tablero(ventana)
    POS_GANADORA = (CANTIDAD_X * CANTIDAD_Y)-1

    #Inicializa Singleton
    Singleton.init(ANCHO, ALTO, CANTIDAD_X, CANTIDAD_Y, POS_GANADORA, tablero.casillas, ventana) 
    Singleton.establecer_pos_jugadores()

    #Inicializa dados
    boton_dados,dado = genere_dados()

    #TODO try and except
    while True:
        try:
            cantidad_jugadores = int(input("Ingrese la cantidad de jugadores: "))
        except:
            print("Tiene que ser un numero")
        if cantidad_jugadores > 1 and cantidad_jugadores < 5:
            break
    
    #Inicializa jugadores
    for i in range(cantidad_jugadores):
        jugador = Jugador(0, Singleton.getPosJugadores(i)[0], Singleton.getPosJugadores(i)[1],
                        (Singleton.getAlto()//Singleton.getCantX())//4, (Singleton.getAlto()/Singleton.getCantY())//4,
                        Singleton.getPosJugadores(i)[0] - Singleton.casillasTablero[0].getCoordenadas()[0],
                        Singleton.getPosJugadores(i)[1] - Singleton.casillasTablero[0].getCoordenadas()[1])
        Arbitro.reporte_jugadores(jugador)

    #Inicializa arbitro
    Arbitro.init()

    #Decidir turnos
    Arbitro.decidir_turnos(cantidad_jugadores, boton_dados, dado)
    
    print("Orden de jugadores: ", end="\n")
    for i in Singleton.jugadores_ordenados:
        print(i.nombre)

    while gano == False: # mientras no haya un ganador, siguen los turnos
        for jugador in Singleton.jugadores_ordenados: #recorre el vector de jugadores, y le da el turno a cada uno
            gano = juegue(jugador, boton_dados, dado, tablero)  #manda al jugador por el cual va iterando a que realice su jugada
            tablero.dibujarCasillas()

            espere_boton_espacio()

            if gano == True:#comprueba si ese jugador gano y cierra el programa, dando el nombre del ganador
                jugadorGanador = jugador.getNombre()
                break
    

    Singleton.setJugadorGanador(jugadorGanador)
    muestre_mensaje_ganador()
    pygame.quit()
    sys.exit(0)
    
run() 