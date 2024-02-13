# Example file showing a circle moving on screen
import math
import pygame
import time
from obstacle import obstacle
from flipper import flipper
from ball import ball
import mapfuncs
from buttons import menuButton
from scorepoint import scorePoint

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

#init variables
dt = 0
unpressed = True
unpressed2 = True
debugList = []
lineCount = 0

#constants
GRAVITY = pygame.Vector2(0, 2000)
FLIPTIME = 0.2


#create pinballs
player1 = ball(50, "blue", (640, 200), pygame.Vector2(0, 0), GRAVITY, 1)
player2 = ball(50, "purple", (840, 100), pygame.Vector2(300, 500), GRAVITY, 2)
pinballGroup = pygame.sprite.Group()
pinballGroup.add(player1)
pinballGroup.add(player2)

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
P1FlipperL = flipper(1, [500,600], "left")
P1FlipperR = flipper(1, [700, 700], "right")

obstacleGroup.add(P1FlipperL)
obstacleGroup.add(P1FlipperR)

flipperGroup = pygame.sprite.Group()
flipperGroup.add(P1FlipperL)
flipperGroup.add(P1FlipperR)

#create score points
#scoreGroup = pygame.sprite.Group()
#scorePoint1 = scorePoint((100,500))
#scoreGroup.add(scorePoint1)


#collision check function

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
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
        P1FlipperL.setTime(FLIPTIME)
        print(player1.score)


    for obstacle in obstacleGroup:
        obstacle.translate(obstacle.getVelocity()*dt)
        obstacle.rotate(obstacle.angularVelocity * dt)

    #flipper rotation
    for flipper in flipperGroup:
        #change flip direction depending on side
        if flipper.getLeftRight() == "left":
            multiplier = -1
        else:
            multiplier = 1
        
        if flipper.getFlipState() == "up":
            if flipper.getTime() > 0:
                flipper.setAngularVelocity(multiplier * math.pi)
                turnSpeed = flipper.getAngularVelocity()
                flipper.rotate(turnSpeed * dt)
                flipper.setTime(flipper.getTime() - dt)
            else:
                flipper.setTime(FLIPTIME)
                flipper.setFlipState("down")

        elif flipper.getFlipState() == "down":
            if -1 * multiplier * flipper.getAngularDisplacement() < 0:
                flipper.setAngularVelocity(multiplier * -math.pi)
                turnSpeed = flipper.getAngularVelocity()
                flipper.rotate(turnSpeed * dt)
            else:
                flipper.setAngularVelocity(0)
                flipper.setFlipState("")

    #score
    #scoreGroup.update()
    #scoreGroup.draw(screen)

        
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(100) / 1000

pygame.quit()
