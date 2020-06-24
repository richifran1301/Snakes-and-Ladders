from abc import ABC, abstractmethod
from singleton import Singleton
from tkinter import *
from jugador import Jugador
from casilla import Casilla,CasillaEscalera,CasillaEstandar,CasillaSerpiente
from conector import Conector, Escalera,Serpiente
from arbitro import Arbitro
import pygame
import os
import sys

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
        f = None
        es_invalido = True
        while es_invalido: 
            self.obtener_nombre_guardado()
            #Comienza a leer del archivo
            self.nombre += ".txt"
            if not os.path.exists(self.nombre) or os.path.getsize(self.nombre) == 0:
                print("El archivo no existe, esta vacio")
            else:
                es_invalido = False
        try:
            f = open(self.nombre,"r+") #si no esta creado, borra todo y escribe de cero
        except:
            print("Ocurrio un error al abrir el archivo "+self.nombre_archivo)
        
        bufferLineas = f.readlines()
        
        if(len(bufferLineas) < 8):
            raise Exception("Archivo incompleto.")

        #Primero va a leer los jugadores
        iterador = 0
        Singleton.cantidad_jugadores = int(bufferLineas[iterador])
        iterador += 1
        #TODO imprimir jugadores a ver si se respeta el orden de quien tira primero, fijo tengo que invertir el vector por el append
        for _ in range(Singleton.cantidad_jugadores):
            linea = bufferLineas[iterador]
            datos = linea.split("/")
            jugador = Jugador(int(datos[1]), Singleton.casillasTablero[int(datos[1])].getCoordenadas()[0]+int(datos[3]), 
                                Singleton.casillasTablero[int(datos[1])].getCoordenadas()[1]+int(datos[4]), (Singleton.getAlto()//Singleton.getCantX())//4,
                                (Singleton.getAlto()//Singleton.getCantY())//4, int(datos[3]), int(datos[4]))
            jugador.setNombre(datos[0])
            jugador.mi_color = Singleton.colores_jugadores[str(datos[2])]
            Arbitro.reporte_jugadores(jugador)
            iterador += 1
        Singleton.jugadores_ordenados = Singleton.jugadores
            
        Arbitro.decidiendoTurno = False
        Arbitro.en_jugada = True
        #Despues va a leer las serpientes
        Singleton.cantidad_serpientes = int(bufferLineas[iterador])
        iterador += 1
        for _ in range(Singleton.cantidad_serpientes):
            linea = bufferLineas[iterador]
            datos = linea.split("/")
            #Implementacion de la casilla1
            figura = pygame.Rect(Singleton.casillasTablero[int(datos[0])].getCoordenadas()[0] - int((Singleton.alto_tablero//Singleton.cantidad_x)/2), 
                                Singleton.casillasTablero[int(datos[0])].getCoordenadas()[1] - int((Singleton.ancho_tablero//Singleton.cantidad_y)/2), 
                                Singleton.alto_tablero//Singleton.cantidad_x, Singleton.ancho_tablero//Singleton.cantidad_y)
            casilla1 = CasillaSerpiente(Singleton.casillasTablero[int(datos[0])].getCoordenadas(),(255,255,255), figura, datos[0], Singleton.ventana)

            #Implementacion de la casilla2
            figura = pygame.Rect(Singleton.casillasTablero[int(datos[1])].getCoordenadas()[0] - int((Singleton.alto_tablero//Singleton.cantidad_x)//2), 
                                Singleton.casillasTablero[int(datos[1])].getCoordenadas()[1] - int((Singleton.ancho_tablero//Singleton.cantidad_y)/2), 
                                Singleton.alto_tablero//Singleton.cantidad_x, Singleton.ancho_tablero//Singleton.cantidad_y)
            casilla2 = CasillaSerpiente(Singleton.casillasTablero[int(datos[1])].getCoordenadas(),(255,255,255), figura, datos[1], Singleton.ventana)
            
            #Se unen mediante el conector
            conector = Serpiente((casilla1,casilla2),Singleton.ventana)
            Singleton.serpientes.append(conector)
            iterador+=1


        #Despues va a leer las escaleras
        Singleton.cantidad_escaleras = int(bufferLineas[iterador])
        iterador += 1
        for _ in range(Singleton.cantidad_escaleras):
            linea = bufferLineas[iterador]
            datos = linea.split("/")

            #Implementacion de la casilla1
            figura = pygame.Rect(Singleton.casillasTablero[int(datos[0])].getCoordenadas()[0] - int((Singleton.alto_tablero//Singleton.cantidad_x)//2), 
                                Singleton.casillasTablero[int(datos[0])].getCoordenadas()[1] - int((Singleton.ancho_tablero//Singleton.cantidad_y)/2), 
                                Singleton.alto_tablero//Singleton.cantidad_x, Singleton.ancho_tablero//Singleton.cantidad_y)
            casilla1 = CasillaEscalera(Singleton.casillasTablero[int(datos[0])].getCoordenadas(),(255,255,255), figura, datos[0], Singleton.ventana)

            #Implementacion de la casilla2
            figura = pygame.Rect(Singleton.casillasTablero[int(datos[1])].getCoordenadas()[0] - int((Singleton.alto_tablero//Singleton.cantidad_x)//2), 
                                Singleton.casillasTablero[int(datos[1])].getCoordenadas()[1] - int((Singleton.ancho_tablero//Singleton.cantidad_y)/2), 
                                Singleton.alto_tablero//Singleton.cantidad_x, Singleton.ancho_tablero//Singleton.cantidad_y)
            casilla2 = CasillaEscalera(Singleton.casillasTablero[int(datos[1])].getCoordenadas(),(255,255,255), figura, datos[1], Singleton.ventana)

            #Se unen mediante el conector
            conector = Escalera((casilla1,casilla2),Singleton.ventana)
            Singleton.escaleras.append(conector)
            iterador+=1

        try:
            f.close()
        except:
            print("Ocurrio un error cerrando el archivo "+self.nombre_archivo)
       
        

    def obtener_nombre_guardado(self):
        root = Tk() 
        root.title("Cargar partida")
        root.geometry("450x360")     
        NC_label = Label(root, text = "Nombre de partida a cargar:")
        NC_label.grid(row = 1, column = 1)         
        NC_Int = StringVar()
        NC_entry = Entry(root, textvariable = NC_Int)
        NC_entry.grid(row = 1, column = 2)         
        NC_Int.get()         
        ok = Button(root,text = "CARGAR",command = root.destroy)
        ok.grid(row = 2, column = 2)
        def mostrar():
            numcur = NC_Int.get()
            self.nombre = "Guardado/"+numcur
            self.nombre_archivo = numcur
            root.destroy()
        ok.config(command=mostrar)
        root.mainloop()