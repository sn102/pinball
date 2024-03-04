import math
import pygame
import time
from obstacle import obstacle
from flipper import flipper
from ball import ball
import mapfuncs
from buttons import menuButton
from endScreen import endScreen
#from server import serverGame
#from client import clientGame
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

#open menu which returns socket
#playerType = menu(screen)
#if playerType == "host":
    #hostSetup()
#else:
    #clientSetup()

#create obstacles
machine = open("map.txt", "r")
obstacleGroup = pygame.sprite.Group()
for line in machine:
    line = line.strip()
    line = line.split(".")
    line[0] = mapfuncs.convertStringToList(line[0])
    line[1] = int(line[1])
    line[3] = int(line[3])
    line[4] = int(line[4])
    obstacleGroup.add(obstacle(line[0], line[1], line[2], line[3], line[4]))
machine.close()

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
player2 = ball(40, "purple", (1080, 200), pygame.Vector2(0, 0), GRAVITY, 2)
pinballGroup = pygame.sprite.Group()
pinballGroup.add(player1)
pinballGroup.add(player2)



#main game loop

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    #update obstacle sprites
    obstacleGroup.update()
    obstacleGroup.draw(screen)

    

    #update pinball sprites
    pinballGroup.update()
    pinballGroup.draw(screen)

    #ball physics and score update
    for ball in pinballGroup:
        ball.setVelocity(ball.getVelocity() + (ball.getAcceleration() * dt))
        ball.setPosition(ball.getPosition() + (ball.getVelocity() * dt))
        ball.setAcceleration(pygame.Vector2(GRAVITY))

        screen.blit(ball.getTextSurf(), (0, (50 * ball.getPlayerNo())))

        #if ball falls out of range
    if player1.getPosition().y > 1280 or player1.getPosition().y < 0:
        player1.setPosition((250, 250))
        player1.setVelocity(pygame.Vector2(0,0))
    if player2.getPosition().y > 1280 or player2.getPosition().y < 0:
        player2.setPosition((1080, 200))
        player2.setVelocity(pygame.Vector2(0,0))
        

    #collision
    mapfuncs.checkCollideObstacle(pinballGroup, obstacleGroup)
    mapfuncs.checkCollideBall(pinballGroup)
        
    #flipper controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and P1FlipperL.getFlipState() == "":
        P1FlipperL.setFlipState("up")
        P1FlipperL.setTime(FLIPTIME)

    if keys[pygame.K_d] and P1FlipperR.getFlipState() == "":
        P1FlipperR.setFlipState("up")
        P1FlipperR.setTime(FLIPTIME)

    if keys[pygame.K_LEFT] and P2FlipperL.getFlipState() == "":
        P2FlipperL.setFlipState("up")
        P2FlipperL.setTime(FLIPTIME)

    if keys[pygame.K_RIGHT] and P2FlipperR.getFlipState() == "":
        P2FlipperR.setFlipState("up")
        P2FlipperR.setTime(FLIPTIME)


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
        endTimer -= dt
        timerText = ("Time left: " + str(math.floor(endTimer)))
        timerTextSurf = font.render(timerText, False, "black")
        screen.blit(timerTextSurf, (1000, 0))
    else:
        if endText == "":
            endText = endScreen(pinballGroup)
        else:
            endTextSurf = font.render(endText, False, "black")
            screen.blit(endTextSurf, (screen.get_width()/2-100, screen.get_height()/2))

        
    pygame.display.flip()
    dt = clock.tick(1000) / 1000

pygame.quit()

