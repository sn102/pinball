#used to start program

import math
import mapfuncs
from endScreen import endScreen
from menu import *
import pygame
import mapfuncs
from buttons import *
import socket
from client import *
from server import *
from obstacle import obstacle
from flipper import *
from ball import *
import pickle

screen = pygame.display.set_mode((1280, 720))

#open menu
menu(screen)
