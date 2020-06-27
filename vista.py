from tkinter import *
#from tkinter import ttk
#from tkinter import messagebox
#from tkinter.ttk import *
import os, pygame
from tablero import VistaTablero
from singleton import Singleton
from sidebar import Sidebar
from dado import VistaDado
from button import Boton
from arbitro import Arbitro
from almacenador import AlmacenadorTXT

ANCHO_BARRA = 250
ANCHO = 700 + ANCHO_BARRA
ALTO = 700
CANTIDAD_X = 10
CANTIDAD_Y = 10

CLICK = 5
MOVER_CURSOR = 4

class Vista():

    def __init__(self, controlador, ventana, es_partida_cargada):
        '''
        Crea un nuevo objeto de vista.
        :param controlador: objeto de la clase de controlador 
        :type controlador: Controlador class object
        :param ventana: ventana grafica 
        :type ventana: Pygame object
        :param es_partida_cargada: bandera de que si es una partida cargada o una nueva
        :type es_partida_cargada: boolean
        '''
        self.controlador = controlador
        self.ventana = ventana
        self.es_partida_cargada = es_partida_cargada
        self.tablero_grafico = self.crear_tablero_grafico()
        Singleton.init(ANCHO, ALTO, CANTIDAD_X, CANTIDAD_Y, (CANTIDAD_X * CANTIDAD_Y)-1, self.es_partida_cargada, self.ventana)
        self.boton_dados, self.dado_grafico, self.boton_reglas, self.boton_guardar = self.crear_sidebar()
        #print("Se creo la vista")
        

    def crear_tablero_grafico(self):
        """
        Llama el constructor de Tablero y sus metodos para generar tanto las casillas, como
        las serpientes y escaleras respectivas en estas casillas.
        :returns: Tablero Vista object -- Devuelve el objeto de tablero recien creado para luego
        utilizar sus metodos en otras funciones.
        """
        tablero_grafico = VistaTablero(self.controlador, (CANTIDAD_X, CANTIDAD_Y), self.ventana, ANCHO_BARRA, self.es_partida_cargada)
        return tablero_grafico

    def actualizar_tablero_grafico(self):
        '''
        Actualiza y vuelve a dibujar las casillas porque cada vez que se mueve
        un jugador se modifica el formato grafico de la casilla que acaba de moverse.
        '''
        self.tablero_grafico.actualizar()

    def crear_sidebar(self):
        """
        Llama el constructor de Dado y sus metodos para agregar el icono de los 
        dados en pantalla y poder obtener el resultado aleatorio que ellos generen.
        :param _ventana: Ventana grafica del juego
        :type _ventana: pygame window object
        :returns: tuple -- Devuelve como tupla el objeto de Button, que va a ser el boton 
        grafico de los dados, de primero y de segundo, el objeto de Dado para poder utilizar sus funciones.
        """
        boton_dados = Boton(self.ventana, Singleton.colores_casillas["blanco"], 750, 35, 150, 40, "Lanzar dados")
        boton_guardar = Boton(self.ventana, Singleton.colores_casillas["negro"], 750, 550, 150, 40, "Guardar partida")
        boton_reglas = Boton(self.ventana, Singleton.colores_casillas["negro"], 750, 600, 150 ,40, "Mostrar reglas")
        dado_grafico = VistaDado(self.controlador)
        elementos_sidebar = [boton_dados, dado_grafico]
        Sidebar(700, 700, 250, Singleton.colores_casillas["blanco"], elementos_sidebar)
        return boton_dados, dado_grafico, boton_reglas,boton_guardar
        
    def guardarPartida(self):
        '''
        Crea el boton de guardado en la ventana del juego y cuando se 
        presiona, llama al constructor del almacenador para pasarle el
        nombre de la partida a guardar.
        '''
        root = Tk() 
        root.title("GUARDAR PARTIDA")
        root.geometry("450x360")         
        NC_label = Label(root, text = "Nombre de partida nueva:")
        NC_label.grid(row = 1, column = 1)         
        NC_Int = StringVar()
        NC_entry = Entry(root, textvariable = NC_Int)
        NC_entry.grid(row = 1, column = 2)         
        NC_Int.get()         
        ok = Button(root,text = "GUARDAR",command = root.destroy)
        ok.grid(row = 2, column = 2)
        def mostrar():
            numcur = NC_Int.get()
            almacen = AlmacenadorTXT("Guardado/"+numcur)
            almacen.guardar()
            root.destroy()
        ok.config(command=mostrar)
        root.mainloop()

    def dibuje_cuadro_blanco(self):
        '''
        Dibuja un cuadro blanco para borrar cada vez que se notifica 
        en la ventana que se subio por una escalera o se bajo por una 
        serpiente.
        '''
        rect = pygame.rect.Rect((710, 350, 250, 100))
        pygame.draw.rect(Singleton.ventana, Singleton.colores_casillas["blanco"], rect)
        
    def notify(self, evento):
        '''
        Metodo principal de esta clase, se encarga de manejar un evento cada vez que se presiona 
        un boton u ocurre alguna accion grafica. Llama la funcion depende del evento ocurrido.
        :param evento: evento de pygame que acaba de ocurrir
        :type evento: pygame event
        '''
        self.eventoActual = evento
        posicion_cursor = pygame.mouse.get_pos()
        if self.eventoActual == CLICK:      
            if self.boton_dados.isOver(posicion_cursor):
                resultado_dados = self.dado_grafico.actualizar_caras()
                if Arbitro.decidiendoTurno:                                     #si el arbitro esta decidiendo turnos
                    Arbitro.reciboRespuestaDados(resultado_dados)
                elif  Arbitro.en_jugada:                                        # si el jugador se va a mover
                    Arbitro.procesaRespuestaDados(resultado_dados)
                    
            if self.boton_reglas.isOver(posicion_cursor):
                root = Tk()
                root.title("Reglas del juego")
                width = 800
                height = 450
                screen_width = root.winfo_screenwidth()
                screen_height = root.winfo_screenheight()
                x = (screen_width/2) - (width/2)
                y = (screen_height/2) - (height/2)
                root.geometry('%dx%d+%d+%d' % (width, height, x, y))
                root.resizable(False, False)
                
                texto = "\n\nNúmero de jugadores: dos o más, pero nunca deben jugar más de seis jugadores a la vez. \n Se necesita: un tablero del juego, una ficha de diferente color para cada jugador y un dado. \n\n REGLAS \n\n 1- Para comenzar, todos los jugadores tenéis que tirar una vez el dado. El que saque más puntos será \n el primero en empezar la partida; continuará el que esté a su izquierda y así sucesivamente. \n\n 2- El juego consiste en mover la ficha desde la casilla 1 hasta la 100; debes avanzarla tantos puestos \n como puntos te salgan al tirar el dado. \n\n 3- Pero ¡cuidado!, si caes en la cabeza de una serpiente debes bajar hasta su cola. LAS SERPIENTES \n SOLO BAJAN, NUNCA SUBEN. \n\n 4- También puedes tener suerte. Si caes en una casilla que señale el principio de una escalera sube \n hasta el final de la escalera. LAS ESCALERAS SOLO SUBEN, NUNCA BAJAN. \n\n 5- Gana el primero que llegue a la última casilla. \n\n"
                
                l = Label(root, text= texto)
                l.pack()
                root.after(5000, lambda: root.focus_force())
                root.mainloop()
            if self.boton_guardar.isOver(posicion_cursor):
                self.guardarPartida()
  
        elif self.eventoActual == MOVER_CURSOR:              
            if self.boton_dados.isOver(posicion_cursor) or self.boton_reglas.isOver(posicion_cursor) or self.boton_guardar.isOver(posicion_cursor) :
                if self.boton_dados.isOver(posicion_cursor):
                    self.boton_dados.mi_color = (161,222,147)
                if self.boton_reglas.isOver(posicion_cursor):
                    self.boton_reglas.mi_color = (161,222,147)
                if self.boton_guardar.isOver(posicion_cursor):
                    self.boton_guardar.mi_color = (161,222,147)
            else:
                self.boton_reglas.mi_color = (54,57,63)
                self.boton_dados.mi_color = (54,57,63)
                self.boton_guardar.mi_color = (54,57,63)
        self.boton_dados.dibujar()
        self.boton_reglas.dibujar()
        self.boton_guardar.dibujar()
        pygame.display.update() 

    