from abc import ABC, abstractmethod
from singleton import Singleton

class Almacenador(ABC):

    def __init__(self):
        #self.nombre = nombreArchivo
        super().__init__()

    @abstractmethod
    def guardar(self):
        pass


class AlmacenadorTXT(Almacenador):

    def __init__(self, nombreArchivo):
        self.nombre = nombreArchivo
        super(AlmacenadorTXT,self).__init__()


    def guardar(self):
        self.nombre += ".txt"
        try:
            f = open(self.nombre,"w+") #si no esta creado, borra todo y escribe de cero
        except:
            print("Ocurrio un error al crear el archivo donde se va a guardar el juego")
        #escribe en el archivo
        try:
            f.write(str(len(Singleton.jugadores_ordenados)))
            f.write("\n")
            for jugador in Singleton.jugadores_ordenados:           #los va a almacenar en el orden de turnos asi seran los mismos
                f.write(jugador.nombre)
                f.write("/")
                f.write(str(jugador.pos_tablero))
                f.write("/")
                f.write(str(jugador.colorString))
                f.write("/")
                f.write(str(jugador.movX))
                f.write("/")
                f.write(str(jugador.movY))
                f.write("\n")
            f.write(str(len(Singleton.serpientes)))
            f.write("\n")
            for serpiente in Singleton.serpientes:
                f.write(str(serpiente.getCasillaInicio().getIndice()))
                f.write("/")
                f.write(str(serpiente.getCasillaFinal().getIndice()))
                f.write("\n")
            f.write(str(len(Singleton.escaleras)))
            f.write("\n")
            for escalera in Singleton.escaleras:
                f.write(str(escalera.getCasillaInicio().getIndice()))
                f.write("/")
                f.write(str(escalera.getCasillaFinal().getIndice()))
                f.write("\n")
        except:
            print("Ocurrio un error escribiendo dentro del archivo de guardado")

        try:
            f.close()
        except:
            print("Ocurrio un error cerrando el archivo de guardado")
        