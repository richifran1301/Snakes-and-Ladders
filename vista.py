import os, pygame
from tablero import Tablero
from singleton import Singleton
from sidebar import Sidebar
from dado import Dado
from button import Button

ANCHO_BARRA = 250
ANCHO = 700 + ANCHO_BARRA
ALTO = 700
CANTIDAD_X = 10
CANTIDAD_Y = 10

class Vista():

    def __init__(self, ventana):
        self.ventana = ventana
        self.tablero = self.crear_tablero()
        Singleton.init(ANCHO, ALTO, CANTIDAD_X, CANTIDAD_Y, (CANTIDAD_X * CANTIDAD_Y)-1, self.tablero.casillas, ventana)
        self.boton_dados, self.dado = self.crear_sidebar()

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
        boton_dados = Button(self.ventana, Singleton.colores_casillas["blanco"], 750, 35, 150, 40, "Lanzar dados")
        dado = Dado()
        elementos_sidebar = [boton_dados, dado]
        Sidebar(700, 700, 250, Singleton.colores_casillas["blanco"], elementos_sidebar)
        
        return boton_dados, dado

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

    def notify(self, evento):
        self.eventoActual = evento
        print("La vista recibió el evento: ", self.eventoActual)
        posicion_cursor = pygame.mouse.get_pos()

        if self.eventoActual == 5:
            if self.boton_dados.isOver(posicion_cursor):
                temp = self.dado.lanzar()
        elif self.eventoActual == 4:
            if self.boton_dados.isOver(posicion_cursor):
                self.boton_dados.mi_color = (161,222,147) 
            else:
                self.boton_dados.mi_color = (54,57,63)

            self.boton_dados.dibujar()
        
        pygame.display.update()
        
        

    