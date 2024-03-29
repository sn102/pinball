#module for menu buttons

import pygame

#font
pygame.font.init()
font = pygame.font.SysFont("arialblack", 30)

class menuButton(pygame.sprite.Sprite):
    def __init__(self, colour, text, coord):
        #initialise sprite superclass
        pygame.sprite.Sprite.__init__(self)
        self.colour = colour
        self.text = text
        self.WIDTH = 400
        self.HEIGHT = 120

        #change top left coord to centre
        coord = [coord[0] - self.WIDTH/2, coord[1] - self.HEIGHT/2]
        

        #drawing
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.image.set_colorkey((0,0,0))
        self.image.fill("green")
        self.rect = pygame.Rect(coord[0], coord[1], self.WIDTH, self.HEIGHT)
        pygame.draw.rect(self.image, colour, self.rect)
        textSurf = font.render(text, False, "black")
        self.image.blit(textSurf, (0, self.HEIGHT/2))

    #getters
    def getRect(self):
        return(self.rect)

    #setters
    def setText(self, text):
        self.text = text

    def setColour(self, colour):
        self.colour = colour

    def update(self):
        pygame.draw.rect(self.image, self.colour, (0, 0, self.WIDTH, self.HEIGHT))
        textSurf = font.render(self.text, False, "white")
        self.image.blit(textSurf, (0, self.HEIGHT/2))
        
