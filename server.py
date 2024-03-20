#module for server game

import pygame
import socket
import pygame
import math
import mapfuncs
from endScreen import endScreen
from buttons import *
import socket
from client import *
from server import *
from obstacle import obstacle
from flipper import flipper
from ball import ball
import pickle

def serverGame(controls):
    from obstacle import obstacle
    from flipper import flipper
    from ball import ball

    #constants
    GRAVITY = pygame.Vector2(0, 2000)
    FLIPTIME = 0.2
    FLIPSPEED = 0.75 * math.pi
    TIMERSTART = 60

    #init variables
    dt = 0
    unpressed = True
    unpressed2 = True
    debugList = []
    lineCount = 0
    endText = ""
    connecting = True
    connected = True


#-------NETWORKING START--------

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((socket.gethostname(), 5050))
    serverSocket.listen(1024)
    serverSocket.settimeout(1)

    while connecting:
        connecting = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return
        try:
            connection, address = serverSocket.accept()
        except:
            connecting = True


        
    #init variables
    fileRead = "False"
    clientReady = "False"

    while fileRead != "True":
        fileRead = connection.recv(4).decode("utf-8")
        print("connected to ", address)
        if fileRead == "True":
            running = True

#-------------------------------
         

    machine = open("map.txt", "r")
    obstacleGroup = pygame.sprite.Group()
    for line in machine:
        #check if client is ready to receive a new line
        while clientReady != "True":
            clientReady = connection.recv(4).decode("utf-8")
        clientReady = "False"
        
        connection.send(line.encode("utf-8"))
        line = line.strip()
        line = line.split(".")
        line[0] = mapfuncs.convertStringToList(line[0])
        line[1] = int(line[1])
        line[3] = int(line[3])
        line[4] = int(line[4])
        #send line to client player
        #make obstacle
        obstacleGroup.add(obstacle(line[0], line[1], line[2], line[3], line[4]))
        endTimer = TIMERSTART
    connection.send("False".encode("utf-8"))
    machine.close()


#-----GAME SETUP-----

    # pygame setup
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("arialblack", 30)
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    #create flippers
    P1FlipperL = flipper(1, [150,470], "left")
    P1FlipperR = flipper(1, [850, 600], "right")

    P2FlipperL = flipper(2, [430,600], "left")
    P2FlipperR = flipper(2, [1130,470], "right")

    obstacleGroup.add(P1FlipperL)
    obstacleGroup.add(P1FlipperR)
    obstacleGroup.add(P2FlipperL)
    obstacleGroup.add(P2FlipperR)

    flipperGroup = pygame.sprite.Group()
    flipperGroup.add(P1FlipperL)
    flipperGroup.add(P1FlipperR)
    flipperGroup.add(P2FlipperL)
    flipperGroup.add(P2FlipperR)

    #create pinballs
    player1 = ball(40, "blue", (250, 250), pygame.Vector2(0, 0), GRAVITY, 1)
    player2 = ball(40, "red", (1030, 250), pygame.Vector2(0, 0), GRAVITY, 2)
    pinballGroup = pygame.sprite.Group()
    pinballGroup.add(player1)
    pinballGroup.add(player2)

#--------------------

    endTimer = TIMERSTART
    #main game loop

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    #---------NETWORKING------------

        #receive data from client
        if connected:
            try:
                dataReceived = connection.recv(1024).decode("utf-8")
            except:
                connected = False
                endTimer = -1
                endText = "Player 2 disconnected"
        
        #send game data to client
        player1Data = [player1.getPosition(), player1.getVelocity(), player1.getScore()]
        player2Data = [player2.getPosition(), player2.getVelocity(), player2.getScore()]
        flipperData1 = [P1FlipperL.getFlipState(), P1FlipperR.getFlipState()]
        flipperData2 = [P2FlipperL.getFlipState(), P2FlipperR.getFlipState()]
        timeData = endTimer
        gameDataList = [player1Data, player2Data, flipperData1, flipperData2, endTimer]
        sentGameData = pickle.dumps(gameDataList)
        if len(dataReceived) > 0: #check if client is responsive
            if connected:
                try:
                    connection.send(sentGameData)
                except:
                    connected = False
                    endTimer = -1
                    endText = "Player 2 disconnected"

        screen.fill("white")

        #update obstacle sprites
        obstacleGroup.update()
        obstacleGroup.draw(screen)

        

        #update pinball sprites
        pinballGroup.update()
        pinballGroup.draw(screen)

        #ball physics and score
        if dt <= 0.05: #check for window dragging
            for ball in pinballGroup:
                ball.prevPosition = ball.position
                ball.setVelocity(ball.getVelocity() + (ball.getAcceleration() * dt))
                ball.setPosition(ball.getPosition() + (ball.getVelocity() * dt))
                ball.setAcceleration(pygame.Vector2(GRAVITY))

                #score
                screen.blit(ball.getTextSurf(), (0, (50 * ball.getPlayerNo())))
                    

        #if ball falls out of range
        if player1.getPosition().y > 1280 or player1.getPosition().y < 0:
            player1.setPosition((250, 250))
            player1.setVelocity(pygame.Vector2(0,0))
        if player2.getPosition().y > 1280 or player2.getPosition().y < 0:
            player2.setPosition((1080, 200))
            player2.setVelocity(pygame.Vector2(0,0))
            

        #collision
        for ball in pinballGroup:
            mapfuncs.checkCollideObstacle(ball, obstacleGroup, ball.getVelocity() * dt)
        mapfuncs.checkCollideBall(pinballGroup)
  
        #flipper controls
        keys = pygame.key.get_pressed()
        if keys[controls[0]] and P1FlipperL.getFlipState() == "":
            P1FlipperL.setFlipState("up")
            P1FlipperL.setTime(FLIPTIME)

        if keys[controls[1]] and P1FlipperR.getFlipState() == "":
            P1FlipperR.setFlipState("up")
            P1FlipperR.setTime(FLIPTIME)

        if dataReceived == "L" and P2FlipperL.getFlipState() == "":
            P2FlipperL.setFlipState("up")
            P2FlipperL.setTime(FLIPTIME)

        if dataReceived == "R" and P2FlipperR.getFlipState() == "":
            P2FlipperR.setFlipState("up")
            P2FlipperR.setTime(FLIPTIME)

        if dt <= 0.05: #check for window dragging
            for obstacle in obstacleGroup:
                obstacle.translate(obstacle.getVelocity()*dt)
                obstacle.rotate(obstacle.angularVelocity * dt)

        #flipper rotation
        for flipper in flipperGroup:
            #change flip direction depending on side
            if flipper.getFlipState != "":
                if flipper.getLeftRight() == "left":
                    multiplier = -1
                else:
                    multiplier = 1
                
                if flipper.getFlipState() == "up":
                    if flipper.getTime() > 0:
                        flipper.setAngularVelocity(multiplier * FLIPSPEED)
                        turnSpeed = flipper.getAngularVelocity()
                        flipper.rotate(turnSpeed * dt)
                        flipper.setTime(flipper.getTime() - dt)
                    else:
                        flipper.setTime(FLIPTIME)
                        flipper.setFlipState("down")

                elif flipper.getFlipState() == "down":
                    if -1 * multiplier * flipper.getAngularDisplacement() < 0:
                        flipper.setAngularVelocity(multiplier * -FLIPSPEED)
                        turnSpeed = flipper.getAngularVelocity()
                        flipper.rotate(turnSpeed * dt)
                    else:
                        flipper.setAngularVelocity(0)
                        flipper.setFlipState("")

        #timer
        if endTimer >= 0:
            if len(dataReceived) > 0:
                endTimer -= dt
            timerText = ("Time left: " + str(math.floor(endTimer)))
            timerTextSurf = font.render(timerText, False, "black")
            screen.blit(timerTextSurf, (1000, 0))

            #avoid accidental score change
            if endTimer >= (TIMERSTART - 1):
                for ball in pinballGroup:
                    ball.setScore(0)
        else:
            if endText == "":
                endText = endScreen(pinballGroup)
            if len(pinballGroup) > 0:
                pinballGroup.empty()
            else:
                endTextSurf = font.render(endText, False, "black")
                screen.blit(endTextSurf, (screen.get_width()/2-100, screen.get_height()/2))

        pygame.display.flip()
        dt = clock.tick(1000) / 1000
        
    return
