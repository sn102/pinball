import pygame
import math

class obstacle(pygame.sprite.Sprite):
    def __init__(self, vertices, bounce, colour):
        #initialise Sprite superclass
        pygame.sprite.Sprite.__init__(self)

        #initialise attributes
        self.vertices = list(vertices)
        self.bounce = bounce
        self.colour = colour
        self.position = self.getMidpoint()
        
        #add last coord to finish polygon
        #self.vertices += [self.vertices[0]]

        #drawing
        #self.image = pygame.Surface((self.getWidth(), self.getHeight()))
        #self.image.set_colorkey((0,0,0))
        #self.rect = self.image.get_rect(center=(self.position))
        #pygame.draw.polygon(self.image, colour, self.vertices)
        #self.mask = pygame.mask.from_surface(self.image)


    #Getters

    def getVertices(self):
        return(self.vertices)

    def getBounce(self):
        return(self.getBounce)

    def getLowest(self, xory): #returns minimum x or y coordinate
        if xory == "x" or xory == "X":
            xory = 0
        elif xory == "y" or xory == "Y":
            xory = 1
        lowest = self.vertices[0][xory]
        for coord in self.vertices:
            if lowest > coord[xory]:
                lowest = coord[xory]
        return(lowest)

    def getHighest(self, xory): #returns maximum x or y coordinate
        if xory == "x" or xory == "X":
            xory = 0
        elif xory == "y" or xory == "Y":
            xory = 1
        highest = self.vertices[0][xory]
        for coord in self.vertices:
            if highest < coord[xory]:
                highest = coord[xory]
        return(highest)

    def getMidpoint(self):
        midX = (self.getHighest("x") + self.getLowest("x")) / 2
        midY = (self.getHighest("y") + self.getLowest("y")) / 2
        return pygame.Vector2(midX, midY)

    def getHeight(self): #returns highest y - lowest y
        return(self.getHighest("y") - self.getLowest("y"))

    def getWidth(self): #returns highest x - lowest x
        return(self.getHighest("x") - self.getLowest("x"))

    def getDrawnVertices(self): #gets coordinate to draw on the surface
        drawnVertices = []
        while len(drawnVertices) < len(self.vertices)-1:
            for coord in self.vertices:
                    #shift coordinates so that the top-left is always at [0,0]
                    newCoordX = coord[0] - self.getLowest("x")
                    newCoordY = coord[1] - self.getLowest("y")
                    drawnVertices += [[newCoordX, newCoordY]]
        return(drawnVertices)

    def getCosAngleVariance(self, sideNo, ballPos): #Finds cos of angle that ball is in relation to side
        x1 = self.vertices[sideNo-1][0]
        x2 = self.vertices[sideNo][0]
        y1 = self.vertices[sideNo-1][1]
        y2 = self.vertices[sideNo][1]
        xBall = ballPos[0]
        yBall = ballPos[1]
        sideA = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        sideB = math.sqrt((xBall-x1)**2 + (yBall-y1)**2)
        sideC = math.sqrt((x2-xBall)**2 + (y2-yBall)**2)
        cosA = (((sideB)**2+(sideC)**2-(sideA)**2)/(2*sideB*sideC)) #using cosine rule
        return(cosA)

    def getCollisionSide(self, ballPos):
        greatestAngle = self.getCosAngleVariance(1, ballPos)
        collisionSide = 1
        for sideNo in range(1, len(self.vertices)):
            if greatestAngle > self.getCosAngleVariance(sideNo, ballPos):
                greatestAngle = self.getCosAngleVariance(sideNo, ballPos)
                collisionSide = sideNo
        collisionSide = [self.vertices[collisionSide-1], self.vertices[collisionSide]]
        return(collisionSide)
                
    def getLineAngle(self, line):
        dy = abs(line[0][1]-line[1][1])
        dx = abs(line[0][0]-line[1][0])
        if dy == 0:
            angle = (math.pi)/2
        else:
            angle = math.atan(dx/dy)
        return(angle)

    def getNormal(self, line):
        dy = line[0][1]-line[1][1]
        dx = line[0][0]-line[1][0]
        if dy == 0:
            return(pygame.Vector2(0,1))
        inverseGradient = -1 * (dx)/(dy)
        normalLine = pygame.Vector2((line[0][0], line[0][1]), (line[1][0], line[0][1] + dx * inverseGradient))
        normalised =  pygame.math.Vector2.normalize(normalLine)
        normalised.x = -normalised.x
        return(normalised)
    
    #Methods

    def translate(self,vector): #translates shape
        self.position += vector

    def shiftPoint(self, point, vector):
        self.vertices[point-1] += vector

    def update(self):
        self.image = pygame.Surface((self.getWidth(), self.getHeight()))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(center=(self.position))
        pygame.draw.polygon(self.image, self.colour, self.getDrawnVertices())
        self.mask = pygame.mask.from_surface(self.image)
