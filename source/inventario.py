from abc import ABC, abstractmethod

class ElementoInventario(ABC):
    """
    Clase abstracta de Elemento Inventario. Solo sus clases derivadas estaran
    dentro del inventario. Utilizada para el correcto uso del MARDA.
    """
    def __init__(self):
        """
        Constructor abstracto de Elemento Inventario. Tiene un unico id, que sus
        derivadas utilizaran para diferenciarse el tipo de derivada que es. En este caso
        simplemente es nulo para posteriormente sus derivadas heredar la variable y registrar
        su id.
        """
        super().__init__()
        self.id = ""        #Todo objeto derivado tendra su id


class Ficha(ElementoInventario):
    """
    Clase derivada de ElementoInventario. Corresponde a la ficha del Jugador, la cual
    se va a estar moviendo por el tablero (por las coordenadas x, y de figura). La figura
    se la otorga el jugador por parametro en el init.
    """
    def __init__(self, figura):
        """
        Constructor de Ficha. Otorga la figura de la ficha (en nuestro caso rectangulo)
        y genera su unico id que es tipo ficha.
        """
        super().__init__()
        self.figura = figura
        self.id = "ficha"           # Sera necesario para la busqueda en Inventario

    def setColor(self, color):
        """
        Metodo que establece el color de la ficha. En nuestro caso es el color del Jugador.
        """
        self.mi_color = color
        
    def mover(self, movX, movY):
        """
        Metodo que mueve la ficha por el tablero logico. No se observa en la interfaz, nada mas
        es movimiento logico.
        """
        self.figura.x = movX              
        self.figura.y = movY             



class Inventario:
    """
    Clase Inventario disenada para el correcto uso del MARDA. Es un inventario sin cantidad maxima
    especificada ya que en nuestro caso unicamente tendra la ficha del Jugador que se desplazara por
    el tablero.
    """
    def __init__(self):
        """
        Constructor de clase Inventario. Posee un vector de tuplas, que almacena objetos y la cantidad de ellos.
        """
        self.inventario = []          #Almacena objetos de la siguiente manetra: (Objeto, cantidad)

    def agregar(self, elemento_nuevo, cantidad):
        """
        Metodo que agrega un objeto de tipo ElementoInventario al vector. Si el objeto es otro tipo, se ignora y
        si ya existe un objeto de ese tipo en el Inventario se aumenta su cantidad. Para asi trabajar con mas facilidad
        aspectos como: 5 billetes de mil, 1 ficha, etc.
        """
        if not isinstance(elemento_nuevo, ElementoInventario):
            print("Error: No se agrego al inventario. Objeto de tipo desconocido.")
        else:
            es_nuevo = True
            for elemento in self.inventario:
                if elemento[0] == elemento_nuevo:
                    elemento[1] += cantidad
                    es_nuevo = False
                    break
            if es_nuevo:
                self.inventario.append((elemento_nuevo, cantidad))

    def eliminar(self, elemento_seleccionado, cantidad):
        """
        Metodo que va a eliminar una cantidad de objetos del inventario. Por paramtero viene el id del objeto
        a eliminar. En caso de no lograr eliminar el objeto,lo especifica por la terminal (debido a que solo 
        no podria en pocos casos)
        """
        if not isinstance(elemento_seleccionado, ElementoInventario):
            print("Error: No existe el objeto en el inventario.")
        else:
            for elemento in self.inventario:
                if elemento[0].id == elemento_seleccionado:
                    if elemento[1] - cantidad > 0:
                        elemento[1] -= cantidad
                    else:
                        self.inventario.remove(elemento)
                    break
            print("Elemento no encontrado en el inventario.")

    def buscar_en_inventario(self, elemento_seleccionado):
        """
        Metodo que va a buscar un objeto en el inventario y va a retornar la cantidad del objeto respectivo.
        """
        cantidad = 0
        for elemento in self.inventario:
            if elemento[0].id == elemento_seleccionado:
                cantidad = elemento[1]
                break
        return cantidad
    
    def sacar_objeto(self, elemento_seleccionado):
        """
        Metodo que obtiene el id del objeto a sacar. Solo saca un unico objeto y lo elimina del inventario.
        """
        elemento_tmp = None
        for elemento in self.inventario:
            if elemento[0].id == elemento_seleccionado:
                # Elimina el elemento del inventario
                if elemento[1] - 1 > 0:         
                    elemento[1] -= 1
                    elemento_tmp = elemento[0]
                else:
                    elemento_tmp = elemento[0]
                    self.inventario.remove(elemento)
                break
        return elemento_tmp

    
        
            