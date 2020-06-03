from singleton import Singleton
from tablero import Tablero
from casilla import Casilla, CasillaEstandar, CasillaEscalera, CasillaSerpiente


class Arbitro():

    @classmethod
    def init(cls):
        pass

    @classmethod
    def comprobarGane(cls,pos):#comprueba si el jugador esta en la posicion ganadora y devuelve un bool
        gano = False             #si las coordenadas de jugador son iguales a las de la casilla ganadora, gana = True
        if pos == Singleton.pos_ganadora:
            print(Singleton.pos_ganadora)
            gano = True
        return gano


    @classmethod
    def aplicarReglasMovimiento(cls, posTablero):             #comprueba si el jugador esta en una escalera o serpiente y lo mueve a donde le corresponde
        casillaActual = Singleton.casillasTablero[posTablero]
        distancia = 0
        coordenadasNuevas = []
        if not isinstance(casillaActual,CasillaEstandar):         #entra a la condicion si es serpiente o escalera
            if casillaActual.casilla.esInicio():
                casillaFinal = casillaActual.casilla.getFinal()
                if isinstance(casillaActual, CasillaSerpiente):             #entra si la casilla actual es serpiente
                    if isinstance(casillaFinal, CasillaEstandar):
                        print("BAJE POR SERPIENTE DESDE: ",casillaActual.casilla.getIndice()+1, " HASTA: ",casillaFinal.getIndice()+1)
                        distancia = (posTablero - (casillaFinal.getIndice())) * (-1)
                        coordenadasNuevas = casillaFinal.getCoordenadas()
                    else:
                        print("BAJE POR SERPIENTE DESDE: ",casillaActual.casilla.getIndice()+1, " HASTA: ",casillaFinal.casilla.getIndice()+1)
                        distancia = (posTablero - (casillaFinal.casilla.getIndice())) * (-1)
                        coordenadasNuevas = casillaFinal.casilla.getCoordenadas()
                else:                                                         #entra si es escalera
                    if isinstance(casillaFinal, CasillaEstandar):
                        print("SUBI POR ESCALERA DESDE: ",casillaActual.casilla.getIndice()+1, " HASTA: ",casillaFinal.getIndice()+1)
                        distancia = ((casillaFinal.getIndice())- posTablero)
                        coordenadasNuevas = casillaFinal.getCoordenadas()
                    else:
                        print("SUBI POR ESCALERA DESDE: ",casillaActual.casilla.getIndice()+1, " HASTA: ",casillaFinal.casilla.getIndice()+1)
                        distancia = ((casillaFinal.casilla.getIndice())- posTablero)
                        coordenadasNuevas = casillaFinal.casilla.getCoordenadas()
                        
        return distancia,coordenadasNuevas

    @classmethod
    def reporte_jugadores(cls, jugador):
        Singleton.agregar_jugador(jugador)
    
    @classmethod
    def decidir_turnos(cls, cantidad_jugadores, boton_dados, dado):
        jugadores = []
        resultados = []
        for i in range(cantidad_jugadores):
            print("Tire los dados el Jugador ", i+1)
            resultado_dados = dado.espere_repuesta_dados(boton_dados, dado)
            resultados.append(resultado_dados)
            jugadores.append( (Singleton.jugadores[i], resultado_dados) )
        resultados.sort(reverse=True)
        for i in range (len(resultados)):
            jugador = cls.buscar_jugador(jugadores, resultados[i])
            Singleton.jugadores_ordenados.append(jugador[0])
            jugadores.remove(jugador)

    @classmethod
    def buscar_jugador(cls, jugadores, valor):
        for jugador in jugadores:
            if jugador[1] == valor:
                return jugador
