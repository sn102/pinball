import pygame
import math
import geofuncs

pygame.font.init()
font = pygame.font.SysFont("arialblack", 30)

#Create a class for the pinballs
class ball(pygame.sprite.Sprite):
    def __init__(self, radius, colour, position, velocity, acceleration, playerNo):
        pygame.sprite.Sprite.__init__(self)
        self.radius = radius
        self.colour = colour
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.playerNo = playerNo
        self.score = 0
        
        self.currentLine = []
        self.currentObstacle = 0

        #drawing
        self.image = pygame.Surface((2*radius,2*radius))
        self.centre = (self.image.get_width()/2, self.image.get_height()/2)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(center=position)
        pygame.draw.circle(self.image, colour, (self.centre), radius)
        self.mask = pygame.mask.from_surface(self.image)

        #score text
        self.text = ("Player " + str(self.playerNo) + " score: " + str(self.score))
        self.textSurf = font.render(self.text, False, "black")
        
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

    def getPlayerNo(self):
        return(self.playerNo)

    def getTextSurf(self):
        return(self.textSurf)

    def getScore(self):
        return(self.score)

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

    def setScore(self, score):
        self.score = score

    def increaseScore(self, score):
        self.score += score

    
    #Methods

    def bounceObstacle(self, obstacle):
        #lines
        line = obstacle.getCollisionSide(self.position)
        previousLine = self.currentLine
        normalisedSide = geofuncs.normaliseSide(line)
        lineAngle = geofuncs.getLineAngle(line)
        normal = geofuncs.getNormal(line, self.position)
        interpRatio = geofuncs.getInterpolationRatio(line, self.position)
        ballRatio = self.radius / geofuncs.getSideLength(line)
        contactPoint = geofuncs.getClosestLinePoint(line, self.position)
        obstacleSpeed = obstacle.velocity.magnitude()
        obstacleSpeedToBall = 0
        turnVelocity = pygame.Vector2(0,0)

        #depth
        depthVector = obstacle.getDepthVector(line, self)
        depthMagnitude = depthVector.magnitude()

        #obstacle velocity
        if obstacleSpeed > 0:
            obstacleVelocityLine = [contactPoint, [contactPoint[0] + obstacle.velocity.x, contactPoint[1] + obstacle.velocity.y]]
            cosObstacleVelocityAngle = geofuncs.getCosAngleToPoint(obstacleVelocityLine, self.position)
            obstacleSpeedToBall = obstacleSpeed * cosObstacleVelocityAngle
                                

        #turning
        if obstacle.angularVelocity != 0:
            turnVelocity = obstacle.getTurnVelocity(contactPoint, self.position, normal)
            obstacleSpeedToBall = obstacleSpeedToBall + turnVelocity.magnitude()
        
        #velocity
        velocityAngle = self.getVelocityAngle()
        speed = self.velocity.magnitude()
        angleDiffVelocity = lineAngle + velocityAngle
        appliedSpeedAway = speed * math.sin(angleDiffVelocity)
        velocityAway = normal * (appliedSpeedAway + obstacleSpeedToBall + obstacle.bounciness * 100)

        #output
        self.velocity += depthVector * depthMagnitude
        if normal.dot(self.velocity - normal * (obstacleSpeedToBall)) < 0:
            self.velocity += velocityAway
            

    def bounceBall(self, ball2):
        #lines
        vectorBetween = ball2.position - self.position
        if vectorBetween.dot(self.velocity) > 0 or vectorBetween.dot(ball2.velocity) < 0:
            vectorBetween = vectorBetween.normalize()
            cosAngle = geofuncs.getCosAngleToPoint([self.position, self.position + self.velocity], ball2.position)
            if cosAngle < 0:
                cosAngle = geofuncs.getCosAngleToPoint([self.position, self.position - self.velocity], ball2.position)
            appliedSpeed = self.velocity.magnitude() * cosAngle

            cosAngle2 = geofuncs.getCosAngleToPoint([ball2.position, ball2.position + ball2.velocity], self.position)
            if cosAngle2 < 0:
                cosAngle2 = geofuncs.getCosAngleToPoint([ball2.position, ball2.position - ball2.velocity], self.position)
            appliedSpeed2 = ball2.velocity.magnitude() * cosAngle2

            appliedSpeedAvg = (appliedSpeed + appliedSpeed2) / 2
            appliedVelocity = appliedSpeedAvg * vectorBetween

            self.velocity -= 2 * appliedVelocity
            ball2.velocity += 2 * appliedVelocity

    def update(self):
        self.image = pygame.Surface((2*self.radius,2*self.radius))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(center=(self.position))
        pygame.draw.circle(self.image, self.colour, (self.centre), self.radius)
        self.mask = pygame.mask.from_surface(self.image)

        #score update
        self.text = ("Player " + str(self.playerNo) + " score: " + str(self.score))
        self.textSurf = font.render(self.text, False, "black")
