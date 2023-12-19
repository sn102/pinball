# Example file showing a circle moving on screen
import pygame
from obstacle import obstacle
from ball import ball

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

dt = 0
collidetime = 1
GRAVITY = pygame.Vector2(0, 2000)

#create pinballs
player1 = ball(50, "blue", (screen.get_width()/2, 720), pygame.Vector2(0, -2000), GRAVITY, False, 3)
pinballGroup = pygame.sprite.Group()
pinballGroup.add(player1)

#create obstacles
obstacle1 = obstacle([(100,60), (900,160), (1200,320)], 1, "red")
obstacleGroup = pygame.sprite.Group()
obstacleGroup.add(obstacle1)

#debug print
print(obstacle1.getVertices())
print(obstacle1.getDrawnVertices())

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
    player1.setColour("blue")

    #ball physics
    for ball in pinballGroup:
        ball.setAcceleration(pygame.Vector2(GRAVITY))
        ball.setVelocity(ball.getVelocity() + ball.getAcceleration() * dt)
        ball.setPosition(ball.getPosition() + ball.getVelocity() * dt)
    

    #collision
    if pygame.sprite.groupcollide(pinballGroup, obstacleGroup, False, False, pygame.sprite.collide_mask):
        player1.setColliding(True)
        player1.bounce(obstacle1)
    else:
        player1.setAcceleration(pygame.Vector2(GRAVITY))
        
    #debug
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
        obstacle1.shiftPoint(1, pygame.Vector2(50,-200)*dt)
    if keys[pygame.K_2]:
        obstacle1.shiftPoint(2, pygame.Vector2(50,-200)*dt)
    if keys[pygame.K_3]:
        obstacle1.shiftPoint(3, pygame.Vector2(50,-200)*dt)
    if keys[pygame.K_w]:
        print(player1.getAcceleration())
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
