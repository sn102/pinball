import pygame

def convertStringToList(string):
    string = string.split(", ")
    for i in range(len(string)):
        coord = string[i]
        coord = coord.strip("[")
        coord = coord.strip("]")
        string[i] = coord
    n = len(string) // 2
    newList = []
    for i in range(n):
        newList += [[int(string[2 * i]), int(string[2 * i + 1])]]
    return(newList)
            

def checkCollideObstacle(pinballGroup, obstacleGroup):
    for ball in pinballGroup:
        for obstacle in obstacleGroup:
            if pygame.sprite.collide_mask(ball, obstacle):
                ball.bounceObstacle(obstacle)
                ball.increaseScore(obstacle.getScoreValue())


def checkCollideBall(pinballGroup):
    for ball in pinballGroup:
        for ball2 in pinballGroup:
            if pygame.sprite.collide_circle(ball, ball2) and ball != ball2:
                ball.bounceBall(ball2)

