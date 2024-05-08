import time
import pygame
import random
import RaceMap


class MapMaker:
    def __init__(self):
        self.mapPosition = [0, 0, 10, 10]
        self.mapRect = pygame.Rect(0, 0, 10, 10)
        self.mapName = "Unknown"
        self.enteringName = False

        self.selectedPiece = 0

        self.emptyMapFiller = -1

        self.x = 5
        self.y = 5
        self.myMap = self.createEmptyMap(self.x, self.y)

        self.definition = [[0, 0, 0, 0], # top, right, bottom, left
                           [1, 0, 0, 1],
                           [1, 1, 0, 0],
                           [0, 0, 1, 1],
                           [0, 1, 1, 0],
                           [1, 0, 1, 0],
                           [0, 1, 0, 1]]
                           #[1, 1, 1, 1]]


    def reset(self):
        self.x = 5
        self.y = 5
        self.myMap = self.createEmptyMap(self.x, self.y)

    def place(self, x, y):
        print(self.getPossible(self.myMap, x, y))
        if self.checkPossible(x, y, self.selectedPiece):
            self.myMap[x][y] = self.selectedPiece

    def checkPossible(self, x, y, piece):
        possible = self.getPossible(self.myMap, x, y)
        return piece in possible

    def getPossible(self, myMap, x: int, y: int): # get all possible patterns for the square (x, y)
        # This function is not very clean
        possible = []

        possibleTop = []
        possibleRight = []
        possibleBottom = []
        possibleLeft = []

        # Left
        if x - 1 < 0:
            possibleLeft.append(0)
        else:
            if myMap[x - 1][y] == -1:
                possibleLeft.append(0)
                possibleLeft.append(1)
            else:
                possibleLeft.append(self.definition[myMap[x - 1][y]][1])

        # Right
        if x + 1 > len(myMap) - 1:
            possibleRight.append(0)
        else:
            if myMap[x + 1][y] == -1:
                possibleRight.append(0)
                possibleRight.append(1)
            else:
                possibleRight.append(self.definition[myMap[x + 1][y]][3])

        # Top
        if y - 1 < 0:
            possibleTop.append(0)
        else:
            if myMap[x][y - 1] == -1:
                possibleTop.append(0)
                possibleTop.append(1)
            else:
                possibleTop.append(self.definition[myMap[x][y - 1]][2])

        # Bottom
        if y + 1 > len(myMap[0]) - 1:
            possibleBottom.append(0)
        else:
            if myMap[x][y + 1] == -1:
                possibleBottom.append(0)
                possibleBottom.append(1)
            else:
                possibleBottom.append(self.definition[myMap[x][y + 1]][0])

        count = 0 # to get the right pattern
        for i in self.definition:
            check = False
            for n in possibleTop:
                if n == i[0]:
                    check = True

            if check:
                check = False
                for n in possibleRight:
                    if n == i[1]:
                        check = True

            if check:
                check = False
                for n in possibleBottom:
                    if n == i[2]:
                        check = True

            if check:
                check = False
                for n in possibleLeft:
                    if n == i[3]:
                        check = True

            if check:
                possible.append(count)

            count += 1

        return possible

    def fillMap(self, value):
        for i in range(len(self.myMap)):
            for j in range(len(self.myMap[0])):
                self.myMap[i][j] = value

    def save(self, path):
        raceMap = RaceMap.RaceMap(self.myMap)
        raceMap.saveMap(path, self.mapName)

    def createEmptyMap(self, x, y):
        newMap = []
        for i in range(x):
            temp = []
            for j in range(y):
                temp.append(self.emptyMapFiller)
            newMap.append(temp)

        return newMap

    def clearMap(self):
        self.fillMap(self.emptyMapFiller)
