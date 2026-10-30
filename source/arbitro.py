import pygame
import random
from singleton import Singleton
from tablero import Tablero
from abc import ABC, abstractmethod
from casilla import Casilla, CasillaEstandar, CasillaEscalera, CasillaSerpiente


class Arbitro(ABC):
    """
    Clase abstracta que permite tener arbitros de diferentes juegos dinamicamente
    """

    
class ArbitroES(Arbitro):
    """
    Clase de ArbitroES que se encarga de revisar el comportamiento de los jugadores. Se encarga de
    asegurar el buen funcionamiento del juego y lo realiza de las siguientes maneras: comprueba si 
    un jugador gano; si se tiene que mover porque cayo en escaelera o serpiente (si lo hace, le dice
    hacia donde moverse), ayuda a decidir los turnos al inicio del juego, reporta los jugadores como
    existentes dentro del juego, se asegura que cada jugador tenga un color unico...
    """
    @classmethod
    def init(cls, controlador):
        """
        Inicializa el Arbitro.
        :param controlador: referencia al conrolador. 
        """
        cls.decidiendoTurno = True
        cls.en_jugada = False
        cls.jugadores = []
        cls.resultados = []
        cls.jugador_gano = False
        cls.valor_actual_dados = 0
        cls.controlador = controlador
        cls.cantidad_jugadores_tmp = 0


    @classmethod
    def comprobarGane(cls,pos):#comprueba si el jugador esta en la posicion ganadora y devuelve un bool
        """
        Este metodo se encarga de verificar si un jugador ha ganado la partida, se utiliza en cada jugada del jugador
        :param pos: Recibe la posicion de la casilla en la que se encuentra el jugador 
        :type pos: numero entero
        :returns: bool, devuelve true si el jugador en cuestion gano la partida
        """
        if pos == Singleton.pos_ganadora:
            ArbitroES.jugador_gano = True


    @classmethod
    def aplicarReglasMovimiento(cls, posTablero):             #comprueba si el jugador esta en una escalera o serpiente y lo mueve a donde le corresponde
        """
        Este metodo comprueba la posicion del jugador en el tablero y si en esa casilla hay una serpiente o escalera, y aplica el movimiento
        indicado
        :param posTablero: recibe la posicion del jugador en el tablero
        :type posTablero: numero entero
        :return distancia: retorna la distancia que se tiene que recorrer, ya sea al final de la serpiente o el tope de la escalera
        :return coordenadasNuevas: retorna las coordenadas de la nueva casilla hacia donde se va a mover el jugador
        """
        casillaActual = Singleton.casillasTablero[posTablero]
        distancia = 0
        coordenadasNuevas = []
        if not isinstance(casillaActual,CasillaEstandar):         #entra a la condicion si es serpiente o escalera
            if casillaActual.esInicio():
                casillaFinal = casillaActual.getFinal()
                ArbitroVista.muestre_accion_casilla_especial(casillaActual, casillaFinal)
                distancia = (posTablero - (casillaFinal.getIndice())) * (-1)
                coordenadasNuevas = casillaFinal.getCoordenadas()
                        
        return distancia,coordenadasNuevas

    @classmethod
    def reporte_jugadores(cls, jugador):
        """
        Este metodo agrega un Jugador a la lista de jugadores que tiene el Singleton, la cual es informacion importante para las demas clases
        :param jugador: recibe una instancia de un Jugador para agregarlo a la lista
        :type jugador: instancia de la clase jugador
        """
        Singleton.agregar_jugador(jugador)

    @classmethod
    def decidir_turnos(cls, cantidad_jugadores):
        """
        Este metodo se utiliza para decidir el orden de los turnos de los jugadores, cada uno lanza dados y el mas alto, va de primero y asi sucesivamente
        :param cantidad_jugadores: recibe la cantidad de jugadores que estan en la partida
        :type cantidad_jugadores: numero entero
        :param boton_dados: recibe una instancia de un boton de dados del cual se sacara la informacion de los dados
        :type boton_dados: instancia de la clase button
        :param dado: el dado que se lanzara para sacar un numero al azar
        :type dado: una instancia de dado
        """
        for i in range(cantidad_jugadores):
            cls.recibioDados = False
            cls.jugador_en_turno = i
            cls.controlador.muestre_turno_tirar_dados(i+1)
            cls.controlador.maneje_eventos()
        cls.decidiendoTurno = False
        cls.resultados.sort(reverse=True)
        for i in range (len(cls.resultados)):
            jugador = cls.buscar_jugador(cls.jugadores, cls.resultados[i])
            Singleton.jugadores_ordenados.append(jugador[0])
            cls.jugadores.remove(jugador)


    @classmethod
    def reciboRespuestaDados(cls, resultado_dados):
        """
        Este metodo se encarga de leer el resultado de dados, para decidir el orden de turnos 
        de los jugadores.
        :param resultado_dados: resultado de dados, se almacenara en un vector el jugador y su
        resultado especifico.
        """
        cls.recibioDados = True
        cls.resultados.append(resultado_dados)
        cls.jugadores.append( (Singleton.jugadores[cls.jugador_en_turno], resultado_dados) )

    @classmethod
    def jugador_juegue(cls, jugador):
        """
        Metodo que inicia el turno de un jugador, y espera al evento que este tire los dados.
        """
        cls.en_jugada = True
        cls.recibioDados = False
        cls.controlador.maneje_eventos()
    
    @classmethod
    def procesaRespuestaDados(cls, resultado_dados):
        """
        Este metodo se encarga de leer el resultado de dados, para decidir el movimiento del jugador.
        Tambien indica el final de la jugada del jugador, y el Arbitro analizara posteriormente el
        movimiento del jugador.
        :param resultado_dados: resultado de dados, se almacenara en self.valor_actual_dados.
        """
        cls.recibioDados = True
        cls.valor_actual_dados = resultado_dados
        cls.en_jugada = False


    @classmethod
    def buscar_jugador(cls, jugadores, valor):
        """
        Este metodo busca un jugador dentro del vector de turnos de acuerdo al valor que saco en los dados
        :param jugadores: el vector que guarda los turnos de los jugadores
        :type jugadores: un array de Jugador
        :param valor: la cantidad que tiro en los dados el jugador
        :type valor: numero entero
        """
        for jugador in jugadores:
            if jugador[1] == valor:
                return jugador

    @classmethod
    def setColorJugador(cls, jugador):
        """
        Le asigna al Jugador un color al azar de entre los colores disponibles que no hayan sido usados.
        El color es unico por jugador en la partida.
        """
        colores_libres = [llave for llave in Singleton.colores_jugadores if llave not in Singleton.colores_jugadores_usados]
        color = random.choice(colores_libres)
        Singleton.colores_jugadores_usados.append(color)
        jugador.mi_color = Singleton.colores_jugadores[color]
        jugador.rel_ficha.setColor(Singleton.colores_jugadores[color])
        jugador.colorString = color

    @classmethod
    def obtener_destino(cls, index, resultado_dados):
        """
        Metodo que va a conseguir las coordenadas de la casilla adonde el jugador tiene
        que moverse. 
        :param index: posicion en el tablero donde esta el usuario
        :type index: int
        :param resultado_dados: cantidad de casillas a moverse
        :type resultado_dados: int
        """
        #verifica que no pase de 100
        if index + resultado_dados > 99:
            index = (index+resultado_dados)-100
        else:
            index = index+resultado_dados
        #Despues calcula las coordenadas de la siguiente posicion a estar
        if isinstance(Singleton.casillasTablero[index], CasillaEstandar):
            coordenadas = Singleton.casillasTablero[index].getCoordenadas()
        else:
            coordenadas = Singleton.casillasTablero[index].getCoordenadas()
        return coordenadas

class ArbitroVista():
    
    @classmethod
    def muestre_accion_casilla_especial(cls, casillaActual, casillaFinal):
        X = 1650
        Y = 750
        Y2 = Y + 50
        font = pygame.font.Font('freesansbold.ttf', 15) 
        if isinstance(casillaActual, CasillaSerpiente):
            text = font.render("BAJO POR SERPIENTE", True, Singleton.colores_casillas["negro"], Singleton.colores_casillas["rojo"]) 
        else:
            text = font.render("SUBIO POR ESCALERA", True, Singleton.colores_casillas["negro"], Singleton.colores_casillas["verde"])
        text2 =  font.render("DESDE: " + str(casillaActual.getIndice()+1) + " HASTA: " + str(casillaFinal.getIndice()+1), True, Singleton.colores_casillas["negro"], Singleton.colores_casillas["blanco"])
        textRect = text.get_rect()  
        textRect2 = text.get_rect()
        textRect.center = (X // 2, Y // 2) 
        textRect2.center = (X // 2, Y2 // 2) 
        Singleton.ventana.blit(text, textRect)
        Singleton.ventana.blit(text2, textRect2)
    