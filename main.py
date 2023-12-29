# Example file showing a circle moving on screen
import pygame
from obstacle import obstacle
from ball import ball
import time

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
bouncing = False

#init variables
dt = 0
collidetime = 1
GRAVITY = pygame.Vector2(0, 2000)

#create pinballs
player1 = ball(50, "blue", (640, 200), pygame.Vector2(0,-500), GRAVITY, 1)
player2 = ball(50, "purple", (screen.get_width()/2, 200), pygame.Vector2(-300, -500), GRAVITY, 1)
pinballGroup = pygame.sprite.Group()
pinballGroup.add(player1)
#pinballGroup.add(player2)

#create obstacles
obstacle1 = obstacle([[0, 600], [1280, 700], [1280, 1020], [0, 1020]], 0, "red")
obstacle2 = obstacle([(1280,200), (500,720), (1280, 360)], 0, "green")
obstacle3 = obstacle(([0,500], [1280,500], [650, 720]), 10, "orange")
obstacleGroup = pygame.sprite.Group()
obstacleGroup.add(obstacle1)
obstacleGroup.add(obstacle2)
#obstacleGroup.add(obstacle3)



#collision check function
def checkCollide(pinballGroup, obstacleGroup):
    for ball in pinballGroup:
        for obstacle in obstacleGroup:
            if pygame.sprite.collide_mask(ball, obstacle):
                ball.bounce(obstacle)
                #time.sleep(1)

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
    print(obstacle1.getVertices())

    #update pinball sprites
    pinballGroup.update()
    pinballGroup.draw(screen)
    player1.setColour("blue")

    #ball physics
    for ball in pinballGroup:
        ball.setVelocity(ball.getVelocity() + (ball.getAcceleration() * dt))
        ball.setPosition(ball.getPosition() + (ball.getVelocity() * dt))
        ball.setAcceleration(pygame.Vector2(GRAVITY))

    #collision
    checkCollide(pinballGroup, obstacleGroup)
        
    #debug
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
        print(player1.acceleration)
    if keys[pygame.K_2]:
        obstacle1.translate(pygame.Vector2(0,-500) * dt)
    if keys[pygame.K_3]:
        obstacle1.translate(pygame.Vector2(0,500) * dt)
    if keys[pygame.K_w]:
        print(player1.getAcceleration())
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
