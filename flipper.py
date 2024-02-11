import pygame
import math
import geofuncs
import obstacle

class flipper(obstacle.obstacle):
    #init
    def __init__(self, playerNo, position, leftRight):
        
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

        obstacle.obstacle.__init__(self, self.vertices, 0, colour)
        self.setTurnPoint(pygame.Vector2(position))

        #getters
        def getPlayerNo():
            return playerNo
        def getLeftRight():
            return leftRight

        #methods

        def flip():
            time = self.time / dt
            






















        
