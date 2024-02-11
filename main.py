# Example file showing a circle moving on screen
import math
import pygame
import time
from obstacle import obstacle
from flipper import flipper
from ball import ball
from newfunctions import convertStringToList
from buttons import menuButton

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

#init variables
dt = 0
GRAVITY = pygame.Vector2(0, 2000)
unpressed = True
unpressed2 = True
debugList = []
lineCount = 0

#flippers
timer = 0
flipping1 = False



#create pinballs
player1 = ball(50, "blue", (640, 200), pygame.Vector2(0, 0), GRAVITY, 1)
player2 = ball(50, "purple", (840, 100), pygame.Vector2(300, 500), GRAVITY, 1)
pinballGroup = pygame.sprite.Group()
pinballGroup.add(player1)
pinballGroup.add(player2)

#create obstacles
machine = open("map.txt", "r")
obstacleGroup = pygame.sprite.Group()
for line in machine:
    line = line.strip()
    line = line.split(".")
    line[0] = convertStringToList(line[0])
    line[1] = int(line[1])
    obstacleGroup.add(obstacle(line[0], line[1], line[2]))
machine.close()
flipper1 = flipper(1, [100,500], "left")
obstacleGroup.add(flipper1)
flipper1.setAngularVelocity(-math.pi/2)
#obstacleGroup.add(flipper(2, [700,500], "right"))


#collision check function
def checkCollideObstacle(pinballGroup, obstacleGroup):
    for ball in pinballGroup:
        for obstacle in obstacleGroup:
            if pygame.sprite.collide_mask(ball, obstacle):
                ball.bounceObstacle(obstacle)

def checkCollideBall(pinballGroup):
    for ball in pinballGroup:
        for ball2 in pinballGroup:
            if pygame.sprite.collide_circle(ball, ball2) and ball != ball2:
                ball.bounceBall(ball2)

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

    #ball physics
    for ball in pinballGroup:
        ball.setVelocity(ball.getVelocity() + (ball.getAcceleration() * dt))
        ball.setPosition(ball.getPosition() + (ball.getVelocity() * dt))
        ball.setAcceleration(pygame.Vector2(GRAVITY))

    #collision
    checkCollideObstacle(pinballGroup, obstacleGroup)
    checkCollideBall(pinballGroup)
        
    #flipper controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and not flipping1:
        flipping1 = True


    for obstacle in obstacleGroup:
        obstacle.translate(obstacle.getVelocity()*dt)
        obstacle.rotate(obstacle.angularVelocity * dt)

    
    flipper1.rotate(dt)
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(100) / 1000

pygame.quit()
