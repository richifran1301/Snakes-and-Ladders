import os
import time
import random
import itertools
import sys, pygame
from pygame.locals import *
#from button import Button
from sidebar import Sidebar
from conector import Conector, Escalera, Serpiente
from casilla import Casilla, CasillaEstandar, CasillaEscalera, CasillaSerpiente
from singleton import Singleton

class Tablero():
    """
    Esta clase representa un tablero de juego, y contiene los
    atributos y acciones necesarios para su graficación y comportamiento.
    """

    def __init__(self, tamanio, ventana, ancho_barra):
        """
        :param tamanio: Tamaño del tablero en píxeles como tupla (ancho, alto).
        :type tamanio: tuple
        :param ventana: Referencia a la ventana de pygame.
        :type ventana: pygame.display
        :param ancho_barra: Ancho de la sidebar junto al tablero.
        :type ancho_barra: int
        """
        self.tamanio = tamanio
        self.ventana = ventana
        self.casillas = []              # lista de casillas del tablero
        self.serpientes = []            # lista de conectores tipo serpiente del tablero
        self.escaleras = []             # lista de conectores tipo escalera del tablero
        self.generarCasillas()          # se llama a la función que genera casillas
        self.colorearCasillas()
        self.dibujarCasillas()
        self.ancho_barra = ancho_barra
        
    def generarCasillas(self):
        """
        Este método genera casillas y sus conectores para un tablero de Serpientes y escaleras de manera aleatoria.
        :returns:  None -- Procedimiento sin valor de retorno.
        """
        
        alto, ancho = 700, 700 # tamanio del tablero
        
        # las serpientes y escaleras serán cada una un total de entre 5% y 7% de la cantidad total de casillas
        # estos números se determinan aleatoriamente
        cantidad_serpientes = int((self.tamanio[0] * self.tamanio[1]) * ((random.randint(5, 7)) * 0.01))
        cantidad_escaleras = int((self.tamanio[0] * self.tamanio[1]) * ((random.randint(5, 7)) * 0.01))

        # se invoca al método que da las coordenadas de los centros de todas las casillas
        centros_casillas = self.obtener_centro_casillas(alto, ancho)
        
        # se invoca al método que indica en qué posiciones irán las serpientes y escaleras, cuya cantidad ya calculamos
        # estas posiciones vienen en tuplas con la posición inicial y final de cada serpiente o escalera
        posiciones_serpientes, posiciones_escaleras = self.generar_conexiones(centros_casillas, cantidad_serpientes, cantidad_escaleras)
        
        
        for i in range(len(centros_casillas)):  # para cada posición en el vector de centros_casilla, o sea, cada posición de todas las casillas
            encontrado = False                  # asuma que no ha encontrado una posición de serpiente en las posiciones generales
            
            for j in range(len(posiciones_serpientes)):     # haga esto tantas veces como la cant. de serpientes

                if not encontrado and i in posiciones_serpientes[j]:    # si no ha encontrado aún la posición y por fin la encuentra
                    # cree un rectángulo como forma para la casilla
                    figura = pygame.Rect(centros_casillas[i][0] - int((alto//self.tamanio[0])//2), centros_casillas[i][1] - int((ancho//self.tamanio[1])/2), alto//self.tamanio[0], ancho//self.tamanio[1])
                    # cree una casilla como una casilla de tipo serpiente
                    serpiente = CasillaSerpiente(centros_casillas[i], (255,255,255), figura, i, self.ventana)
                    # agréguela al vector de casillas general una vez decorada
                    self.casillas.append(serpiente)
                    # encontré la posición de una serpiente
                    encontrado = True

                if encontrado:  # si encontró la posición de la serpiente, detenga el ciclo
                    break

            for k in range(len(posiciones_escaleras)):      # haga esto tantas veces como la cant. de escaleras

                if not encontrado and i in posiciones_escaleras[k]:     # si no ha encontrado aún la posición y por fin la encuentra
                    # cree un rectángulo como forma para la casilla
                    figura = pygame.Rect(centros_casillas[i][0] - int((alto//self.tamanio[0])//2), centros_casillas[i][1] - int((ancho//self.tamanio[1])/2), alto//self.tamanio[0], ancho//self.tamanio[1])
                    # cree una casilla como una casilla de tipo escalera
                    escalera = CasillaEscalera(centros_casillas[i], (255,255,255), figura, i, self.ventana)
                    # agréguela al vector de casillas general una vez decorada
                    self.casillas.append(escalera)
                    # encontré la posición de una escalera
                    encontrado = True

                if encontrado:  # si encontró la posición de la escalera, detenga el ciclo
                    break

            if not encontrado:          # si la posición no se encontró en las pensadas para serpiente o escalera
                # cree un rectángulo como forma para la casilla
                figura = pygame.Rect(centros_casillas[i][0] - int((alto//self.tamanio[0])//2), centros_casillas[i][1] - int((ancho//self.tamanio[1])//2), alto//self.tamanio[0], ancho//self.tamanio[1])
                # cree una casilla estándar con la forma anteriormente creada
                casillaEstandar = CasillaEstandar(centros_casillas[i], (255,255,255), figura, i, self.ventana)
                # agréguela al vector de casillas general (no requiere decorador, porque es estándar)
                self.casillas.append(casillaEstandar)

        for i in range(len(self.casillas)):     # para cada una de las casillas totales ya generadas

            if isinstance(self.casillas[i], CasillaSerpiente):      # si la casilla es de tipo serpiente
                if not self.existeConexion(self.casillas[i].getIndice()):   # si esta casilla no tiene conectores
                    # cree un conector como una serpiente y añádalo a la lista de serpientes del tablero
                    self.serpientes.append(Serpiente(self.getPar(self.casillas[i].getIndice(), posiciones_serpientes), self.ventana))
                    # el conector avisará a sus casillas relacionadas que él es su conector
                    self.serpientes[len(self.serpientes) - 1].sendConector()

            elif isinstance(self.casillas[i], CasillaEscalera):     # si la casilla es de tipo escalera
                if not self.existeConexion(self.casillas[i].getIndice()):   # si esta casilla no tiene conectores
                    # cree un conector como una escalera y añádalo a la lista de escaleras del tablero
                    self.escaleras.append(Escalera(self.getPar(self.casillas[i].getIndice(), posiciones_escaleras), self.ventana))
                    # el conector avisará a sus casillas relacionadas que él es su conector
                    self.escaleras[len(self.escaleras) - 1].sendConector()
        Singleton.serpientes = self.serpientes
        Singleton.escaleras = self.escaleras
        #for i in range(len(self.casillas)):
            #if not isinstance(self.casillas[i], CasillaEstandar):
                #print(self.casillas[i].casilla.getIndice() + 1, self.casillas[i].casilla.getFinal() + 1, self.casillas[i].casilla.esInicio())
                
    def getPosicionesEnTupla(self, indice, posiciones):
        """
        Esta función devuelve la tupla de índices inicio y fin donde se encuentra un índice de casilla.
        :param indice: El índice de la casilla en la lista general de casillas.
        :type indice: int
        :param posiciones: Lista de tuplas con las posiciones inicial y final de cada serpiente o escalera.
        :type posiciones: list
        :returns:  tuple/None -- Devuelve la tupla si se encontró, si no, devuelve None.
        """
        for i in posiciones:    # para cada tupla (de posiciones_serpiente o posiciones_escalera)
            if indice in i:     # si el índice está en la tupla
                return i        # devuelva la tupla
        return

    def getPar(self, indice, posiciones):
        """
        Esta función devuelve la tupla de casillas correspondiente a una tupla de índices inicio y fin.
        :param indice: El índice de la casilla en la lista general de casillas.
        :type indice: int
        :param posiciones: Lista de tuplas con las posiciones inicial y final de cada serpiente o escalera.
        :type posiciones: list
        :returns:  tuple -- Devuelve la tupla de dos casillas, la de inicio en pos 0 y la de fin en pos 1.
        """

        temp_par = self.getPosicionesEnTupla(indice, posiciones)            # obtenga la tupla de posiciones donde está ese índice
        tupla = (self.casillas[temp_par[0]], self.casillas[temp_par[1]])    # obtenga la versión de esa tupla con objetos Casilla

        return tupla

    def existeConexion(self, indice):
        """
        Esta función indica si una casilla ya está conectada con otra.
        :param indice: El índice de la casilla en la lista general de casillas.
        :type indice: int
        :returns:  bool -- Devuelve True si la casilla en ese índice ya está relacionada con un conector.
        """

        for i in range(len(self.serpientes)):       # para cada serpiente
            # si esa serpiente está relacionada con la casilla posicionada en el índice dado
            if indice == self.serpientes[i].getCasillaInicio().getIndice() or indice == self.serpientes[i].getCasillaFinal().getIndice():
                return True     # indique verdadero

        for i in range(len(self.escaleras)):       # para cada escalera
            # si esa escalera está relacionada con la casilla posicionada en el índice dado
            if indice == self.escaleras[i].getCasillaInicio().getIndice() or indice == self.escaleras[i].getCasillaFinal().getIndice():
                return True     # indique verdadero

        return False            # de lo contrario, indique falso

    def generar_serpientes(self, escaleras, casillas, cantidad):
        """
        Esta función genera tuplas con las posiciones de inicio y fin de n serpientes dadas.
        :param escaleras: Lista de escaleras (necesaria para no crear serpientes donde hay escaleras).
        :type escaleras: list
        :param casillas: Lista de todas las casillas.
        :type casillas: list
        :param cantidad: Cantidad deseada de serpientes (n).
        :type cantidad: int
        :returns:  list -- Devuelve un vector con posiciones de serpientes, pares inicios, impares fines, consecutivos.
        """

        serpientes_temp = []
        generados = 0
        while generados < cantidad * 2: # mientras la cantidad de serpientes generadas sea menor al doble de las deseadas (porque son pares)
            while True:
                valor = random.randint(1, len(casillas) - 2)                    # cree una posición de casilla aleatoria
                if (valor not in escaleras) and (valor not in serpientes_temp): # si esa posición no es escalera ni serpiente aún
                    serpientes_temp.append(valor)                               # hágala serpiente
                    break
            generados += 1                                                      # aumente por uno los generados
        
        return serpientes_temp

    def generar_escaleras(self, casillas, cantidad):
        """
        Esta función genera tuplas con las posiciones de inicio y fin de n escaleras dadas.
        :param casillas: Lista de todas las casillas.
        :type casillas: list
        :param cantidad: Cantidad deseada de escaleras (n).
        :type cantidad: int
        :returns:  list -- Devuelve un vector con posiciones de escaleras, pares inicios, impares fines, consecutivos.
        """

        escaleras_temp = []
        generados = 0

        while generados < cantidad * 2: # mientras la cantidad de serpientes generadas sea menor al doble de las deseadas (porque son pares)
            while True:
                valor = random.randint(1, len(casillas) - 2)                    # cree una posición de casilla aleatoria
                if valor not in escaleras_temp:                                 # si esa posición no es escalera aún
                    escaleras_temp.append(valor)                                # hágala escalera
                    break
            generados += 1                                                      # aumente por uno los generados

        return escaleras_temp

    def generar_conexiones(self, casillas, cantidad_serpientes, cantidad_escaleras):
        """
        Esta función genera dos listas de tuplas a partir de ciertas posiciones, una para serpientes y otra para escaleras. 
        Las tuplas tienen los índices de casillas de inicio y fin de cada serpiente o escalera.
        :param casillas: Lista de todas las casillas.
        :type casillas: list
        :param cantidad_serpientes: Cantidad deseada de serpientes (n).
        :type cantidad_serpientes: int
        :param cantidad_escaleras: Cantidad deseada de escaleras (m).
        :type cantidad_escaleras: int
        :returns:  tuple -- Devuelve como tupla las dos listas con tuplas de posiciones de serpientes y escaleras.
        """

        # genere los vectores con índices aleatorios de dos en dos que representan tuplas
        escaleras_temp = self.generar_escaleras(casillas, cantidad_escaleras)
        serpientes_temp = self.generar_serpientes(escaleras_temp, casillas, cantidad_serpientes)

        escaleras = []
        serpientes = []

        for i in range(0, len(escaleras_temp), 2):  # para cada par en el vector de índices de escaleras

            valorInicial = 0
            valorFinal = 0

            # ordene el par depende de quién es mayor
            # el valor menor debe ir en la primera posición
            # el valor mayor debe ir en la segunda posición
            if escaleras_temp[i] < escaleras_temp[i+1]:     
                valorInicial = escaleras_temp[i]            
                valorFinal = escaleras_temp[i+1]
            else:
                valorInicial = escaleras_temp[i+1]
                valorFinal = escaleras_temp[i]

            tupla = (valorInicial, valorFinal)      # agrupe el par como tupla
            escaleras.append(tupla)                 # añádalo a las posiciones de escaleras como una tupla (inicio, fin)

        for i in range(0, len(serpientes_temp), 2): # para cada par en el vector de índices de escaleras

            valorInicial = 0
            valorFinal = 0

            # ordene el par depende de quién es mayor
            # el valor mayor debe ir en la primera posición
            # el valor menor debe ir en la segunda posición
            if serpientes_temp[i] > serpientes_temp[i+1]:
                valorInicial = serpientes_temp[i]
                valorFinal = serpientes_temp[i+1]
            else:
                valorInicial = serpientes_temp[i+1]
                valorFinal = serpientes_temp[i]

            tupla = (valorInicial, valorFinal)      # agrupe el par como tupla
            serpientes.append(tupla)                # añádalo a las posiciones de escaleras como una tupla (inicio, fin)

        return serpientes, escaleras

    def obtener_orden_coordenadas(self, centro_casillas_x, centro_casillas_y):
        """
        Esta función genera una lista con las coordenadas de cada casilla en el orden lógico de recorrido del tablero. 
        :param centro_casillas_x: Lista de centros de casillas en eje x.
        :type centro_casillas_x: list
        :param centro_casillas_y: Lista de centros de casillas en eje y.
        :type centro_casillas_y: list
        :returns:  list -- Devuelve la lista con coordenadas de todas las casillas (x, y) como tuplas.
        """

        casillas_temp = []
        temp = centro_casillas_x

        # favor documentar el funcionamiento de este algoritmo
        for i in range(0, len(centro_casillas_y)):
            if(i % 2 == 0):
                for j in range(len(centro_casillas_x)):
                    tupla_temp = (centro_casillas_x[j], centro_casillas_y[i])
                    casillas_temp.append(tupla_temp)
            else:
                for k in range(len(temp)):
                    tupla_temp = (temp[k], centro_casillas_y[i])
                    casillas_temp.append(tupla_temp)
            temp.reverse()
        
        return casillas_temp

    def obtener_casillas(self, x, max_iteracion):
        """
        Esta función genera una lista con las coordenadas de cada casilla en el orden lógico de recorrido del tablero. 
        :param x: Ancho de la casilla.
        :type x: int
        :param max_iteracion: Máxima cantidad de coordenadas por generar.
        :type max_iteracion: int
        :returns:  list -- Devuelve una lista con coordenadas que representan centros.
        """

        # favor documentar el funcionamiento de este algoritmo
        centro_casillas = []    
        for i in range(max_iteracion):
            centro_casillas.append(int(x/2) + (i*x))
        return centro_casillas

    def obtener_centro_casillas(self, ancho_total, alto_total):
        """
        Esta función calcula una cantidad de casillas basado en el tamaño del tablero, y arroja la lista de sus centros. 
        :param ancho_total: Ancho total del tablero.
        :type ancho_total: int
        :param alto_total: Alto total del tablero.
        :type alto_total: int
        :returns:  list -- Devuelve una lista con coordenadas que representan centros.
        """
    
        centro_casillas = []
        centro_casillas_x = []
        centro_casillas_y = []

        # favor documentar el funcionamiento de este algoritmo
        cantidad_casillas_x, cantidad_casillas_y = self.tamanio[0], self.tamanio[1]
        ancho_casilla = int(ancho_total/cantidad_casillas_x)
        altura_casilla = int(alto_total/cantidad_casillas_y)
    
        centro_casillas_x = self.obtener_casillas(ancho_casilla, cantidad_casillas_x)
        centro_casillas_y = self.obtener_casillas(altura_casilla, cantidad_casillas_y)
    
        centro_casillas_y.reverse()
    
        centro_casillas = self.obtener_orden_coordenadas(centro_casillas_x, centro_casillas_y)
    
        return centro_casillas

    def colorearCasillas(self):
        """
        Esta función colorea las casillas con un algoritmo que impide colores consecutivos. 
        :returns:  None -- Procedimiento sin valor de retorno.
        """

        colores_x = ["amarillo", "blanco", "rojo", "azul", "verde"]

        i = 0
        indice_color_x = 0
        indice_color_y = 0
        par_actual, par_final = 0, self.tamanio[0]
        impar_actual, impar_final = self.tamanio[0] * 2 - 1, self.tamanio[0] - 1

        # favor documentar este algoritmo
        while i < self.tamanio[1] // 2: 
            #Coloreado filas pares
            for j in range (par_actual, par_final):
                if isinstance(self.casillas[j], CasillaEstandar):
                    self.casillas[j].setColor(colores_x[indice_color_x])
                else:
                    self.casillas[j].setColor(colores_x[indice_color_x])
                
                indice_color_x += 1
                if indice_color_x > 4:
                    indice_color_x = 0

            #Coloreado filas impares
            for j in range (impar_actual, impar_final, -1):
                if isinstance(self.casillas[j], CasillaEstandar):
                    self.casillas[j].setColor(colores_x[(indice_color_x + 3) % 5])
                else:
                    self.casillas[j].setColor(colores_x[(indice_color_x + 3) % 5])
                
                indice_color_x += 1
                if indice_color_x > 4:
                    indice_color_x = 0
            
            indice_color_y += 1 
            if indice_color_y > 4:
                indice_color_y = 0

            indice_color_x = indice_color_y

            par_actual += self.tamanio[0] * 2
            par_final += self.tamanio[0] * 2

            impar_actual += self.tamanio[0] * 2
            impar_final += self.tamanio[0] * 2

            i += 1
 
        return

    def dibujarCasillas(self):
        """
        Esta función dibuja las casillas y sus conectores en la ventana.
        :returns:  None -- Procedimiento sin valor de retorno.
        """

        for c in self.casillas:
            c.dibujar()             # y las estándar

        for i in self.serpientes:   # para cada serpiente
            i.dibujar()             # dibújese
        
        for i in self.escaleras:    # para cada escalera
            i.dibujar()             # dibújese


    #TODO mejorar condicion de limpieza
    def limpar_casilla(self, index):
        """
        Metodo que limpia la casilla actual donde se ubica el jugador. 
        :param index: posicion en el tablero donde esta el usuario
        :type index: int
        """
        #Primero limpia la posicion actual
        if isinstance(self.casillas[index], CasillaEstandar):
            self.casillas[index].dibujar()
        else:
            self.casillas[index].casilla.dibujar()
            conector = self.casillas[index].casilla.getConector()
            if isinstance(conector, Serpiente):      #dibuja si hay serpiente 
                #lo intente simplemente conector.dibujar() pero tampoco
                #conector.dibujar()
                self.serpientes.index(conector).dibujar()
            elif isinstance(conector, Escalera):      #dibuja si hay escalera
                self.escaleras.index(conector).dibujar()




