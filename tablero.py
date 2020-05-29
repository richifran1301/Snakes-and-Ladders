import os
import time
import random
import itertools
import sys, pygame
from pygame.locals import *
from button import Button
from sidebar import Sidebar
from conector import Conector, ConectorEstandar, Escalera, Serpiente
from casilla import Casilla, CasillaEstandar, CasillaEscalera, CasillaSerpiente
from dado import Dado

class Tablero():
    def __init__(self, tamanio, ventana, ancho_barra):
        self.tamanio = tamanio # x * y = z
        self.ventana = ventana
        self.casillas = []
        self.serpientes = []
        self.escaleras = []
        self.generarCasillas()
        self.ancho_barra = ancho_barra

    def generarCasillas(self):
        
        alto, ancho = 700, 700 # del tablero
        
        cantidad_serpientes = int((self.tamanio[0] * self.tamanio[1]) * ((random.randint(5, 7)) * 0.01))
        cantidad_escaleras = int((self.tamanio[0] * self.tamanio[1]) * ((random.randint(5, 7)) * 0.01))

        centros_casillas = self.obtener_centro_casillas(alto, ancho)
        
        posiciones_serpientes, posiciones_escaleras = self.generar_conexiones(centros_casillas, cantidad_serpientes, cantidad_escaleras)

        for i in range(len(centros_casillas)):
            encontrado = False
            for j in range(len(posiciones_serpientes)):
                if not encontrado and i in posiciones_serpientes[j]:
                    figura = pygame.Rect(centros_casillas[i][0] - int((alto//self.tamanio[0])//2), centros_casillas[i][1] - int((ancho//self.tamanio[1])/2), alto//self.tamanio[0], ancho//self.tamanio[1])
                    temp = CasillaEstandar(centros_casillas[i], (255,255,255), figura, i, self.ventana)
                    serpiente = CasillaSerpiente(temp)
                    self.casillas.append(serpiente)
                    encontrado = True
                if encontrado:
                    break

            for k in range(len(posiciones_escaleras)):
                if not encontrado and i in posiciones_escaleras[k]:
                    figura = pygame.Rect(centros_casillas[i][0] - int((alto//self.tamanio[0])//2), centros_casillas[i][1] - int((ancho//self.tamanio[1])/2), alto//self.tamanio[0], ancho//self.tamanio[1])
                    temp = CasillaEstandar(centros_casillas[i], (255,255,255), figura, i, self.ventana)
                    escalera = CasillaEscalera(temp)
                    self.casillas.append(escalera)
                    encontrado = True
                if encontrado:
                    break

            if not encontrado:
                figura = pygame.Rect(centros_casillas[i][0] - int((alto//self.tamanio[0])//2), centros_casillas[i][1] - int((ancho//self.tamanio[1])//2), alto//self.tamanio[0], ancho//self.tamanio[1])
                casillaEstandar = CasillaEstandar(centros_casillas[i], (255,255,255), figura, i, self.ventana)
                self.casillas.append(casillaEstandar)

        for i in range(len(self.casillas)):
            if isinstance(self.casillas[i], CasillaSerpiente):
                if not self.existeConexion(self.casillas[i].casilla.getIndice()):
                    conector = ConectorEstandar(self.getPar(self.casillas[i].casilla.getIndice(), posiciones_serpientes), self.ventana)
                    self.serpientes.append(Serpiente(conector))
                    self.serpientes[len(self.serpientes) - 1].conector.sendConector()

            elif isinstance(self.casillas[i], CasillaEscalera):
                if not self.existeConexion(self.casillas[i].casilla.getIndice()):
                    conector = ConectorEstandar(self.getPar(self.casillas[i].casilla.getIndice(), posiciones_escaleras), self.ventana)
                    self.escaleras.append(Escalera(conector))
                    self.escaleras[len(self.escaleras) - 1].conector.sendConector()

        #for i in range(len(self.casillas)):
            #if not isinstance(self.casillas[i], CasillaEstandar):
                #print(self.casillas[i].casilla.getIndice() + 1, self.casillas[i].casilla.getFinal() + 1, self.casillas[i].casilla.esInicio())
                
    def getPosicionesEnTupla(self, indice, posiciones):
        #print("Indice: ", indice, "\n", "Posiciones: ", posiciones)
        for i in posiciones:
            if indice in i:
                #print("i = ", i)
                return i
        return

    def getPar(self, indice, posiciones):
        temp_par = self.getPosicionesEnTupla(indice, posiciones)

        tupla = (self.casillas[temp_par[0]], self.casillas[temp_par[1]])

        return tupla

    def existeConexion(self, indice):

        for i in range(len(self.serpientes)):
            if indice == self.serpientes[i].conector.getCasillaInicio().casilla.getIndice() or indice == self.serpientes[i].conector.getCasillaFinal().casilla.getIndice():
                return True

        for i in range(len(self.escaleras)):
            if indice == self.escaleras[i].conector.getCasillaInicio().casilla.getIndice() or indice == self.escaleras[i].conector.getCasillaFinal().casilla.getIndice():
                return True

        return False

    def generar_serpientes(self, escaleras, casillas, cantidad):
        serpientes_temp = []
        generados = 0
        while generados < cantidad * 2: #Son cantidad serpientes generadas en tuplas de 2
            while True:
                valor = random.randint(1, len(casillas) - 2)
                if (valor not in escaleras) and (valor not in serpientes_temp):
                    serpientes_temp.append(valor)
                    break
            generados += 1
        
        return serpientes_temp

    def generar_escaleras(self, casillas, cantidad):
        escaleras_temp = []
        generados = 0

        while generados < cantidad * 2: #Son cantidad escaleras generadas en tuplas de 2
            while True:
                valor = random.randint(1, len(casillas) - 2)
                if valor not in escaleras_temp:
                    escaleras_temp.append(valor)
                    break
            generados += 1

        return escaleras_temp

    def generar_conexiones(self, casillas, cantidad_serpientes, cantidad_escaleras):

        escaleras_temp = self.generar_escaleras(casillas, cantidad_escaleras)
        serpientes_temp = self.generar_serpientes(escaleras_temp, casillas, cantidad_serpientes)

        escaleras = []
        serpientes = []

        for i in range(0, len(escaleras_temp), 2):

            valorInicial = 0
            valorFinal = 0

            if escaleras_temp[i] < escaleras_temp[i+1]:
                valorInicial = escaleras_temp[i]
                valorFinal = escaleras_temp[i+1]
            else:
                valorInicial = escaleras_temp[i+1]
                valorFinal = escaleras_temp[i]

            tupla = (valorInicial, valorFinal)
            escaleras.append(tupla)

        for i in range(0, len(serpientes_temp), 2):

            valorInicial = 0
            valorFinal = 0

            if serpientes_temp[i] > serpientes_temp[i+1]:
                valorInicial = serpientes_temp[i]
                valorFinal = serpientes_temp[i+1]
            else:
                valorInicial = serpientes_temp[i+1]
                valorFinal = serpientes_temp[i]

            tupla = (valorInicial, valorFinal)
            serpientes.append(tupla)

        #print("Escaleras: ", escaleras)
        #print("Serpientes: ", serpientes)

        return serpientes, escaleras

    def obtener_orden_coordenadas(self, centro_casillas_x, centro_casillas_y):

        casillas_temp = []
        temp = centro_casillas_x

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
        centro_casillas = []    
        for i in range(max_iteracion):
            centro_casillas.append(int(x/2) + (i*x))
        return centro_casillas

    def obtener_centro_casillas(self, ancho_total, alto_total):
    
        centro_casillas = []
        centro_casillas_x = []
        centro_casillas_y = []

        cantidad_casillas_x, cantidad_casillas_y = self.tamanio[0], self.tamanio[1]
        ancho_casilla = int(ancho_total/cantidad_casillas_x)
        altura_casilla = int(alto_total/cantidad_casillas_y)
    
        centro_casillas_x = self.obtener_casillas(ancho_casilla, cantidad_casillas_x)
        centro_casillas_y = self.obtener_casillas(altura_casilla, cantidad_casillas_y)
    
        centro_casillas_y.reverse()
    
        centro_casillas = self.obtener_orden_coordenadas(centro_casillas_x, centro_casillas_y)
    
        return centro_casillas

    def colorearCasillas(self):
        colores_x = ["amarillo", "blanco", "rojo", "azul", "verde"]

        i = 0
        indice_color_x = 0
        indice_color_y = 0
        par_actual, par_final = 0, self.tamanio[0]
        impar_actual, impar_final = self.tamanio[0] * 2 - 1, self.tamanio[0] - 1

        while i < self.tamanio[1] // 2: 
            #Coloreado filas pares
            for j in range (par_actual, par_final):
                if isinstance(self.casillas[j], CasillaEstandar):
                    self.casillas[j].setColor(colores_x[indice_color_x])
                else:
                    self.casillas[j].casilla.setColor(colores_x[indice_color_x])
                
                indice_color_x += 1
                if indice_color_x > 4:
                    indice_color_x = 0

            #Coloreado filas impares
            for j in range (impar_actual, impar_final, -1):
                if isinstance(self.casillas[j], CasillaEstandar):
                    self.casillas[j].setColor(colores_x[(indice_color_x + 3) % 5])
                else:
                    self.casillas[j].casilla.setColor(colores_x[(indice_color_x + 3) % 5])
                
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

        for c in self.casillas:
            if isinstance(c, CasillaSerpiente) or isinstance(c, CasillaEscalera):
                c.casilla.dibujar()
            else:
                c.dibujar()

        """
        casilla_previa = None
        for casilla_actual in self.casillas:
            if casilla_previa:
                if (isinstance(casilla_previa, CasillaEscalera) or isinstance(casilla_previa, CasillaSerpiente)) and (isinstance(casilla_actual, CasillaEstandar)):
                    pygame.draw.line(self.ventana, (0,0,0), casilla_previa.casilla.getCoordenadas(), casilla_actual.getCoordenadas(), 4)

                elif (isinstance(casilla_previa, CasillaEstandar)) and (isinstance(casilla_actual, CasillaSerpiente) or isinstance(casilla_actual, CasillaEscalera)):
                    pygame.draw.line(self.ventana, (0,0,0), casilla_previa.getCoordenadas(), casilla_actual.casilla.getCoordenadas(), 4)

                elif isinstance(casilla_previa, CasillaEstandar) and isinstance(casilla_actual, CasillaEstandar):
                    pygame.draw.line(self.ventana, (0,0,0), casilla_previa.getCoordenadas(), casilla_actual.getCoordenadas(), 4)

                elif (isinstance(casilla_previa, CasillaEscalera) or isinstance(casilla_previa, CasillaSerpiente)) and (isinstance(casilla_actual, CasillaSerpiente) or isinstance(casilla_actual, CasillaEscalera)):
                    pygame.draw.line(self.ventana, (0,0,0), casilla_previa.casilla.getCoordenadas(), casilla_actual.casilla.getCoordenadas(), 4)

            casilla_previa = casilla_actual
        """

        for i in self.serpientes:
            i.dibujar()
        
        for i in self.escaleras:
            i.dibujar()

def main():

    ancho_barra = 250

    ancho, alto = 700 + ancho_barra, 700

    pygame.init()
    pygame.display.set_caption("Serpientes y escaleras")
    #ruta_local = os.path.dirname(__file__)
    #ruta_icono = os.path.join(ruta_local, "000.jpg")
    #icono = pygame.image.load(ruta_icono)
    #pygame.display.set_icon(icono)

    #Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>

    os.environ['SDL_VIDEO_CENTERED'] = '1'
    ventana = pygame.display.set_mode((ancho, alto))
    #ventana.fill((0,0,0))

    cantidad_x, cantidad_y = 10, 10

    assert (ancho - ancho_barra) % cantidad_x == 0 and alto % cantidad_y == 0

    t = Tablero((cantidad_x, cantidad_y), ventana, ancho_barra)
    t.colorearCasillas()
    t.dibujarCasillas()

    boton_dados = Button(ventana, (255,255,255), 750, 35, 150, 40, "Lanzar dados")
    dado = Dado(ventana)
    elementos_sidebar = [boton_dados, dado]
    sidebar = Sidebar(ventana, 700, 700, 250, (255,255,255), elementos_sidebar)

    while True:
        boton_dados.dibujar()
        pygame.display.update()
        resultado_dados = 0
        for events in pygame.event.get():
            posicion_cursor = pygame.mouse.get_pos()
            if events.type == QUIT:
                pygame.quit()
                sys.exit(0)
            elif events.type == pygame.MOUSEBUTTONDOWN:
                if boton_dados.isOver(posicion_cursor):
                    resultado_dados = dado.lanzar()     # esta variable contiene ahora el numero que lanzaron los dados. usar donde se necesite.
            elif events.type == pygame.MOUSEMOTION:
                if boton_dados.isOver(posicion_cursor):
                    boton_dados.mi_color = (161,222,147)
                else:
                    boton_dados.mi_color = (54,57,63)
                

main() 