import sys, pygame
import os
import time
from pygame.locals import *
#from button import Button
from sidebar import Sidebar
from conector import Conector, Escalera, Serpiente
from casilla import Casilla, CasillaEstandar, CasillaEscalera, CasillaSerpiente
from dado import Dado
from jugador import Jugador, VistaJugador
from tablero import Tablero
from singleton import Singleton
from arbitro import Arbitro
from vista import Vista
from tkinter import *
from cargador import CargadorTXT

ANCHO_BARRA = 250
ANCHO = 700 + ANCHO_BARRA
ALTO = 700
CANTIDAD_X = 10
CANTIDAD_Y = 10
POS_GANADORA = (CANTIDAD_X * CANTIDAD_Y)-1

class Controlador:

    def __init__(self):
        self.eventos = [1, 2, 3, 4]
        self.ventana = self.genere_ventana_pygame()
        self.vista = Vista(self.ventana)
        self.listeners = []
        self.jugadores = []
        self.registerListener(self.vista)


    def genere_ventana_pygame(self):
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

    def crear_relacion_jugador(self, jugador):
        self.jugadores.append( (jugador, VistaJugador(jugador)) )

    def encontrar_relacion(self, jugador):
        jugadorVista = None
        for player in self.jugadores:
            if player[0] == jugador:
                jugadorVista = player[1]
                break
        return jugadorVista


    def registerListener(self, listener):
        self.listeners.append(listener)
        
    def postEvent(self, event, type):
        for listener in self.listeners:
            if isinstance(listener, type):
                listener.notify(event)

    def dibujar_jugadores(self):
        """
        Metodo del controlador que llama a cada jugador presente en el tablero a dibujarse en la ventana
        de pygame para que pueda seguir siendo visible en el juego.
        """
        for jugador in self.jugadores: jugador[1].dibujar()


    def maneje_eventos(self):
        continuar = True 
        while continuar:
            for events in pygame.event.get():     
                if events.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif events.type == pygame.MOUSEBUTTONDOWN:
                    self.postEvent(events.type, Vista)
                    if Arbitro.recibioDados:
                        continuar = False
                        break
                elif events.type == pygame.MOUSEMOTION:
                    self.postEvent(events.type, Vista)
                pygame.display.update()
    
    def espere_boton_espacio(self):
        """
        Este metodo se encarga tener el programa "en espera" hasta que el usuario
        presione la tecla de espacio. Esto para proseguir con el turno.
        """
        condicion = True
        while condicion:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.dibujar_jugadores()
                    condicion = False

    def muestre_presionar_espacio(self):
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

    def muestre_mensaje_ganador(self):
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

    def juegue(self, jugador, jugadorVista):
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
        jugadorVista.muestre_turno_jugador()
        Arbitro.jugador_juegue(jugador)
        self.muestre_presionar_espacio()
        print("EL jugador saco en los dados un ", Arbitro.valor_actual_dados)
        coordenadas = Arbitro.obtener_destino(jugador.pos_tablero, Arbitro.valor_actual_dados)
        jugador.mover(Arbitro.valor_actual_dados, coordenadas)
    



def run():
    root = Tk() 
    root.title("Serpientes y escaleras")
    root.geometry("450x360")         
    #nuevaPartida.grid()
    #cargarPartida.grid()
    global controlador
    def nuevoJuego():
        controlador = Controlador()
        Arbitro.init(controlador)
        print("VOY A CARGAR JUEGO")
        root.destroy()
        while True:
            try:
                cantidad_jugadores = int(input("Ingrese la cantidad de jugadores: "))
            except:
                print("Tiene que ser un numero")
            if cantidad_jugadores > 1 and cantidad_jugadores < 5:
                break
        #Inicializar jugadores
        for i in range(cantidad_jugadores):
            jugador = Jugador(0, Singleton.getPosJugadores(i)[0], Singleton.getPosJugadores(i)[1],
                            (Singleton.getAlto()//Singleton.getCantX())//4, (Singleton.getAlto()/Singleton.getCantY())//4,
                            Singleton.getPosJugadores(i)[0] - Singleton.casillasTablero[0].getCoordenadas()[0],
                            Singleton.getPosJugadores(i)[1] - Singleton.casillasTablero[0].getCoordenadas()[1])
            Arbitro.reporte_jugadores(jugador)
            controlador.crear_relacion_jugador(jugador)
        controlador.dibujar_jugadores()
            
        #Arbitro decide turnos
        Arbitro.decidir_turnos(cantidad_jugadores)
        print("Orden de jugadores: ", end="\n")
        for i in Singleton.jugadores_ordenados:
            print(i.nombre)

        while not Arbitro.jugador_gano:                                             # mientras no haya un ganador, siguen los turnos
            for jugador in Singleton.jugadores_ordenados:                           #recorre el vector de jugadores, y le da el turno a cada uno
                jugadorVista = controlador.encontrar_relacion(jugador)
                controlador.juegue(jugador, jugadorVista)                                #manda al jugador por el cual va iterando a que realice su jugada
                controlador.vista.tablero.dibujarCasillas()

                controlador.espere_boton_espacio()

                if Arbitro.jugador_gano:                    #comprueba si ese jugador gano y cierra el programa, dando el nombre del ganador
                    jugadorGanador = jugador.getNombre()
                    break
        
        Singleton.setJugadorGanador(jugadorGanador)
        controlador.muestre_mensaje_ganador()
        pygame.quit()
        sys.exit(0) 
    def cargarJuego():
        print("VOY A CARGAR JUEGO")
        cargador = CargadorTXT()
        root.destroy()
        controlador = Controlador()
        Arbitro.init(controlador)
        #CREAR EL TABLERO CON LAS SERPIENTES Y ESCALERAS LEIDAS
        #ASEGURARSE DE QUE VUELVA A FUNCIONAR TODO
        
        cargador.cargar()   
    nuevaPartida = Button(root,text = "Empezar partida",command = nuevoJuego).place(x=170, y=100) 
    cargarPartida = Button(root,text = "Cargar Partida",command = cargarJuego).place(x=170, y=200)
    root.mainloop()
    
   

run()