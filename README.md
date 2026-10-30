# Escaleras y Serpientes

[English](README.en.md) | **Español**

Implementación del clásico juego de mesa Escaleras y Serpientes en Python, con interfaz gráfica en **pygame** (tablero) y **tkinter** (menús y ventanas de diálogo). El proyecto fue desarrollado como trabajo final aplicando un MARDA; la justificación de los patrones y principios de diseño utilizados está en [Documentacion/justificaciónMARDA.pdf](Documentacion/justificaci%C3%B3nMARDA.pdf).

## Autores

- Josue Amador            B80435
- Daniel Salazar          B87214
- Ricardo Franco          B83050
- Ignacio Arroyo          B80766
- Gustavo Jimenez         B84060

## Requerimientos

- Python 3 (probado con Python 3.12)
- pygame 2 (probado con pygame 2.6)
- tkinter (en Windows y macOS viene incluido con el instalador oficial de Python)

### Instalación en Linux

```bash
sudo apt install python3-tk python3-venv
python3 -m venv .venv
source .venv/bin/activate
pip install pygame
```

Para corroborar que se tiene tkinter: `python3 -m tkinter` (debe abrirse una pequeña ventana de prueba).

### Instalación en Windows

```bash
py -m venv .venv
.venv\Scripts\activate
pip install pygame
```

Para corroborar que se tiene tkinter: `python -m tkinter`

## Cómo correr el programa

El programa debe ejecutarse **desde el directorio principal** `Escaleras_y_Serpientes`, ya que carga las imágenes desde `imagenes/` y las partidas desde `Guardado/` usando rutas relativas.

En Linux:
```bash
python3 source/controlador.py
```
En Windows:
```bash
python source/controlador.py
```

## Cómo jugar

Al iniciar el programa se abre un menú con dos opciones: **Empezar partida** y **Cargar partida**.

### Empezar partida

1. Se solicita la cantidad de jugadores (entre 2 y 4). Si el valor es inválido, se vuelve a solicitar indicando el error.
2. Se genera un tablero de 10x10 casillas con serpientes y escaleras ubicadas al azar (cada una entre el 5% y el 7% del total de casillas).
3. A cada jugador se le asigna un color de ficha al azar, sin repetirse.
4. Para decidir el orden de juego, cada jugador lanza los dados una vez; quien saque el mayor número empieza, y así sucesivamente.

### Durante la partida

- Los dados se lanzan con el botón **Lanzar dados** o con la tecla **espacio**. Se lanzan dos dados de seis caras y la ficha avanza la suma de ambos inmediatamente.
- Si la ficha cae en la cabeza de una serpiente, baja hasta su cola; si cae en la base de una escalera, sube hasta su final. La barra lateral indica desde y hasta qué casilla se movió.
- Si el lanzamiento se pasa de la casilla 100, la ficha da la vuelta y continúa contando desde el inicio del tablero.
- Gana el primer jugador que caiga exactamente en la casilla 100. El nombre del ganador se muestra durante 4 segundos y luego el juego se cierra.
- El botón **Mostrar reglas** abre una ventana con las reglas del juego.
- El botón **Guardar partida** pide un nombre y guarda el estado actual en `Guardado/<nombre>.txt`.

### Cargar partida

Se escribe el nombre de la partida guardada, **sin** la extensión `.txt` (por ejemplo, `test` para cargar `Guardado/test.txt`). Si el archivo no existe o está vacío, se vuelve a pedir el nombre. Si el archivo tiene menos de 7 líneas, se considera corrupto y el programa lanza una excepción para evitar crear una partida con datos incorrectos.

Los archivos de guardado se almacenan en la carpeta `Guardado/` con el siguiente formato:

```text
Cantidad de jugadores
Nombre del jugador / posición en el tablero / color del jugador / desplazamiento dentro de la casilla en X / desplazamiento dentro de la casilla en Y
... hasta la cantidad de jugadores (en orden de turno) ...
Cantidad de serpientes
Casilla de inicio (cabeza) de la serpiente 1 / casilla final (cola) de la serpiente 1
... hasta la cantidad de serpientes ...
Cantidad de escaleras
Casilla de inicio (base) de la escalera 1 / casilla final de la escalera 1
... hasta la cantidad de escaleras ...
```

Las posiciones del tablero van de 0 a 99, y los colores válidos son: `magenta`, `azul`, `gris`, `naranja`, `negro`, `verde`, `aqua`, `dorado` y `rojo`. El archivo `Guardado/test.txt` es un ejemplo de partida válida.

## Estructura del proyecto

```text
source/          Código fuente del juego y fuentes de la documentación Sphinx
  controlador.py   Punto de entrada: menú principal, ciclo del juego y manejo de eventos
  vista.py         Interfaz gráfica: barra lateral, botones, reglas y guardado
  arbitro.py       Reglas: orden de turnos, serpientes, escaleras y condición de gane
  tablero.py       Tablero lógico y gráfico (coloreado y dibujo de casillas)
  fabrica.py       Fábrica que genera las casillas, serpientes y escaleras al azar
  casilla.py       Tipos de casilla: estándar, de serpiente y de escalera
  conector.py      Serpientes y escaleras, y su dibujo en el tablero
  jugador.py       Jugador lógico y su representación gráfica
  inventario.py    Inventario del jugador (su ficha)
  dado.py          Lanzamiento y dibujo de los dos dados
  singleton.py     Estado global compartido del juego
  almacenador.py   Guardado de partidas en .txt
  cargador.py      Carga de partidas desde .txt
  button.py, sidebar.py, elementoTablero.py   Componentes auxiliares
imagenes/        Caras de los dados e imágenes del menú
Guardado/        Partidas guardadas
Documentacion/   Diagrama de clases (PNG y XMI) y justificación del MARDA (PDF)
build/           Documentación externa generada con Sphinx (HTML y LaTeX)
```

## Documentación externa

En la carpeta `build/` se encuentra la documentación externa en formato HTML (`build/html/index.html`) y LaTeX, generada con Sphinx a partir de los docstrings del código. Para regenerarla se necesita tener Sphinx instalado (`pip install sphinx`) y ejecutar desde el directorio principal:

```bash
make html
```
