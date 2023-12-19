import pygame
import math

#Create a class for the pinballs
class ball(pygame.sprite.Sprite):
    def __init__(self, radius, colour, position, velocity, acceleration, colliding, lives):
        pygame.sprite.Sprite.__init__(self)
        self.radius = radius
        self.colour = colour
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.colliding = colliding
        self.lives = lives

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

    def getAccelerationAngle(self):
        if self.acceleration[1] == 0:
            angle = math.pi
        else:
            ratio = abs(self.acceleration[0]/self.acceleration[1])
            angle = math.atan(ratio)
        return(angle)

    def isColliding(self):
        return(self.colliding)

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

    def setColliding(self, colliding):
        self.colliding = colliding
        
    #Methods

    def bounce(self, obstacle):
        line = obstacle.getCollisionSide(self.position)
        normal = obstacle.getNormal(line)
        lineAngle = obstacle.getLineAngle(line)

        velocityAngle = self.getVelocityAngle()
        angleDiffVelocity = lineAngle - velocityAngle
        
        accelerationAngle = self.getAccelerationAngle()
        angleDiffAcceleration = lineAngle - accelerationAngle

        if self.colliding == True:
            newAcceleration = pygame.Vector2.magnitude(self.acceleration) * math.sin(angleDiffAcceleration)
            self.acceleration -= normal * newAcceleration
            newSpeed = pygame.Vector2.magnitude(self.velocity) * math.sin(angleDiffVelocity) * obstacle.bounce

        if self.velocity.y > 10:
            self.velocity -= normal * newSpeed
        elif self.velocity.y < 10:
            self.velocity += normal * newSpeed
        if self.velocity.magnitude() < 10:
            self.colliding = False
        

    def update(self):
        self.image = pygame.Surface((2*self.radius,2*self.radius))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(center=(self.position))
        pygame.draw.circle(self.image, self.colour, (self.centre), self.radius)
        self.mask = pygame.mask.from_surface(self.image)
        
