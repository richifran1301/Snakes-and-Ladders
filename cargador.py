from abc import ABC, abstractmethod
from singleton import Singleton
from tkinter import *
from jugador import Jugador
from casilla import Casilla,CasillaEscalera,CasillaEstandar,CasillaSerpiente
from conector import Conector, Escalera,Serpiente
import pygame
class Cargador(ABC):
    def __init__(self):
        #self.nombre = nombreArchivo
        super().__init__()
    @abstractmethod
    def cargar(self):
        pass
class CargadorTXT(Cargador):
    def __init__(self):
        super(CargadorTXT,self).__init__()
    def cargar(self):
        root = Tk() 
        root.title("C PARTIDA")
        root.geometry("450x360")         
        NC_label = Label(root, text = "Nombre de partida a cargar:")
        NC_label.grid(row = 1, column = 1)         
        NC_Int = StringVar()
        NC_entry = Entry(root, textvariable = NC_Int)
        NC_entry.grid(row = 1, column = 2)         
        numcur=NC_Int.get()         
        ok = Button(root,text = "CARGAR",command = root.destroy)
        ok.grid(row = 2, column = 2)
        def mostrar():
            numcur = NC_Int.get()
            self.nombre = numcur
            root.destroy()
        ok.config(command=mostrar)
        root.mainloop()
        print("NOMBRE LEIDO ",self.nombre)
        self.nombre += ".txt"
        f = open(self.nombre,"r+") #si no esta creado, borra todo y escribe de cero
        bufferLineas = f.readlines()
        iterador = 0
        Singleton.cantidad_jugadores = int(bufferLineas[iterador])
        iterador += 1
        print("CANT JUGADORES: ",Singleton.cantidad_jugadores)
        while iterador <= Singleton.cantidad_jugadores:
            linea = bufferLineas[iterador]
            datos = linea.split("/")
            jugador = Jugador(int(datos[1]), Singleton.casillasTablero[int(datos[1])].getCoordenadas()[0],  Singleton.casillasTablero[int(datos[1])].getCoordenadas()[1],(Singleton.getAlto()//Singleton.getCantX())//4,(Singleton.getAlto()//Singleton.getCantY())//4, int(datos[3]), int(datos[4]))
            jugador.setNombre(datos[0])
            jugador.mi_color = Singleton.colores_jugadores[str(datos[2])]
            Singleton.jugadores.append(jugador)
            iterador +=1
        Singleton.cantidad_serpientes = int(bufferLineas[iterador])
        iterador += 1
        print("CANT SERPIENTES: ",Singleton.cantidad_serpientes)
        #error aqui
        figura = pygame.Rect(Singleton.casillasTablero[0].getCoordenadas()[0] - int((Singleton.alto_tablero//self.tamanio[0])//2), Singleton.casillasTablero[int(datos[1])].getCoordenadas()[1] - int((Singleton.ancho_tablero//self.tamanio[1])/2), Singleton.alto_tablero//self.tamanio[0], Singleton.ancho_tablero//self.tamanio[1])
        for indice in range(Singleton.cantidad_serpientes):
            linea = bufferLineas[iterador]
            datos = linea.split("/")
            casilla1 = CasillaSerpiente(Singleton.casillasTablero[int(datos[0])].getCoordenadas(),(255,255,255), figura, datos[0], Singleton.ventana)
            casilla2 = CasillaSerpiente(Singleton.casillasTablero[int(datos[1])].getCoordenadas(),(255,255,255), figura, datos[1], Singleton.ventana)
            conector = Serpiente((casilla1,casilla2),Singleton.ventana)
            Singleton.serpientes.append(conector)
            printf("SERPIENTE1: ",datos[0])
            printf("SERPIENTE2: ",datos[1])
            iterador+=1
        Singleton.cantidad_escaleras = int(bufferLineas[iterador])
        iterador += 1     
        for indice in range(Singleton.cantidad_escaleras):
            linea = bufferLineas[iterador]
            datos = linea.split("/")
            casilla1 = CasillaEscalera(Singleton.casillasTablero[int(datos[0])].getCoordenadas(),(255,255,255), figura, datos[0], Singleton.ventana)
            casilla2 = CasillaEscalera(Singleton.casillasTablero[int(datos[1])].getCoordenadas(),(255,255,255), figura, datos[1], Singleton.ventana)
            conector = Escalera((casilla1,casilla2),Singleton.ventana)
            Singleton.escaleras.append(conector)
            printf("ESCALERA1: ",datos[0])
            printf("ESCALERA2: ",datos[1])
            iterador+=1
        f.close()
       
        #HACER QUE LEA BIEN LOS DATOS
        #
