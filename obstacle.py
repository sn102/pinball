#module for obstacle class

import pygame
import math
import geofuncs

class obstacle(pygame.sprite.Sprite):
    def __init__(self, vertices, bounciness, colour, angularVelocity, scoreValue):
        #initialise Sprite superclass
        pygame.sprite.Sprite.__init__(self)

        #initialise attributes
        self.vertices = list(vertices)
        self.bounciness = bounciness
        self.colour = colour
        self.scoreValue = scoreValue
        self.position = self.getMidpoint()
        self.calcVertices = self.vertices + [self.vertices[0]] #start and end points are equal for calculations with physics

        self.velocity = pygame.Vector2(0,0)
        self.angularVelocity = angularVelocity
        self.angularDisplacement = 0
        self.turnPoint = pygame.Vector2(self.position)
        
    #Getters

    def getVertices(self):
        return(self.vertices)

    def getBounciness(self):
        return(self.bounciness)

    def getVelocity(self):
        return(self.velocity)

    def getAngularVelocity(self):
        return(self.angularVelocity)

    def getAngularDisplacement(self):
        return(self.angularDisplacement)

    def getScoreValue(self):
        return(self.scoreValue)

    
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

    def getDepthVector(self, line, ball):
        ballVector = pygame.Vector2(ball.getPosition())
        normal = geofuncs.getNormal(line, ball.getPosition())
        ballEdge = ballVector - (ball.getRadius() * normal)
        closestPoint = geofuncs.getClosestLinePoint(line, ball.getPosition())
        depthVector = closestPoint - ballEdge
        return(depthVector)

    def getTurnVelocity(self, contactPoint, ballPos, normalBall):
        line = [self.turnPoint, contactPoint]
        if line[1][0] - line[0][0] != 0:
            inverseGradient = -1 / ((line[1][1]-line[0][1]) / (line[1][0] - line[0][0]))
            normalLine = [line[0], [line[0][0]+1, (line[0][0] + 1 * inverseGradient)]]
        else:
            normalLine = [[line[0]], [line[0][0], line[1][0] + 1]]
        radius = geofuncs.getSideLength(line)
        angle = math.acos(geofuncs.getCosAngleToPoint(normalLine, ballPos))
        turnSpeed = radius * self.angularVelocity * math.sin(angle)
        turnVelocity = abs(turnSpeed) * normalBall
        return(turnVelocity)     

    def getCollisionSide(self, ballPos):
        collisionSideNo = 0
        ballVector = pygame.Vector2(ballPos)
        for sideNo in range(len(self.calcVertices)-1):
            start = self.calcVertices[sideNo]
            end = pygame.Vector2(self.calcVertices[sideNo + 1])
            line = [start, end]
            closest = pygame.Vector2(geofuncs.getClosestLinePoint(line, ballPos))
            closestToBall = ballVector - closest
            distance = closestToBall.magnitude()
            if sideNo == 0:
                lowest = distance
                collisionSide = line
            if distance < lowest or sideNo == 0:
                lowest = distance
                collisionSide = line
        return(collisionSide)

    #Setters

    def setVelocity(self, velocity):
        self.velocity = velocity

    def setAngularVelocity(self, angularVelocity):
        self.angularVelocity = angularVelocity

    def setTurnPoint(self, turnPoint):
        self.turnPoint = turnPoint

    #Methods

    def rotate(self, turnSpeed):
        point = pygame.Vector2(self.turnPoint)
        for vertex in self.vertices:
            pointVertexVector = pygame.Vector2(vertex) - pygame.Vector2(point)
            newVertex = pygame.Vector2(point + pointVertexVector.rotate_rad(turnSpeed))
            vertex[0] = newVertex[0]
            vertex[1] = newVertex[1]
            self.angularDisplacement += turnSpeed
        

    def translate(self, vector): #translates shape
        self.position += vector
        for vertex in self.vertices:
            vertex[0] += vector[0]
            vertex[1] += vector[1]
        self.position = self.getMidpoint()

    def shiftPoint(self, point, vector):
        self.vertices[point-1] += vector

    def update(self):
        self.image = pygame.Surface((self.getWidth(), self.getHeight()))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(center=(self.position))
        pygame.draw.polygon(self.image, self.colour, self.getDrawnVertices())
        self.mask = pygame.mask.from_surface(self.image)
