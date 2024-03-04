import math
import pygame

def getSideLength(line):
    length = math.sqrt((line[0][0]-line[1][0])**2 + (line[0][1]-line[1][1])**2)
    return length

def cosineRule(sideA, sideB, sideC): #find angle using cosine rule
    cosA = (((sideB)**2+(sideC)**2-(sideA)**2)/(2*sideB*sideC))
    return cosA

def getCosAngleToPoint(line, point): #this finds a different angle than getCosAngleVariance
    lineCoord1 = line[0]
    lineCoord2 = line[1]
    sideA = getSideLength([point, lineCoord2])
    sideB = getSideLength([lineCoord1, lineCoord2])
    sideC = getSideLength([lineCoord1, point])
    cosA = cosineRule(sideA, sideB, sideC)
    #angle kept as cos so precision not lost
    return(cosA)

def getInterpolationRatio(line, ballPos):
        vectorBall = pygame.Vector2(ballPos)
        cosAngleToBall = getCosAngleToPoint(line, ballPos)
        distToBall = getSideLength([line[0], ballPos])
        lineComponent = distToBall * cosAngleToBall
        interpRatio = lineComponent / getSideLength(line)
        if interpRatio < 0:
            interpRatio = 0
        if interpRatio > 1:
            interpRatio = 1
        return(interpRatio)
        
def getClosestLinePoint(line, ballPos):
    interpRatio = getInterpolationRatio(line, ballPos)
    vectorCoord1 = pygame.Vector2((line[0][0], line[0][1]))
    vectorCoord2 = pygame.Vector2((line[1][0], line[1][1]))
    lineVector = vectorCoord2 - vectorCoord1
    ballVector = pygame.Vector2(ballPos)
    closestPoint =  vectorCoord1 + (interpRatio * lineVector)
    return(closestPoint)

def getNormal(line, ballPos):
    ballVector = pygame.Vector2(ballPos)
    normalStart = getClosestLinePoint(line, ballPos)
    normalVector = ballVector - normalStart
    normalised = normalVector.normalize()
    return(normalised)

def getIntersection(line1, line2):
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

def normaliseSide(line):
    if line[0][1] > line[1][1]:
        highestPoint = pygame.Vector2(line[0])
        lowestPoint = pygame.Vector2(line[1])
    else:
        highestPoint = pygame.Vector2(line[1])
        lowestPoint = pygame.Vector2(line[0])
    orderedLine = pygame.Vector2(highestPoint - lowestPoint)
    normalised = orderedLine.normalize()
    return(normalised)

def getLineAngle(line):
    dy = abs(line[0][1]-line[1][1])
    dx = abs(line[0][0]-line[1][0])
    if dy != 0:
        tanAngle = dx/dy
    else:
        return(math.pi / 2)
    angle = math.atan(tanAngle)
    return(angle)















