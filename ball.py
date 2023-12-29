import pygame
import math

#Create a class for the pinballs
class ball(pygame.sprite.Sprite):
    def __init__(self, radius, colour, position, velocity, acceleration, lives):
        pygame.sprite.Sprite.__init__(self)
        self.radius = radius
        self.colour = colour
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.lives = lives
        
        self.currentLine = []
        self.currentObstacle = 0
        self.inBlock = False

        #drawing
        self.image = pygame.Surface((2*radius,2*radius))
        self.centre = (self.image.get_width()/2, self.image.get_height()/2)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(center=position)
        pygame.draw.circle(self.image, colour, (self.centre), radius)
        self.mask = pygame.mask.from_surface(self.image)
        
    #Getters

    def getRadius(self):
        return(self.radius)

    def getPosition(self):
        return(self.position)

    def getVelocity(self):
        return(self.velocity)

    def getAcceleration(self):
        return(self.acceleration)

    def getColour(self):
        return(self.colour)

    def checkTouching(self):
        return(self.touching)

    def getVelocityAngle(self):
        if self.velocity[1] == 0:
            angle = math.pi
        else:
            ratio = abs(self.velocity[0]/self.velocity[1])
            angle = math.atan(ratio)
        return(angle)

    def getVelocityMagnitude(self):
        magnitude = self.velocity.magnitude()
        return magnitude

    def getAccelerationAngle(self):
        if self.acceleration[1] == 0:
            angle = math.pi
        else:
            ratio = abs(self.acceleration[0]/self.acceleration[1])
            angle = math.atan(ratio)
        return(angle)

    def getAccelerationMagnitude(self):
        magnitude = self.acceleration.magnitude()
        return magnitude

    def getCurrentLine(self):
        return(self.currentLine)

    def getCurrentObstacle(self):
        return(self.currentObstacle)

    #Setters

    def setRadius(self, radius):
        self.radius = radius

    def setPosition(self, position):
        self.position = position

    def setVelocity(self, velocity):
        self.velocity = velocity

    def setAcceleration(self, acceleration):
        self.acceleration = acceleration

    def setColour(self, colour):
        self.colour = colour

    def setCurrentLine(self, collideObjects):
        self.currentLine = currentLine

    
    #Methods

    def bounce(self, obstacle):
        #lines
        line = obstacle.getCollisionSide(self.position)
        previousLine = self.currentLine
        normalisedSide = obstacle.normaliseSide(line)
        lineAngle = obstacle.getLineAngle(line)
        normal = obstacle.getNormal(line, self.position)
        depthVector = obstacle.getDepthVector(line, self)
        depthMagnitude = depthVector.magnitude()

        #velocity
        velocityAngle = self.getVelocityAngle()
        speed = self.velocity.magnitude()
        angleDiffVelocity = lineAngle + velocityAngle
        appliedSpeedAway = speed * math.sin(angleDiffVelocity) + (10*depthMagnitude)
        velocityAway = normal * appliedSpeedAway

        #output
        #self.position += depthVector
        if normal.dot(self.velocity) < 0: #only bounce if velocity is facing side
            self.velocity += velocityAway + (normal * obstacle.bounciness * 100)

    def update(self):
        self.image = pygame.Surface((2*self.radius,2*self.radius))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(center=(self.position))
        pygame.draw.circle(self.image, self.colour, (self.centre), self.radius)
        self.mask = pygame.mask.from_surface(self.image)
