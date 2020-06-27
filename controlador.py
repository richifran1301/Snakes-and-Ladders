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

    def __init__(self, es_partida_cargada):
        self.tablero = None
        self.dado = Dado()
        self.eventos = [1, 2, 3, 4]
        self.es_partida_cargada = es_partida_cargada
        self.ventana = self.genere_ventana_pygame()
        self.vista = Vista(self, self.ventana, self.es_partida_cargada)
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

    def crear_relacion_jugadores(self):
        '''
        Llena la lista de tuplas de jugadores para hacer la relacion
        jugador logico - jugador grafico.
        '''
        for jugador in Singleton.jugadores:
            self.jugadores.append( (jugador, VistaJugador(jugador)) )

    def encontrar_relacion(self, jugador):
        '''
        Busca la relacion entre jugador logico y jugador grafico en la lista de tuplas
        :param jugador: jugador logico a buscar
        :type jugador: Jugador object
        '''
        jugadorVista = None
        for player in self.jugadores:
            if player[0] == jugador:
                jugadorVista = player[1]
                break
        return jugadorVista

    def registerListener(self, listener):
        '''
        Agrega un objeto encargado de realizar una accion a la lista de listeners
        :param listener: objeto a guardar
        :type listener: Template object
        '''
        self.listeners.append(listener)
        
    def postEvent(self, event, type):
        '''
        Llama a la funcion de vista para saber cual accion es la que debe de suceder en la interfaz grafica
        :param event: evento que acaba de suceder
        :type event: Pygame event
        :param type: tipo de objeto que se va a encargar de realizar alguna funcion respectiva
        :type type: Template Object
        '''
        for listener in self.listeners:
            if isinstance(listener, type):
                listener.notify(event)

    def dibujar_jugadores(self):
        """
        Metodo del controlador que llama a cada jugador presente en el tablero a dibujarse en la ventana
        de pygame para que pueda seguir siendo visible en el juego.
        """
        for jugador in self.jugadores: jugador[1].dibujar()

    def lanzar_dado(self):
        '''
        LLama a la funcion de dado de lanzar los dados y devuelve el resultado
        :return: el resultado de los dados en forma de entero
        '''
        return self.dado.lanzar()

    def crear_tablero_logico(self, tamanio, ventana, ancho_barra, es_partida_cargada):
        '''
        Crea un objeto de tablero logico y o guarda en una variable local de "tablero"
        '''
        self.tablero = Tablero(tamanio, ventana, ancho_barra, es_partida_cargada)

    def colorear_casillas_tablero(self):
        '''
        Colorea las casillas del tablero con su color predeterminado.
        :return: Devuelve las casillas del tablero en forma de lista
        '''
        self.tablero.colorearCasillas()
        return self.tablero.casillas

    def actualizar_tablero(self):
        '''
        Recolorea y redibuja las casillas del tablero
        :return: las casillas del tablero en forma de lista
        '''
        self.tablero.casillas = []
        #self.tablero.serpientes = []
        #self.tablero.escaleras = []
        self.tablero.generarCasillas()          # se llama a la función que genera casillas
        self.tablero.colorearCasillas()

        return self.tablero.casillas

    def maneje_eventos(self):
        '''
        Se encarga de manejar los eventos de cuando los botones se ponen de otro color
        o si se se la click al boton de dado.
        '''
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
        coordenadas = Arbitro.obtener_destino(jugador.pos_tablero, Arbitro.valor_actual_dados)
        self.vista.dibuje_cuadro_blanco()
        jugador.mover(Arbitro.valor_actual_dados, coordenadas)
    
    def obtener_colores_jugadores(self, nombre, error, contador):
        '''
        Le pide al usuario el color de ficha que quiere usar en el juego
        y guarda esa informacion para luego ser consumida por el jugador.
        :param nombre: nombre del jugador a pedirle el color a usar
        :type nombre: string
        :param error: mensaje que se va a desplegar si el usuario pide un color invalido
        :type error: string
        :param contador: cantidad de jugadores a hacer la solicitud
        :type contador: int
        '''
        root = Tk() 
        root.title("Crear jugadores")
        root.geometry("450x360")     
        mensaje = Label(root, text = "Color de "+nombre+": ")
        mensaje.grid(row = 1, column = 1)
        if contador > 0:
            mensaje_error = Label(root, text = error)
            mensaje_error.grid(row = 8, column = 1)
        color = StringVar()
        entrada_color = Entry(root, textvariable = color)
        entrada_color.grid(row = 1, column = 2)         
        color.get()        
        ok = Button(root,text = "Continuar",command = root.destroy)
        ok.grid(row = 2, column = 2)
        def mostrar():
            numcur = color.get()
            try:
                Arbitro.color_tmp = str(numcur)
            except:
                pass
            root.destroy()
        ok.config(command=mostrar)
        root.mainloop()

    def obtener_cantidad_jugadores(self, contador):
        '''
        Se pide al usuario la cantidad de jugadores que van a jugar y guarda la 
        informacion para ser consumida por el arbitro.
        :param contador: cantidad de jugadores ingresada
        :type contador: int
        '''
        root = Tk() 
        root.title("Crear partida")
        root.geometry("450x360")     
        mensaje = Label(root, text = "Cantidad de jugadores:")
        mensaje.grid(row = 1, column = 1)
        if contador > 0:
            mensaje_error = Label(root, text = "Cantidad invalida")
            mensaje_error.grid(row = 8, column = 1)             
        cant_jugadores = StringVar()
        entrada_cant = Entry(root, textvariable = cant_jugadores)
        entrada_cant.grid(row = 1, column = 2)         
        cant_jugadores.get()        
        ok = Button(root,text = "Continuar",command = root.destroy)
        ok.grid(row = 2, column = 2)
        def mostrar():
            numcur = cant_jugadores.get()
            try:
                Arbitro.cantidad_jugadores_tmp = int(numcur)
            except:
                pass
            root.destroy()
        ok.config(command=mostrar)
        root.mainloop()


def empezarCondicionesJuego(controlador):
    '''
    Llena las condiciones iniciales que ocupa el juego
    :param controlador: objeto de controlador para utilizar sus funciones
    :type controlador: Controlador object
    '''
    contador = 0
    while True:
        controlador.obtener_cantidad_jugadores(contador)
        contador +=1
        if Arbitro.cantidad_jugadores_tmp > 1 and Arbitro.cantidad_jugadores_tmp < 5:
            break
        
    #Inicializar jugadores
    for i in range(Arbitro.cantidad_jugadores_tmp):
        jugador = Jugador(0, Singleton.getPosJugadores(i)[0], Singleton.getPosJugadores(i)[1],
                        (Singleton.getAlto()//Singleton.getCantX())//4, (Singleton.getAlto()/Singleton.getCantY())//4,
                        Singleton.getPosJugadores(i)[0] - Singleton.casillasTablero[0].getCoordenadas()[0],
                        Singleton.getPosJugadores(i)[1] - Singleton.casillasTablero[0].getCoordenadas()[1])
        Arbitro.reporte_jugadores(jugador)
    controlador.crear_relacion_jugadores()
    controlador.dibujar_jugadores()
        
    #Arbitro decide turnos
    Arbitro.decidir_turnos(Arbitro.cantidad_jugadores_tmp)
    print("Orden de jugadores: ", end="\n")
    for i in Singleton.jugadores_ordenados:
        print(i.nombre)


def juego(controlador):
    '''
    Este metodo tiene el ciclo principal del juego, que no termina hasta que alguien gane.
    Va a llamar todas las funciones que ocupa el juego para funcionar.
    :param controlador: objeto de controlador para utilizar sus funciones
    :type controlador: Controlador object
    '''
    while not Arbitro.jugador_gano:                                             # mientras no haya un ganador, siguen los turnos
        for jugador in Singleton.jugadores_ordenados:                          #recorre el vector de jugadores, y le da el turno a cada uno
            jugadorVista = controlador.encontrar_relacion(jugador)
            controlador.juegue(jugador, jugadorVista)                                #manda al jugador por el cual va iterando a que realice su jugada
            controlador.vista.tablero_grafico.dibujarCasillas()
            controlador.espere_boton_espacio()

            if Arbitro.jugador_gano:                    #comprueba si ese jugador gano y cierra el programa, dando el nombre del ganador
                jugadorGanador = jugador.getNombre()
                break
        
    Singleton.setJugadorGanador(jugadorGanador)
    controlador.muestre_mensaje_ganador()
    pygame.quit()
    sys.exit(0) 


def run():
    '''
    Metodo que verifica si es una partida cargada o una partida nueva. Tambien despliega el
    menu principal. Llama al ciclo principal del juego (metodo juego)
    '''
    root = Tk() 
    root.title("Serpientes y escaleras")
    #root.geometry("450x360")        
    root.geometry("512x512")        
    bg_image = PhotoImage(file ="imagenes/menu.png")
    x = Label (image = bg_image)
    x.grid(row = 0, column = 0)

    def nuevoJuego():
        controlador = Controlador(False)        #False = NO es partida cargada
        Arbitro.init(controlador)
        root.destroy()
        empezarCondicionesJuego(controlador)
        juego(controlador)

    def cargarJuego():
        cargador = CargadorTXT()
        root.destroy()
        controlador = Controlador(True)             # True = SI es partida cargada
        Arbitro.init(controlador)
        cargador.cargar()
        controlador.colorear_casillas_tablero()
        controlador.vista.tablero_grafico.actualizar()
        controlador.crear_relacion_jugadores()
        controlador.dibujar_jugadores()
        juego(controlador)

    Button(root,text = "Empezar partida",command = nuevoJuego).place(x=170, y=100)  #Nueva Partida
    Button(root,text = "Cargar partida",command = cargarJuego).place(x=170, y=200)   #Cargar Partida
    root.mainloop()


run()