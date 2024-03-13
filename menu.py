import pygame
from buttons import *
import socket
from client import clientGame
from server import serverGame

def menu(screen):
    #init variables
    inMenu = True
    mainMenu = True
    joinGameMenu = True
    textInput = ""
    
    #create menu buttons

    createGameButton = menuButton("red", "CREATE GAME", [screen.get_width()/2, 150])
    joinGameButton = menuButton("orange", "JOIN GAME", [screen.get_width()/2, 350])
    controlsButton = menuButton("green", "VIEW CONTROLS", [screen.get_width()/2, 550])
    enterTextButton = menuButton("orange", textInput, [screen.get_width()/2, screen.get_height()/2])
    ipText = menuButton("black", "ENTER HOST ADDRESS", [screen.get_width()/2, 200])
    hostNameText = menuButton("black", "HOSTNAME: " +str(socket.gethostname()), [screen.get_width()/2, 50])

    buttonGroup = pygame.sprite.Group()
    buttonGroup.add(createGameButton)
    buttonGroup.add(joinGameButton)
    buttonGroup.add(controlsButton)
    buttonGroup.add(hostNameText)
    
    while inMenu:
        if mainMenu:
            screen.fill("black")
            for event in pygame.event.get():
                #clicking buttons
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    if joinGameButton.getRect().collidepoint(mousePos):
                        mainMenu = False
                        joinGameMenu = True

                        #replace buttons
                        buttonGroup.empty()
                        buttonGroup.add(enterTextButton)
                        buttonGroup.add(ipText)

                    elif createGameButton.getRect().collidepoint(mousePos):
                        createGameButton.setText("ANY KEY TO CANCEL")
                        buttonGroup.update()
                        buttonGroup.draw(screen)
                        pygame.display.flip()
                        serverGame()
                        #if cancelled
                        createGameButton.setText("CREATE GAME")
                        
                if event.type == pygame.QUIT:
                    inMenu = False
                    running = False
                    
        if joinGameMenu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    inMenu = False
                    joinGameMenu = False
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        textInput = textInput[:-1]
                    elif event.key == pygame.K_RETURN:
                        clientGame(textInput)
                    else:
                        textInput += event.unicode

                    enterTextButton.setText(textInput)
                    
        buttonGroup.update()
        buttonGroup.draw(screen)
        pygame.display.flip()

    buttonGroup.empty()
