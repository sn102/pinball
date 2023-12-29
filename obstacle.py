import pygame
import math

class obstacle(pygame.sprite.Sprite):
    def __init__(self, vertices, bounciness, colour):
        #initialise Sprite superclass
        pygame.sprite.Sprite.__init__(self)

        #initialise attributes
        self.vertices = list(vertices)
        self.bounciness = bounciness
        self.colour = colour
        self.position = self.getMidpoint()
        self.calcVertices = self.vertices + [self.vertices[0]] #start and end points are equal for calculations with physics

    #Getters

    def getVertices(self):
        return(self.vertices)

    def getBounciness(self):
        return(self.bounciness)

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

    def getSideLength(self, line):
        length = math.sqrt((line[0][0]-line[1][0])**2 + (line[0][1]-line[1][1])**2)
        return length

    def cosineRule(self, sideA, sideB, sideC): #find angle using cosine rule
        cosA = (((sideB)**2+(sideC)**2-(sideA)**2)/(2*sideB*sideC))
        return cosA

    def getCosAngleVariance(self, sideNo, ballPos): #finds cos of angle that ball is in relation to side
        coord1 = [self.calcVertices[sideNo-1][0], self.calcVertices[sideNo-1][1]]
        coord2 = [self.calcVertices[sideNo][0], self.calcVertices[sideNo][1]]
        coordBall = [ballPos[0], ballPos[1]] 
        sideA = self.getSideLength([coord1, coord2])
        sideB = self.getSideLength([coord1, coordBall])
        sideC = self.getSideLength([coord2, coordBall])
        cosA = self.cosineRule(sideA, sideB, sideC)
        #angle kept as cos so precision not lost
        return(cosA)

    def getCosAngleToBall(self, line, ballPos): #this finds a different angle then getCosAngleVariance
        lineCoord1 = line[0]
        lineCoord2 = line[1]
        sideA = self.getSideLength([ballPos, lineCoord2])
        sideB = self.getSideLength([lineCoord1, lineCoord2])
        sideC = self.getSideLength([lineCoord1, ballPos])
        cosA = self.cosineRule(sideA, sideB, sideC)
        #angle kept as cos so precision not lost
        return(cosA)

    def getInterpolationRatio(self, line, ballPos):
        #vectorCoord1 = pygame.Vector2((line[0][0], line[0][1]))
        #vectorCoord2 = pygame.Vector2((line[1][0], line[1][1]))
        #vectorLine = vectorCoord2 - vectorCoord1
        vectorBall = pygame.Vector2(ballPos)
        cosAngleToBall = self.getCosAngleToBall(line, ballPos)
        distToBall = self.getSideLength([line[1], ballPos])
        lineComponent = distToBall * cosAngleToBall
        interpRatio = lineComponent / self.getSideLength(line)
        return(interpRatio)
        
    def getClosestLinePoint(self, line, ballPos):
        interpRatio = 1 - (self.getInterpolationRatio(line, ballPos))
        vectorCoord1 = pygame.Vector2((line[0][0], line[0][1]))
        vectorCoord2 = pygame.Vector2((line[1][0], line[1][1]))
        lineVector = vectorCoord2 - vectorCoord1
        ballVector = pygame.Vector2(ballPos)
        closestPoint =  vectorCoord1 + interpRatio * lineVector
        return(closestPoint)

    def getNormal(self, line, ballPos):
        ballVector = pygame.Vector2(ballPos)
        normalStart = self.getClosestLinePoint(line, ballPos)
        normalVector = ballVector - normalStart
        normalised = normalVector.normalize()
        return(normalised)

    def getIntersection(self, line1, line2):
        y1 = line1[0][1]
        x1 = line1[0][0]
        y2 = line2[0][1]
        x2 = line2[0][0]
        dy1 = line1[1][1] - line1[0][1]
        dx1 = line1[1][0] - line1[0][0]
        dy2 = line2[1][1] - line2[0][1]
        dx2 = line2[1][0] - line2[0][0]
        gradient1 = dy1/dx1
        yintercept1 = y1 - (gradient1 * x1)
        if dx2 == 0:
            finalX = x2
        else:
            gradient2 = dy2/dx2
            yintercept2 = y2 - (gradient2 * x2)
            finalX = (yintercept2-yintercept1)/(gradient1-gradient2)
        finalY = (gradient1 * finalX) + yintercept1
        return([finalX, finalY])

    def getDepthVector(self, line, ball):
        ballVector = pygame.Vector2(ball.getPosition())
        normal = self.getNormal(line, ball.getPosition())
        ballEdge = ballVector - (ball.getRadius() * normal)
        closestPoint = self.getClosestLinePoint(line, ball.getPosition())
        depthVector = closestPoint - ballEdge
        #print(intersectVector)
        #print(ballVector)
        #print(nextPosition)
        return(depthVector)
    
    def normaliseSide(self, line):
        if line[0][1] > line[1][1]:
            highestPoint = pygame.Vector2(line[0])
            lowestPoint = pygame.Vector2(line[1])
        else:
            highestPoint = pygame.Vector2(line[1])
            lowestPoint = pygame.Vector2(line[0])
        orderedLine = pygame.Vector2(highestPoint - lowestPoint)
        normalised = orderedLine.normalize()
        return normalised
        

    def getCollisionSide(self, ballPos):
        greatestAngle = self.getCosAngleVariance(1, ballPos)
        collisionSide = 1
        for sideNo in range(1, len(self.calcVertices)):
            if greatestAngle > self.getCosAngleVariance(sideNo, ballPos):
                greatestAngle = self.getCosAngleVariance(sideNo, ballPos)
                collisionSide = sideNo
        collisionSide = [self.calcVertices[collisionSide-1], self.calcVertices[collisionSide]]
        return(collisionSide)

    def getLineAngle(self, line):
        dy = abs(line[0][1]-line[1][1])
        dx = abs(line[0][0]-line[1][0])
        if dy != 0:
            tanAngle = dx/dy
        else:
            return(math.pi / 2)
        angle = math.atan(tanAngle)
        return(angle)
        
    #Methods

    def translate(self,vector): #translates shape
        self.position += vector
        for vertex in self.vertices:
            vertex[0] += vector[0]
            vertex[1] += vector[1]

    def shiftPoint(self, point, vector):
        self.vertices[point-1] += vector

    def update(self):
        self.image = pygame.Surface((self.getWidth(), self.getHeight()))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(center=(self.position))
        pygame.draw.polygon(self.image, self.colour, self.getDrawnVertices())
        self.mask = pygame.mask.from_surface(self.image)
