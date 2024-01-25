# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

#init variables
unpressed = True
unpressed2 = True
mapList = []

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    
    #debug
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    if mouse[0] and unpressed:
        mapList += [[pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]]
        print(mapList)
        unpressed = False
    if not mouse[0]:
        unpressed = True
    if mouse[2] and unpressed2:
        machine = open("map.txt", "a")
        print(mapList)
        machine.write(str(mapList) + ".0.red\n")
        mapList = []
        unpressed2 = False
        machine.close()
    if not mouse[2]:
        unpressed2 = True
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(1000) / 1000

pygame.quit()
