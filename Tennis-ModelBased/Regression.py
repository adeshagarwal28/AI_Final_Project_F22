import numpy as np


#creates the networking class
class Networking:
    def __init__(self, minXvalue, maxXvalue, minYvalue, maxYvalue):

        self.StaticDiscipline = {
            'minXvalue': minXvalue,
            'maxXvalue': maxXvalue,
            'minYvalue': minYvalue,
            'maxYvalue': maxYvalue
        }

    #creates the net function
    def net(self, sourceXvalue, sourceYvalue=100, newYvalue=600, divisorvalue=50): 

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

def DefPosition(self, pos1, pos2=300, divisorvalue=50):
    DefPositionA = 300
    DefPositionB = 300
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