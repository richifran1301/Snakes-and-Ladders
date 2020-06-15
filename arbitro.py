from singleton import Singleton
from tablero import Tablero
from casilla import Casilla, CasillaEstandar, CasillaEscalera, CasillaSerpiente

class Arbitro():
    """
    Clase de Arbitro que se encarga de revisar el comportamiento de los jugadores. Se encarga de
    asegurar el buen funcionamiento del juego y lo realiza de las siguientes maneras: comprueba si 
    un jugador gano; si se tiene que mover porque cayo en escaelera o serpiente (si lo hace, le dice
    hacia donde moverse), ayuda a decidir los turnos al inicio del juego, reporta los jugadores como
    existentes dentro del juego, se asegura que cada jugador tenga un color unico...
    """
    @classmethod
    def init(cls):
        pass
    """
    Este metodo se encarga de verificar si un jugador ha ganado la partida, se utiliza en cada jugada del jugador
    @param pos: Recibe la posicion de la casilla en la que se encuentra el jugador 
    @type pos: numero entero
    @returns: bool, devuelve true si el jugador en cuestion gano la partida
    """
    @classmethod
    def comprobarGane(cls,pos):#comprueba si el jugador esta en la posicion ganadora y devuelve un bool
        gano = False             #si las coordenadas de jugador son iguales a las de la casilla ganadora, gana = True
        if pos == Singleton.pos_ganadora:
            gano = True
        return gano
    """
    Este metodo comprueba la posicion del jugador en el tablero y si en esa casilla hay una serpiente o escalera, y aplica el movimiento
    indicado
    @param posTablero: recibe la posicion del jugador en el tablero
    @type posTablero: numero entero
    @return distancia: retorna la distancia que se tiene que recorrer, ya sea al final de la serpiente o el tope de la escalera
    @return coordenadasNuevas: retorna las coordenadas de la nueva casilla hacia donde se va a mover el jugador
    
    """
    @classmethod
    def aplicarReglasMovimiento(cls, posTablero):             #comprueba si el jugador esta en una escalera o serpiente y lo mueve a donde le corresponde
        casillaActual = Singleton.casillasTablero[posTablero]
        distancia = 0
        coordenadasNuevas = []
        if not isinstance(casillaActual,CasillaEstandar):         #entra a la condicion si es serpiente o escalera
            if casillaActual.esInicio():
                casillaFinal = casillaActual.getFinal()
                if isinstance(casillaActual, CasillaSerpiente):             #entra si la casilla actual es serpiente
                    if isinstance(casillaFinal, CasillaEstandar):
                        print("BAJE POR SERPIENTE DESDE: ",casillaActual.getIndice()+1, " HASTA: ",casillaFinal.getIndice()+1)
                        distancia = (posTablero - (casillaFinal.getIndice())) * (-1)
                        coordenadasNuevas = casillaFinal.getCoordenadas()
                    else:
                        print("BAJE POR SERPIENTE DESDE: ",casillaActual.getIndice()+1, " HASTA: ",casillaFinal.getIndice()+1)
                        distancia = (posTablero - (casillaFinal.getIndice())) * (-1)
                        coordenadasNuevas = casillaFinal.getCoordenadas()
                else:                                                         #entra si es escalera
                    if isinstance(casillaFinal, CasillaEstandar):
                        print("SUBI POR ESCALERA DESDE: ",casillaActual.getIndice()+1, " HASTA: ",casillaFinal.getIndice()+1)
                        distancia = ((casillaFinal.getIndice())- posTablero)
                        coordenadasNuevas = casillaFinal.getCoordenadas()
                    else:
                        print("SUBI POR ESCALERA DESDE: ",casillaActual.getIndice()+1, " HASTA: ",casillaFinal.getIndice()+1)
                        distancia = ((casillaFinal.getIndice())- posTablero)
                        coordenadasNuevas = casillaFinal.getCoordenadas()
                        
        return distancia,coordenadasNuevas
    """
    Este metodo agrega un Jugador a la lista de jugadores que tiene el Singleton, la cual es informacion importante para las demas clases
    @param jugador: recibe una instancia de un Jugador para agregarlo a la lista
    @type jugador: instancia de la clase jugador
    """
    
    @classmethod
    def reporte_jugadores(cls, jugador):
        Singleton.agregar_jugador(jugador)
    """
    Este metodo se utiliza para decidir el orden de los turnos de los jugadores, cada uno lanza dados y el mas alto, va de primero y asi sucesivamente
    @param cantidad_jugadores: recibe la cantidad de jugadores que estan en la partida
    @type cantidad_jugadores: numero entero
    @param boton_dados: recibe una instancia de un boton de dados del cual se sacara la informacion de los dados
    @type boton_dados: instancia de la clase button
    @param dado: el dado que se lanzara para sacar un numero al azar
    @type dado: una instancia de dado
    """
    @classmethod
    def decidir_turnos(cls, cantidad_jugadores, boton_dados, dado):
        jugadores = []
        resultados = []
        for i in range(cantidad_jugadores):
            print("Tire los dados el Jugador ", i+1)
            resultado_dados = dado.espere_repuesta_dados(boton_dados)
            resultados.append(resultado_dados)
            jugadores.append( (Singleton.jugadores[i], resultado_dados) )
        resultados.sort(reverse=True)
        for i in range (len(resultados)):
            jugador = cls.buscar_jugador(jugadores, resultados[i])
            Singleton.jugadores_ordenados.append(jugador[0])
            jugadores.remove(jugador)

    """
    Este metodo busca un jugador dentro del vector de turnos de acuerdo al valor que saco en los dados
    @param jugadores: el vector que guarda los turnos de los jugadores
    @type jugadores: un array de Jugador
    @param valor: la cantidad que tiro en los dados el jugador
    @type valor: numero entero
    """
    @classmethod
    def buscar_jugador(cls, jugadores, valor):
        for jugador in jugadores:
            if jugador[1] == valor:
                return jugador

    @classmethod
    def esColorRepetido(cls, color):     
        """
        Va a buscar si el color, ya acordado por el usuario, le pertenece a otro jugador y retorna true si es asi.
        Si por el otro lado, no esta repetido, entonces retorna false.
        :param color: color a buscar dentro de los colores de jugadores
        :type color: string
        :returns: True si un jugador ya tiene ese color, False si nadie lo ha solicitado antes y no le pertenece a alguien.
        """
        if color in Singleton.colores_jugadores_usados:
            return True
        else:
            return False
    
    @classmethod
    def existeColor(cls, color):
        """
        Va a buscar dentro de los colores existentes, si el color escogido por el usuario existe, y va a 
        retornar True si si exsite y False si no.
        :param color: Color escogido por el usuario que se va a buscar si existe
        :type color: string
        :returns: retorna True si encuentra el color dentro de los existentes, False si no.
        """
        for llave in Singleton.colores_jugadores:
            if llave == color:
                return True
        return False

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