
class Singleton():

    #Atributos
    jugadores = []
    jugadores_ordenados = []            #ordenados por turno
    ancho_tablero = 0
    alto_tablero = 0
    cantidad_jugadores = 0
    cantidad_x = 0
    cantidad_y = 0
    #TODO variable de colores aqui para que los demas lo utilicen
    
    #Metodos
    @classmethod
    def init(cls, an, al, cantX, cantY):
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
