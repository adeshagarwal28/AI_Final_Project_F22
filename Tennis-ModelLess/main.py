import time
import numpy as np
import pygame
import sys

from pygame.locals import *
pygame.init()

#creates the tennis class
class Tennis:
    def __init__(self, minXvalue, maxXvalue, minYvalue, maxYvalue):

        self.StaticDiscipline = {
            'minXvalue': minXvalue,
            'maxXvalue': maxXvalue,
            'minYvalue': minYvalue,
            'maxYvalue': maxYvalue
        }

    #creates the tennis function
    def tennis(self, sourceXvalue, sourceYvalue=100, newYvalue=600, divisorvalue=50): 
    

        while True:
            ListOfXsourceYSource = []
            newXvalue = np.random.choice([i for i in range(
                self.StaticDiscipline['minXvalue'], self.StaticDiscipline['maxXvalue'])], 1)

            sourcevalue = (sourceXvalue, sourceYvalue)
            targetvalue = (newXvalue[0], newYvalue)

            #Intercept value and Slope value
            slopevalue = (sourceYvalue - newYvalue)/(sourceXvalue - newXvalue[0])
            interceptvalue = sourceYvalue - (slopevalue*sourceXvalue)
            if (slopevalue != np.inf) and (interceptvalue != np.inf):
                break
            else:
                continue

      
        NewXList = [sourceXvalue]

        if sourceXvalue < newXvalue:
            diff = newXvalue[0] - sourceXvalue
            increase = diff / divisorvalue
            newXval = sourceXvalue
            for i in range(divisorvalue):
                newXval += increase
                NewXList.append(int(newXval))
        else:
            diff = sourceXvalue - newXvalue[0]
            decrease = diff / divisorvalue
            newXval = sourceXvalue
            for i in range(divisorvalue):
                newXval -= decrease
                NewXList.append(int(newXval))

        # Find the values of y
        yNewList = []
        for i in NewXList:
            findYvaue = (slopevalue * i) + interceptvalue  # using y = mx + c
            yNewList.append(int(findYvaue))

        ListOfXsourceYSource = [(x, y) for x, y in zip(NewXList, yNewList)]

        return NewXList, yNewList


# Define Boundries
netvalue = Tennis(150, 450, 100, 600)
NetworkAvalue = netvalue.tennis(300, sourceYvalue=100, newYvalue=600)  
NetworkBvalue = netvalue.tennis(200, sourceYvalue=600, newYvalue=100)

# show test of tennis A and  tennis B
DefPositionA = 300
DefPositionB = 300


def DefPosition(pos1, pos2=300, divisorvalue=50):
    NewXList = []
    if pos1 < pos2:
        diff = pos2 - pos1
        increase = diff / divisorvalue
        newXval = pos1
        for i in range(divisorvalue):
            newXval += increase
            NewXList.append(int(np.floor(newXval)))

    else:
        diff = pos1 - pos2
        decrease = diff / divisorvalue
        newXval = pos1
        for i in range(divisorvalue):
            newXval -= decrease
            NewXList.append(int(np.floor(newXval)))
    return NewXList


outvalue = DefPosition(250)


pygame.init()

FramesPerSecond = 50
FramesPerSecondClock = pygame.time.Clock()

# set the window
BOARDDISPLAY = pygame.display.set_mode((600, 700), 0, 32)
pygame.display.set_caption('TABLE TENNIS using REINFORCEMENT LEARNING')
# set the colors
BlackColor = (0, 0, 0)
WhiteColor = (255, 255, 255)
RedColor = (255, 0, 0)
BlueColor = (0, 0, 255)


def show():
    BOARDDISPLAY.fill(WhiteColor)
    pygame.draw.rect(BOARDDISPLAY, BlueColor, (150, 100, 300, 500))
    pygame.draw.rect(BOARDDISPLAY, BlackColor, (150, 340, 300, 20))
    pygame.draw.rect(BOARDDISPLAY, RedColor, (0, 20, 600, 20))
    pygame.draw.rect(BOARDDISPLAY, RedColor, (0, 660, 600, 20))
    return


#main method
def main():
    APLAYER = pygame.image.load('images/player.jpg')
    APLAYER = pygame.transform.scale(APLAYER, (50, 50))
    BPLAYER = pygame.image.load('images/player.jpg')
    BPLAYER = pygame.transform.scale(BPLAYER, (50, 50))
    tennisball = pygame.image.load('images/tennisball.png')
    tennisball = pygame.transform.scale(tennisball, (15, 15))

    APlayerX = 150
    BPlayerX = 250
    Xball = 250
    Yball = 300

    playernext = 'A'
    coordinateX = 350
    counter = 0
    while True:
        show()
        if playernext == 'A':
            # A player should play
            if counter == 0:
                NetworkAvalue = netvalue.tennis(
                    coordinateX, sourceYvalue=100, newYvalue=600) 
                outvalue = DefPosition(coordinateX)

                # update coordinateX
                Yball = NetworkAvalue[1][counter]
                APlayerX = Xball
                counter += 1
            else:
                Xball = NetworkAvalue[0][counter]
                Yball = NetworkAvalue[1][counter]
                BPlayerX = Xball
                APlayerX = outvalue[counter]
                counter += 1

            # let B player play after 50 tennisball movement
            if counter == 49:
                counter = 0
                playernext = 'B'
            else:
                playernext = 'A'

        else:
            # B player can play
            if counter == 0:
                NetworkBvalue = netvalue.tennis(
                    coordinateX, sourceYvalue=600, newYvalue=100)  
                outvalue = DefPosition(coordinateX)

                # update coordinateX
                Yball = NetworkBvalue[1][counter]
                BPlayerX = Xball
                counter += 1
            else:
                # update coordinateX
                Xball = NetworkBvalue[0][counter]
                Yball = NetworkBvalue[1][counter]
                BPlayerX = outvalue[counter]
                APlayerX = Xball
                counter += 1

            # let A player play after 50 tennisball movement
            if counter == 49:
                counter = 0
                playernext = 'A'
            else:
                playernext = 'B'

        # CHECK MOVEMENT of TennisBALL
        BOARDDISPLAY.blit(APLAYER, (APlayerX, 50))
        BOARDDISPLAY.blit(APLAYER, (BPlayerX, 600))
        BOARDDISPLAY.blit(tennisball, (Xball, Yball))

        # update coordinate Last
        coordinateX = Xball

        pygame.display.update()
        FramesPerSecondClock.tick(FramesPerSecond)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()
