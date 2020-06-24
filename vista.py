from tkinter import *
#from tkinter import ttk
#from tkinter import messagebox
#from tkinter.ttk import *
import os, pygame
from tablero import Tablero
from singleton import Singleton
from sidebar import Sidebar
from dado import Dado
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

    def __init__(self, ventana, es_partida_cargada):
        self.ventana = ventana
        self.tablero = self.crear_tablero()
        Singleton.init(ANCHO, ALTO, CANTIDAD_X, CANTIDAD_Y, (CANTIDAD_X * CANTIDAD_Y)-1, self.tablero.casillas, es_partida_cargada, self.ventana)
        self.boton_dados, self.dado, self.boton_reglas, self.boton_guardar = self.crear_sidebar()
        

    def crear_tablero(self):
        """
        Llama el constructor de Tablero y sus metodos para generar tanto las casillas, como
        las serpientes y escaleras respectivas en estas casillas.
        :param _ventana: Ventana grafica del juego
        :type _ventana: pygame window object
        :returns: Tablero object -- Devuelve el objeto de tablero recien creado para luego
        utilizar sus metodos en otras funciones.
        """
        tablero = Tablero((CANTIDAD_X, CANTIDAD_Y), self.ventana, ANCHO_BARRA)

        return tablero

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
        dado = Dado()
        elementos_sidebar = [boton_dados, dado]
        Sidebar(700, 700, 250, Singleton.colores_casillas["blanco"], elementos_sidebar)
        return boton_dados, dado, boton_reglas,boton_guardar

    def dibujar_dados(self, resultados_por_dado):
        """
        Esta función dibuja dos dados según el resultado de sus caras.
        :returns:  None -- Procedimiento sin valor de retorno.
        """

        # dirección de las imágenes de los dados
        ruta_local = 'imagenes/'

        # haga el proceso de dibujo de la primera cara del dado, de pygame para imágenes
        ruta_imagen = os.path.join(ruta_local, str(resultados_por_dado[0]) + ".png")
        cara_temp = pygame.image.load(ruta_imagen)
        imagen_transformada = pygame.transform.scale(cara_temp, (60,60))
        cara_izq = imagen_transformada.convert()  # or .convert_alpha()
        rect_izq = cara_izq.get_rect()
        rect_izq.center = (780, 145)
        Singleton.ventana.blit(cara_izq, rect_izq)

        # lo mismo para la segunda cara
        ruta_imagen = os.path.join(ruta_local, str(resultados_por_dado[1]) + ".png")
        cara_temp = pygame.image.load(ruta_imagen)
        imagen_transformada = pygame.transform.scale(cara_temp, (60,60))
        cara_der = imagen_transformada.convert()  # or .convert_alpha()
        rect_der = cara_der.get_rect()
        rect_der.center = (870, 145)
        Singleton.ventana.blit(cara_der, rect_der)

        
    def guardarPartida(self):
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
        #print("NOMBRE PARTIDA: ",nombre)
        
        
        
        
    def notify(self, evento):
        self.eventoActual = evento
        #print("La vista recibió el evento: ", self.eventoActual)
        posicion_cursor = pygame.mouse.get_pos()
        if self.eventoActual == CLICK:      
            if self.boton_dados.isOver(posicion_cursor):
                resultado_dados = self.dado.lanzar()
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
                
                texto = "\n\nNúmero de jugadores: dos o más, pero nunca deben jugar más de seis jugadores a la vez. \n Se necesita: un tablero del juego, una ficha de diferente color para cada jugador y un dado. \n\n REGLAS \n\n 1- Para comenzar, todos los jugadores tenéis que tirar una vez el dado. El que saque más puntos será \n el primero en empezar la partida; continuará el que esté a su izquierda y así sucesivamente. \n\n 2- El juego consiste en mover la ficha desde la casilla 1 hasta la 64; debes avanzarla tantos puestos \n como puntos te salgan al tirar el dado. \n\n 3- Pero ¡cuidado!, si caes en la cabeza de una serpiente debes bajar hasta su cola. LAS SERPIENTES \n SOLO BAJAN, NUNCA SUBEN. \n\n 4- También puedes tener suerte. Si caes en una casilla que señale el principio de una escalera sube \n hasta el final de la escalera. LAS ESCALERAS SOLO SUBEN, NUNCA BAJAN. \n\n 5- Gana el primero que llegue a la última casilla. \n\n 6- Si queréis jugar otra partida, el ganador de la primera debe ser ahora el último en empezar a jugar. \n Así tendrá menos posibilidades de volver a ganar. \n\n"
                
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

    