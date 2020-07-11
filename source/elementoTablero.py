import os
import time
import random
import itertools
import sys, pygame
from pygame.locals import *
from abc import ABC, abstractmethod

class ElementoTablero(ABC):
    
    def __init__(self):
        super().__init__()