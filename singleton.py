
class Singleton():
    def __init__(self,ancho,alto):
        self.jugadores = []
        self.ancho_tablero = ancho
        self.alto_tablero = alto
        self.cantidad_jugadores = 0

    def get_alto_tablero(self):
        return self.alto_tablero

    def get_ancho_tablero(self):
        return self.ancho_tablero

    def agregar_jugador(self, jugador):
        self.cantidad_jugadores += 1
        jugador.setNombre("Jugador " + str(self.cantidad_jugadores))
        self.jugadores.append(jugador)
    
    def ver_jugadores(self):
        hilera = "Jugadores: "
        for jugador in self.jugadores:
            hilera += jugador.getNombre() + ", " 
        print(hilera)