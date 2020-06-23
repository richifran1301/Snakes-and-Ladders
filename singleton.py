
class Singleton():
    """
    Esta clase corresponde al cumplimiento del patron de disenyo 
    llamado Singletone. Es una clase con metodos de clase, que contiene
    informacion de interes para todas las demas clases del programa.
    """

    #Atributos
    jugadores = []
    jugadores_ordenados = []            #ordenados por turno
    ancho_tablero = 0
    alto_tablero = 0
    cantidad_jugadores = 0
    cantidad_serpientes = 0
    cantidad_escaleras = 0
    cantidad_x = 0
    cantidad_y = 0
    pos_ganadora = 0
    ventana = None
    posicion_jugadores = []
    jugadorGanador = None
    casillasTablero = []
    colores_casillas = {"rojo": (244,124,124), "amarillo": (247,244,139), "verde": (161,222,147), "azul": (112,161,215), "blanco": (255,255,255), "negro":(0,0,0)}
    colores_jugadores = {"magenta": (255,0,230), "azul": (0, 0, 128), "gris": (127,127,127), "naranja": (255,100,10), "negro": (0,0,0),
                        "verde": (118,238,0), "aqua": (0,255,255), "dorado": (255,185,15), "rojo": (205,51,51) }
    colores_jugadores_usados = []
    serpientes = []
    escaleras = []

    #Metodos
    @classmethod
    def init(cls, an, al, cantX, cantY, casillaGanadora, casillasT, vent):
        """
        :param an: ancho del tablero
        :type an: int 
        :param al: largo del tablero.
        :type al: int
        :param cantX: cantidad de casillas horizontalmente (en coordenadas X)
        :type cantX: int
        :param cantX: cantidad de casillas verticalmente (en coordenadas Y)
        :type cantY: int
        :param casillaGanadora: posicion de casilla ganadora
        :type casillaGanadora: int
        :param casillasT: casillas del tablero 
        :type: vector de objetos Casilla 
        :param vent: Referencia a la ventana de pygame.
        :type vent: pygame.display
        """
        cls.casillasTablero = casillasT                     #copia las casillas del tablero 
        cls.pos_ganadora = casillaGanadora                  #guarda las coordenadas de la casilla 100 en tablero 10x10 por ejemplo (ganadora)
        cls.jugadores = []
        cls.ancho_tablero = an
        cls.alto_tablero = al
        cls.cantidad_jugadores = 0
        cls.cantidad_x = cantX
        cls.cantidad_y = cantY
        cls.ventana = vent
        cls.establecer_pos_jugadores()


    @classmethod
    def establecer_pos_jugadores(cls):
        """
        Este metodo establece las posiciones en las que se van a ubicar los jugadores. Esta pensado
        para un minimo de 2 jugadores y un maximo que corresponde a 4. Los ubica en la casilla inicial pero
        de manera que se visualicen, anque hayan varios en la misma casilla. 
        """
        cls.posicion_jugadores = [
                        ((cls.casillasTablero[0].getCoordenadas()[0] + ((Singleton.getAlto()//Singleton.getCantX())//4)),
                        (cls.casillasTablero[0].getCoordenadas()[1] - ((Singleton.getAlto()//Singleton.getCantY())//2))),

                        ((cls.casillasTablero[0].getCoordenadas()[0] - ((Singleton.getAlto()//Singleton.getCantX()//2))), 
                        (cls.casillasTablero[0].getCoordenadas()[1] - ((Singleton.getAlto()//Singleton.getCantY())//2))),

                        ((cls.casillasTablero[0].getCoordenadas()[0] + ((Singleton.getAlto()//Singleton.getCantX())//4)), 
                        (cls.casillasTablero[0].getCoordenadas()[1] + ((Singleton.getAlto()//Singleton.getCantY())//4))),

                        ((cls.casillasTablero[0].getCoordenadas()[0] - ((Singleton.getAlto()//Singleton.getCantX())//2)), 
                        (cls.casillasTablero[0].getCoordenadas()[1] + ((Singleton.getAlto()//Singleton.getCantY())//4)))
        ]
    
    @classmethod
    def getPosJugadores(cls, indice):
        """
        Este metodo devuelve la posicion en el tablero, en coordenadas, de un jugador en especificion.
        :param indice: numero identificador del jugador
        :type indice: int
        :returns: coordenadas de X y Y del jugador respectivo segun el indice
        """
        return cls.posicion_jugadores[indice]


    @classmethod
    def getAlto(cls):
        """
        Este metodo devuelve la medida del alto del tablero.
        :returns: la medida del alto del tablero
        """
        return cls.alto_tablero

    @classmethod
    def getAncho(cls):
        """
        Este metodo devuelve la medida del ancho del tablero.
        :returns: la medida del ancho del tablero
        """
        return cls.ancho_tablero
    
    @classmethod
    def getCantX(cls):
        """
        Este metodo devuelve la cantidad de casillas horizontales
        :returns: la cantidad de casillas en X (horizontalmente)
        """
        return cls.cantidad_x

    @classmethod
    def getCantY(cls):
        """
        Este metodo devuelve la cantidad de casillas verticales
        :returns: la cantidad de casillas en X (verticalmente)
        """
        return cls.cantidad_y

    @classmethod
    def agregar_jugador(cls, jugador):
        """
        Este metodo reporta la existencia de un jugador en el juego, agregandolo a la lista de jugadores. 
        Ademas, le otorga un nombre automaticamente segun sea el orden en el que fue creado.
        :param jugador: jugador a agregar.
        :type jugador: Jugador
        """
        cls.cantidad_jugadores += 1
        jugador.setNombre("Jugador " + str(cls.cantidad_jugadores))
        cls.jugadores.append(jugador)
    
    @classmethod
    def ver_jugadores(cls):
        """
        Este metodo imprime en consola la cantidad de jugadores actuales
        :returns: la cantidad de casillas en X (horizontalmente)
        """
        hilera = "Jugadores: "
        for jugador in cls.jugadores:
            hilera += jugador.getNombre() + ", " 
        print(hilera)
    
    @classmethod
    def setJugadorGanador(cls, jugador):
        """
        Metodo que va a informarle al Singleton quien es el jugador ganador. Va a almacenarlo en la variable
        jugadorGanador.
        :param jugador: Jugador ganador a almacenar en Singleton
        :type jugador: Jugador
        """
        cls.jugadorGanador = jugador

    @classmethod
    def getJugadorGanador(cls):
        """
        Metodo que devuelve al jugador ganador de la partida.
        """
        return cls.jugadorGanador