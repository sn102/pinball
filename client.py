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
import pickle

def clientGame():
    #import stuff -TEMPORARY
    from obstacle import obstacle
    from flipper import flipper
    from ball import ball

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

    
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((socket.gethostname(), 5050))

    clientSocket.send("True".encode("utf-8"))
    print("sent true")
    line = "True"

    obstacleGroup = pygame.sprite.Group()
    while line != "False": #line = false when the last line has been sent
        clientSocket.send("True".encode("utf-8"))
        line = clientSocket.recv(1024).decode("utf-8")
        if line == "False":
            break
        if len(line) > 0:
            print(line)
            line = line.strip()
            line = line.split(".")
            line[0] = mapfuncs.convertStringToList(line[0])
            line[1] = int(line[1])
            line[3] = int(line[3])
            line[4] = int(line[4])
            newObstacle = obstacle(line[0], line[1], line[2], line[3], line[4])
            obstacleGroup.add(newObstacle)

    for obstacle in obstacleGroup:
        print(obstacle)

#-----GAME SETUP-----

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
    player2 = ball(40, "purple", (1030, 250), pygame.Vector2(0, 0), GRAVITY, 2)
    pinballGroup = pygame.sprite.Group()
    pinballGroup.add(player1)
    pinballGroup.add(player2)

#--------------------



#---------GAME LOOP START-------------

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("white")

    #---------NETWORKING------------
        
        #client receives game data and unpickles it
        receivedGameData = clientSocket.recv(1024)
        receivedGameData = pickle.loads(receivedGameData)

        #update player 1 ball
        player1.setPosition(receivedGameData[0][0])
        player1.setVelocity(receivedGameData[0][1])
        player1.setScore(receivedGameData[0][2])

        #update player 2 ball
        player2.setPosition(receivedGameData[1][0])
        player2.setVelocity(receivedGameData[1][1])
        player2.setScore(receivedGameData[1][2])

        #update player 1 flippers
        P1FlipperL.setFlipState(receivedGameData[2][0])
        P1FlipperR.setFlipState(receivedGameData[2][1])

        #update player 2 flippers
        P2FlipperL.setFlipState(receivedGameData[3][0])
        P2FlipperR.setFlipState(receivedGameData[3][1])

        #update timer
        endTimer = receivedGameData[4]
        
    #-------------------------------
        
        #update obstacle sprites
        obstacleGroup.update()
        obstacleGroup.draw(screen)

        #update pinball sprites
        pinballGroup.update()
        pinballGroup.draw(screen)

        #update score
        for ball in pinballGroup:
            screen.blit(ball.getTextSurf(), (0, (50 * ball.getPlayerNo())))


        if dt <= 0.05: #check for window dragging
            for obstacle in obstacleGroup:
                obstacle.translate(obstacle.getVelocity()*dt)
                obstacle.rotate(obstacle.angularVelocity * dt)


        #flipper controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            clientSocket.send("L".encode("utf-8"))

        elif keys[pygame.K_d]:
            clientSocket.send("R".encode("utf-8"))

        else:
            clientSocket.send("False".encode("utf-8"))

        


        
        #flipper rotation
        for flipper in flipperGroup:
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
            timerText = ("Time left: " + str(math.floor(endTimer)))
            timerTextSurf = font.render(timerText, False, "black")
            screen.blit(timerTextSurf, (1000, 0))

            #avoid accidental score change
            if endTimer <= 0.5:
                for ball in pinballGroup:
                    ball.setScore(0)
        else:
            if endText == "":
                endText = endScreen(pinballGroup)
            else:
                endTextSurf = font.render(endText, False, "black")
                screen.blit(endTextSurf, (screen.get_width()/2-100, screen.get_height()/2))

        
        pygame.display.flip()
        dt = clock.tick(1000) / 1000

    pygame.quit()

clientGame()
