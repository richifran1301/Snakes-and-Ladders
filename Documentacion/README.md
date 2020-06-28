# Escaleras_y_Serpientes

## Autores:

- Josue Amador            B80435
- Daniel Salazar          B87214
- Ricardo Franco          B83050
- Ignacio Arroyo          B80766
- Gustavo Jimenez         B84060

## Requerimientos

Para el funcionamiento correcto del programa se requiere tener instalado python 3, al igual que las bibliotecas de pygame y tkinter (en el caso de Windows ya viene instalado con python). Para poder descargar estas bibliotecas se pueden ejecutar los siguientes comandos:

En Linux:
```bash
sudo apt install python3-setuptools
sudo easy_install3 pip
python3 -m pip install --user pygame

apt-get install python-tk
```
En Windows:
```bash
pip install wheel
pip install pygame‑1.9.2a0‑cp34‑none‑win_AMD64.whl

Para corroborar que se tiene tkinter: python -m Tkinter t
```
## Comandos para correr el programa:

El programa funciona tanto en Windows como en Linux, y el comando para correr el programa en Linux es 
```bash
python3 controlador.py
```
Si se desea correr en Windows, se usa con el comando
```bash
python controlador.py
```

## Instrucciones para empezar a jugar

Cuando se inicia el programa, se va abrir un menú con las siguientes opciones:
```bash
Cargar partida
Empezar partida
```
Si se escoge **cargar partida**:
- Se tiene que escribir el nombre del archivo de texto de la partida guardada. No se aceptan archivos de texto vacios o inexistentes. Si el archivo tiene menos líneas de texto del tamaño mínimo, que es 7, se considera corrupto y el programa tira excepción para evitar cear una partida con datos incorrectos. 

Los archivos de texto que funcionan como guardados, se almacenan en la carpeta ***Guardados*** y tienen este formato:
```bash
Cantidad de jugadores
Nombre del jugador / posicion en el tablero / color del jugador / posicion dentro de una casilla en X / posicion dentro de una casilla en X
---Hasta la cantidad de jugadores...
Cantidad de serpientes
Posicion en el tablero de la casilla de inicio de serpiente 1 / posicion en el tablero de la casilla final de serpiente 1
... Hasta la cantidada de serpientes ...
Cantidad de escaleras
Posicion en el tablero de la casilla de inicio de escalera 1 / posicion en el tablero de la casilla final de escalera 1
... Hasta la cantidada de escaleras ...
```
Si se escoge **empezar partida**:
El programa va a solicitarle al usuario que se digite el numero de jugadores que van a estar en la partida y los colores para sus fichas. Si estos datos no se ingresan, el juego no va a iniciar. Solo se pueden entre 2 a 4 jugadores en la partida y no se pueden repetir colores. Cualquier ingreso inválido o que no cumpla los requisitos recíen mencionados, ocasionará que el programa le solicite la información denuevo e incluso mencionará su error.
