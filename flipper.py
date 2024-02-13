import pygame
import math
import geofuncs
import obstacle

class flipper(obstacle.obstacle):
    #init
    def __init__(self, playerNo, position, leftRight):

        self.playerNo = playerNo
        self.position = position
        self.leftRight = leftRight
        self.flipState = ""
        self.time = 0
        
        if playerNo == 1:
            colour = "blue"
        else:
            colour = "red"

        if leftRight == "left":
            xChange = 200
        else:
            xChange = -200

        position = pygame.Vector2(position)
        self.vertices = []
        newVertex = position + pygame.Vector2(0, 20)
        self.vertices += [[newVertex.x, newVertex.y]]
        newVertex = position + pygame.Vector2(0, -20)
        self.vertices += [[newVertex.x, newVertex.y]]
        newVertex = position + pygame.Vector2(xChange, -10)
        self.vertices += [[newVertex.x, newVertex.y]]
        newVertex = position + pygame.Vector2(xChange, 10)
        self.vertices += [[newVertex.x, newVertex.y]]

        obstacle.obstacle.__init__(self, self.vertices, 0, colour, 0, 0)
        self.setTurnPoint(pygame.Vector2(position))

    #getters
    def getPlayerNo(self):
        return (self.playerNo)

    def getLeftRight(self):
        return (self.leftRight)

    def getFlipState(self):
        return(self.flipState)

    def getTime(self):
        return(self.time)
        
    #setters

    def setFlipState(self, flipState):
        self.flipState = flipState

    def setTime(self, time):
        self.time = time





















        
