from abc import ABC, abstractmethod

class ElementoInventario(ABC):
    def __init__(self):
        super().__init__()


class Ficha(ElementoInventario):
    def __init__(self, figura):
        super().__init__()
        self.figura = figura

    def setColor(self, color):
        self.mi_color = color
        
    def mover(self, movX, movY):
        self.figura.x = movX              
        self.figura.y = movY             



class Inventario:

    def __init__(self):
        self.inventario = []          #(Objeto, cantidad)
    
    def agregar(self, elemento_nuevo, cantidad):
        es_nuevo = True
        for elemento in self.inventario:
            if elemento[0] == elemento_nuevo:
                elemento[1] += cantidad
                es_nuevo = False
                break
        if es_nuevo:
            self.inventario.append((elemento_nuevo, cantidad))

    def eliminar(self, elemento_seleccionado, cantidad):
        for elemento in self.inventario:
            if elemento[0] == elemento_seleccionado:
                if elemento[1] - cantidad > 0:
                    elemento[1] -= cantidad
                else:
                    self.inventario.remove(elemento)
                break

    def buscar_en_inventario(self, elemento_seleccionado):
        cantidad = 0
        for elemento in self.inventario:
            if elemento[0] == elemento_seleccionado:
                cantidad = elemento[1]
                break
        return cantidad
        
            