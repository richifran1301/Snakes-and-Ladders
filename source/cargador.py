from abc import ABC, abstractmethod
from singleton import Singleton
from tkinter import *
from jugador import JugadorES
from casilla import Casilla,CasillaEscalera,CasillaEstandar,CasillaSerpiente
from conector import Conector, Escalera,Serpiente
from arbitro import ArbitroES
import pygame
import os
import sys
"""
Clase cargador, que sirve para tener diferentes maneras de cargar una partida, ademas pueden ser añadidas dinamicamente
para que existan diferentes formatos en los cuales cargar la partida

"""
class Cargador(ABC):
    def __init__(self):
        #self.nombre = nombreArchivo
        super().__init__()
    @abstractmethod
    def cargar(self):
        pass
"""
Clase cargadorTXT encargada de dictar como se cargara una partida en formato "txt", por lo que esta clase contiene metodos para este fin
"""
class CargadorTXT(Cargador):
    """
    Este metodo se encarga de inicializar la clase, este constructor es heredado de la clase "Cargador"
    @param: No tiene parametros
    @return: No retorna nada  
    """
    def __init__(self):
        super(CargadorTXT,self).__init__()
    """
    Este metodo se encarga de abrir el archivo donde estan los datos de la partida a cargar, si no existe, va a pedir un nombre valido hasta que
    se le indique uno. Una vez se haya abierto el archivo, se procede a leer los datos de este, que tienen un formato especifico creado en el "Almacenador", esta informacion se le pasa a la clase "Singleton" que es a donde va a acceder la vista para dibujar los elementos del tablero en el lugar donde estaban, con su respectivo color, forma...
    @param: No tiene parametros
    @return: No retorna nada
    
    """
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
        
        if(len(bufferLineas) < 7):
            raise Exception("Archivo incompleto.")

        #Primero va a leer los jugadores
        iterador = 0
        Singleton.cantidad_jugadores = int(bufferLineas[iterador])
        iterador += 1
        #TODO imprimir jugadores a ver si se respeta el orden de quien tira primero, fijo tengo que invertir el vector por el append
        for _ in range(Singleton.cantidad_jugadores):
            linea = bufferLineas[iterador]
            datos = linea.split("/")
            jugador = JugadorES(int(datos[1]), Singleton.casillasTablero[int(datos[1])].getCoordenadas()[0]+int(datos[3]), 
                                Singleton.casillasTablero[int(datos[1])].getCoordenadas()[1]+int(datos[4]), (Singleton.getAlto()//Singleton.getCantX())//4,
                                (Singleton.getAlto()//Singleton.getCantY())//4, int(datos[3]), int(datos[4]))
            jugador.setNombre(datos[0])
            jugador.mi_color = Singleton.colores_jugadores[str(datos[2])]
            jugador.colorString = str(datos[2])
            ArbitroES.reporte_jugadores(jugador)
            iterador += 1
        Singleton.jugadores_ordenados = Singleton.jugadores
            
        ArbitroES.decidiendoTurno = False
        ArbitroES.en_jugada = True
        #Despues va a leer las serpientes
        Singleton.cantidad_serpientes = int(bufferLineas[iterador])
        iterador += 1
        for _ in range(Singleton.cantidad_serpientes):
            linea = bufferLineas[iterador]
            linea.strip("\n")
            datos = linea.split("/")
            Singleton.indices_serpientes.append((int(datos[0]), int(datos[1])))
            iterador+=1

        #Despues va a leer las escaleras
        Singleton.cantidad_escaleras = int(bufferLineas[iterador])
        iterador += 1
        for _ in range(Singleton.cantidad_escaleras):
            linea = bufferLineas[iterador]
            linea.strip("\n")
            datos = linea.split("/")
            #print("METIENDO ESCALERAS DATOS DE "+datos[0]+", "+datos[1])
            Singleton.indices_escaleras.append((int(datos[0]), int(datos[1])))
            iterador+=1

        try:
            f.close()
        except:
            print("Ocurrio un error cerrando el archivo "+self.nombre_archivo)
       
    """
    Este metodo se encarga de recibir el nombre de la partida a cargar, si no existe, se vuelve a pedir hasta que se indique un nombre valido
    @param: No tiene parametros
    @return: No retorna nada
    """  

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
        Singleton.mantener_ventana_activa(root)
        root.mainloop()
