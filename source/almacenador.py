from abc import ABC, abstractmethod
from singleton import Singleton

class Almacenador(ABC):
    """
    Esta clase corresponde a un almacenador, cuya funcionalidad es guardar en un archivo los avances del juego de manera
    que el usuario pueda continuar la partida en otro momento. Esta clase respeta el patron de disenyo Constructor. 
    """
    def __init__(self):
        #self.nombre = nombreArchivo
        super().__init__()

    @abstractmethod
    def guardar(self):
        """
        Metodo abstracto del guardado de archivos. Cada clase que haga herencia, guardara en un archivo de formato distinto.
        En nuestro caso, solo lo haremos con una clase que guarde en .txt.
        """
        pass


class AlmacenadorTXT(Almacenador):
    """
    Esta clase hereda de Almacenador, y demuestra el correcto funcionamiento del patron Constructor. Esta clase es especifica
    para crear archivos de formato .txt donde se almacenara la informacion vital del juego, para que sea posible jugarlo luego.
    """
    def __init__(self, nombreArchivo):
        """
        Inicializa el almacenador de archivos de texto.
        :param nombreArchivo: Nombre del archivo que se va a crear o donde se va a sobreescribir  informacion.
        """
        self.nombre = nombreArchivo
        super(AlmacenadorTXT,self).__init__()


    def guardar(self):
        """
        Metodo que va guaardar en un archivo de texto toda la informacion vital para guardar la partida. Esta informacion es: la
        cantidad de jugadores; el nombre, posicion en el tablero, color, ubicacion en casilla en X y ubicacion en casilla en Y de 
        cada jugador; cantidad de serpientes; posicion en el tablero de inicio de sepriente y la posicion de final de la misma; 
        cantidad de escaleras; posicion en el tablero de inicio de escalera y la posicion de final de la misma.
        """
        self.nombre += ".txt"
        try:
            f = open(self.nombre,"w+")              #si no esta creado, borra todo y escribe de cero
        except:
            print("Ocurrio un error al crear el archivo donde se va a guardar el juego")
        #escribe en el archivo
        try:
            f.write(str(len(Singleton.jugadores_ordenados)))
            f.write("\n")
            for jugador in Singleton.jugadores_ordenados:           #los va a almacenar en el orden de turnos asi seran los mismos
                f.write(jugador.nombre + "/" + str(jugador.pos_tablero) + "/" + str(jugador.colorString) + "/" + str(jugador.movX) + "/" + str(jugador.movY))
                #print("ACA TENGO UN "+str(jugador.colorString))
                f.write("\n")
            f.write(str(len(Singleton.serpientes)) + "\n")
            for serpiente in Singleton.serpientes:
                f.write(str(serpiente.getCasillaInicio().getIndice()) + "/" + str(serpiente.getCasillaFinal().getIndice()))
                f.write("\n")
            f.write(str(len(Singleton.escaleras)) + "\n")
            for escalera in Singleton.escaleras:
                f.write(str(escalera.getCasillaInicio().getIndice()) + "/" + str(escalera.getCasillaFinal().getIndice()))
                f.write("\n")
        except:
            print("Ocurrio un error escribiendo dentro del archivo de guardado")

        try:
            f.close()
        except:
            print("Ocurrio un error cerrando el archivo de guardado")
        