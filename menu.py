#module for main menu

import pygame
import mapfuncs
from buttons import *
import socket
from client import *
from server import *
import pickle

def menu(screen):
    #init variables
    inMenu = True
    mainMenu = True
    joinGameMenu = False
    controlsMenu = False
    textInput = ""
    controls = [pygame.K_a, pygame.K_d]
    
    #menu buttons
    #main menu
    createGameButton = menuButton("red", "CREATE GAME", [screen.get_width()/2, 150])
    joinGameButton = menuButton("orange", "JOIN GAME", [screen.get_width()/2, 350])
    controlsButton = menuButton("green", "VIEW CONTROLS", [screen.get_width()/2, 550])
    #hostNameText = menuButton("black", "HOSTNAME: " +str(socket.gethostname()), [screen.get_width()/2, 50])

    #join menu
    enterTextButton = menuButton("orange", textInput, [screen.get_width()/2, screen.get_height()/2])
    ipText = menuButton("black", "ENTER HOST ADDRESS", [screen.get_width()/2, 200])

    #controls menu
    adButton = menuButton("green", "A/D KEYS", [screen.get_width()/2, 250])
    lrButton = menuButton("red", "LEFT/RIGHT ARROWS", [screen.get_width()/2, 450])

    #other
    returnButton = menuButton("gray", "RETURN", [210,50])
    
    buttonGroup = pygame.sprite.Group()
    buttonGroup.add(createGameButton, joinGameButton, controlsButton)

    #subgroups for menus
    mainGroup = pygame.sprite.Group()
    mainGroup.add(createGameButton, joinGameButton, controlsButton)

    joinGroup = pygame.sprite.Group()
    joinGroup.add(enterTextButton, ipText, returnButton)

    controlsGroup = pygame.sprite.Group()
    controlsGroup.add(adButton, lrButton, returnButton)
    
    while inMenu:                 
        if mainMenu:
            screen.fill("black")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    inMenu = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    if joinGameButton.getRect().collidepoint(mousePos):
                        mainMenu = False
                        joinGameMenu = True

                        buttonGroup.empty()
                        buttonGroup.add(joinGroup)

                    elif createGameButton.getRect().collidepoint(mousePos):
                        createGameButton.setText("ANY KEY TO CANCEL")
                        buttonGroup.update()
                        buttonGroup.draw(screen)
                        pygame.display.flip()
                        serverGame(controls)
                        #if cancelled
                        createGameButton.setText("CREATE GAME")

                    elif controlsButton.getRect().collidepoint(mousePos):
                        mainMenu = False
                        controlsMenu = True

                        buttonGroup.empty()
                        buttonGroup.add(controlsGroup)

                    
        if joinGameMenu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    inMenu = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    if returnButton.getRect().collidepoint(mousePos):
                        textInput = ""
                        enterTextButton.setText(textInput)
                        mainMenu = True
                        joinGameMenu = False
                        
                        buttonGroup.empty()
                        buttonGroup.add(mainGroup)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        textInput = textInput[:-1]
                    elif event.key == pygame.K_RETURN:
                        clientGame(textInput, controls)
                        screen.fill("black")
                    else:
                        textInput += event.unicode

                    enterTextButton.setText(textInput)

        if controlsMenu:
            if event.type == pygame.QUIT:
                    inMenu = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #player chooses a and d keys
                    mousePos = pygame.mouse.get_pos()
                    if adButton.getRect().collidepoint(mousePos):
                        adButton.setColour("green")
                        lrButton.setColour("red")
                        controls = [pygame.K_a, pygame.K_d]

                    #player chooses left and right arrow keys
                    elif lrButton.getRect().collidepoint(mousePos):
                        adButton.setColour("red")
                        lrButton.setColour("green")
                        controls = [pygame.K_LEFT, pygame.K_RIGHT]

                if returnButton.getRect().collidepoint(mousePos):
                    mainMenu = True
                    joinGameMenu = False
                    controlsMenu = False
                    buttonGroup.empty()
                    buttonGroup.add(mainGroup)
                    
        buttonGroup.update()
        buttonGroup.draw(screen)
        pygame.display.flip()

    buttonGroup.empty()
    pygame.quit()
