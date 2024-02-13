import pygame
import math

class scorePoint(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.RADIUS = 10
        self.time = 0
        self.collide = True
        self.colour = "red"

        #drawing
        self.image = pygame.Surface((2 * self.RADIUS, 2 * self.RADIUS))
        self.image.set_colorkey((0,0,0))
        self.centre = [self.position[0] + 0.5 * self.RADIUS, self.position[1] + 0.5 * self.RADIUS]
        self.rect = self.image.get_rect(center = self.centre)
        pygame.draw.circle(self.image, self.colour, self.centre, self.RADIUS)


    #getters
    def getTime(self):
        return(self.time)


    #setters
    def setTime(self, time):
        self.time = time

    #methods
    def grab(self):
        self.collide = False
        self.colour = "black"

    def update(self):
        self.image = pygame.Surface((2 * self.RADIUS, 2 * self.RADIUS))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(center = self.centre)
        pygame.draw.circle(self.image, self.colour, self.centre, self.RADIUS)

        
        














        
