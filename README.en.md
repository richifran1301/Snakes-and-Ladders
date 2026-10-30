# Escaleras y Serpientes (Snakes and Ladders)

**English** | [Español](README.md)

A Python implementation of the classic Snakes and Ladders board game, with a graphical interface built on **pygame** (the board) and **tkinter** (menus and dialog windows). The project was developed as a final course assignment applying a MARDA (a design rationale document); the justification for the design patterns and principles used is in [Documentacion/justificaciónMARDA.pdf](Documentacion/justificaci%C3%B3nMARDA.pdf) (in Spanish).

The game's interface and the source code are in Spanish. The UI terms used in this README are given in Spanish with an English translation.

## Authors

- Josue Amador            B80435
- Daniel Salazar          B87214
- Ricardo Franco          B83050
- Ignacio Arroyo          B80766
- Gustavo Jimenez         B84060

## Requirements

- Python 3 (tested with Python 3.12)
- pygame 2 (tested with pygame 2.6)
- tkinter (included with the official Python installer on Windows and macOS)

### Installing on Linux

```bash
sudo apt install python3-tk python3-venv
python3 -m venv .venv
source .venv/bin/activate
pip install pygame
```

To check that tkinter is available: `python3 -m tkinter` (a small test window should open).

### Installing on Windows

```bash
py -m venv .venv
.venv\Scripts\activate
pip install pygame
```

To check that tkinter is available: `python -m tkinter`

## Running the game

The game must be run **from the project's root directory** `Escaleras_y_Serpientes`, because it loads images from `imagenes/` and saved games from `Guardado/` using relative paths.

On Linux:
```bash
python3 source/controlador.py
```
On Windows:
```bash
python source/controlador.py
```

## How to play

When the game starts, a menu opens with two options: **Empezar partida** (start game) and **Cargar partida** (load game).

### Starting a new game

1. You are asked for the number of players (2 to 4). If the value is invalid, you are asked again and told what was wrong.
2. A 10x10 board is generated, with snakes and ladders placed at random (each between 5% and 7% of the total number of squares).
3. Each player is assigned a random piece color, with no repeats.
4. To decide the turn order, each player rolls the dice once; the highest roll goes first, and so on.

### During the game

- Roll the dice with the **Lanzar dados** (roll dice) button or the **space bar**. Two six-sided dice are rolled, and the piece immediately moves forward by their sum.
- Landing on a snake's head sends the piece down to its tail; landing at the bottom of a ladder sends it up to the top. The sidebar shows which square the piece moved from and to.
- If a roll goes past square 100, the piece wraps around and keeps counting from the start of the board.
- The first player to land exactly on square 100 wins. The winner's name is shown for 4 seconds, then the game closes.
- The **Mostrar reglas** (show rules) button opens a window with the game rules.
- The **Guardar partida** (save game) button asks for a name and saves the current state to `Guardado/<name>.txt`.

### Loading a saved game

Type the name of the saved game **without** the `.txt` extension (for example, `test` to load `Guardado/test.txt`). If the file doesn't exist or is empty, you are asked for the name again. If the file has fewer than 7 lines, it is considered corrupt and the program raises an exception, rather than create a game from bad data.

Saved games are stored in the `Guardado/` folder in this format:

```text
Number of players
Player name / board position / player color / offset within the square in X / offset within the square in Y
... one line per player (in turn order) ...
Number of snakes
Start square (head) of snake 1 / end square (tail) of snake 1
... one line per snake ...
Number of ladders
Start square (bottom) of ladder 1 / end square (top) of ladder 1
... one line per ladder ...
```

Board positions range from 0 to 99. The valid colors are the Spanish names `magenta`, `azul` (blue), `gris` (gray), `naranja` (orange), `negro` (black), `verde` (green), `aqua`, `dorado` (gold) and `rojo` (red). `Guardado/test.txt` is an example of a valid saved game.

## Project structure

```text
source/          Game source code and Sphinx documentation sources
  controlador.py   Entry point: main menu, game loop and event handling
  vista.py         Graphical interface: sidebar, buttons, rules and saving
  arbitro.py       Rules: turn order, snakes, ladders and win condition
  tablero.py       Logical and graphical board (square coloring and drawing)
  fabrica.py       Factory that randomly generates squares, snakes and ladders
  casilla.py       Square types: standard, snake and ladder
  conector.py      Snakes and ladders, and how they are drawn on the board
  jugador.py       Logical player and its graphical representation
  inventario.py    Player inventory (their game piece)
  dado.py          Rolling and drawing the two dice
  singleton.py     Shared global game state
  almacenador.py   Saving games to .txt
  cargador.py      Loading games from .txt
  button.py, sidebar.py, elementoTablero.py   Helper components
imagenes/        Dice faces and menu images
Guardado/        Saved games
Documentacion/   Class diagram (PNG and XMI) and MARDA justification (PDF)
build/           External documentation generated with Sphinx (HTML and LaTeX)
```

## External documentation

The `build/` folder contains the external documentation in HTML (`build/html/index.html`) and LaTeX formats, generated with Sphinx from the code's docstrings (in Spanish). To regenerate it, install Sphinx (`pip install sphinx`) and run this from the root directory:

```bash
make html
```
