import math
import pygame
from buttons import menuButton

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

#menu buttons
buttonGroup = pygame.sprite.Group()
singlePlayButton = menuButton("red", "SINGLE PLAYER GAME", [screen.get_width()/2, 150])
multiPlayButton = menuButton("orange", "MULTI PLAYER GAME", [screen.get_width()/2, 350])
controlsButton = menuButton("green", "SET CONTROLS", [screen.get_width()/2, 550])
buttonGroup.add(singlePlayButton)
buttonGroup.add(multiPlayButton)
buttonGroup.add(controlsButton)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #clicking buttons
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            for button in buttonGroup:
                if button.getRect().collidepoint(mousePos):
                    print("yaya")

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    buttonGroup.update()
    buttonGroup.draw(screen)
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(100) / 1000

pygame.quit()
