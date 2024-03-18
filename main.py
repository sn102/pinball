import math
import pygame
import time
from obstacle import obstacle
from flipper import flipper
from ball import ball
import mapfuncs
from buttons import menuButton
from endScreen import endScreen
from menu import *

# pygame setup
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("arialblack", 30)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

#init variables
dt = 0
unpressed = True
unpressed2 = True
debugList = []
lineCount = 0
endTimer = 60
endText = ""
inMenu = True
mainMenu = True
joinGameMenu = False

#constants
GRAVITY = pygame.Vector2(0, 2000)
FLIPTIME = 0.2
FLIPSPEED = 0.75 * math.pi

#open menu
menu(screen)


