
class Singleton():

    #Atributos
    jugadores = []
    jugadores_ordenados = []            #ordenados por turno
    ancho_tablero = 0
    alto_tablero = 0
    cantidad_jugadores = 0
    cantidad_x = 0
    cantidad_y = 0
    pos_ganadora = 0
    casillasTablero = []
    colores_casillas = {"rojo": (244,124,124), "amarillo": (247,244,139), "verde": (161,222,147), "azul": (112,161,215), "blanco": (255,255,255)}
    colores_jugadores = {"magenta": (255,0,230), "azul": (0, 0, 128), "gris": (127,127,127), "naranja": (255,100,10), "negro": (0,0,0)}
    colores_jugadores_usados = []

    #Metodos
    @classmethod
    def init(cls, an, al, cantX, cantY, casillaGanadora, casillasT):
        cls.casillasTablero = casillasT #copia las casillas del tablero 
        cls.pos_ganadora = casillaGanadora #guarda las coordenadas de la casilla 100 (ganadora)
        cls.jugadores = []
        cls.ancho_tablero = an
        cls.alto_tablero = al
        cls.cantidad_jugadores = 0
        cls.cantidad_x = cantX
        cls.cantidad_y = cantY

    @classmethod
    def getAlto(cls):
        return cls.alto_tablero

    @classmethod
    def getAncho(cls):
        return cls.ancho_tablero
    
    @classmethod
    def getCantX(cls):
        return cls.cantidad_x

    @classmethod
    def getCantY(cls):
        return cls.cantidad_y

    @classmethod
    def agregar_jugador(cls, jugador):
        cls.cantidad_jugadores += 1
        jugador.setNombre("Jugador " + str(cls.cantidad_jugadores))
        cls.jugadores.append(jugador)
    
    @classmethod
    def ver_jugadores(cls):
        hilera = "Jugadores: "
        for jugador in cls.jugadores:
            hilera += jugador.getNombre() + ", " 
        print(hilera)
    
    @classmethod
    def dibujar_jugadores(cls):
        for jugador in cls.jugadores:
            jugador.dibujar()
