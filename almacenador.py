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
        print("NOMBRE: ",self.nombre)
        self.nombre += ".txt"
        print("NOMBRE: ",self.nombre)
        f = open(self.nombre,"w+") #si no esta creado, borra todo y escribe de cero
        #escribe en el archivo
        f.write(str(len(Singleton.jugadores)))
        f.write("\n")
        for jugador in Singleton.jugadores:
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
        f.close()
        