import pygame
import random
import os
import time
import numpy


class WaveFunctionCollapse:
    def __init__(self, images, imageDefinition):
        self.images = images
        self.definition = imageDefinition

    def generate(self, x, y):
        myMap = []
        a = 0
        while a < x:
            temp = []
            b = 0
            while b < y:
                temp.append(-1)
                b += 1
            myMap.append(temp)
            a += 1

        a = random.randint(0, x - 1)
        b = random.randint(0, y - 1)

        #myMap[a][b] = random.randint(1, 4)
        #myMap[1][1] = 2
        myMap[0][0] = 4

        myMap[0][1] = 4
        myMap[1][1] = 4
        myMap[2][1] = 4
        myMap[0][2] = 4
        myMap[1][2] = 4
        myMap[2][2] = 4

        print(self.getEntropy(myMap, 0, 1))

        print(self.getLowestEntropy(myMap))
        # self.findEnd(myMap) # different concept
        print(self.getPossible(myMap, 0, 1))

        return self.generateAll(myMap, 0, 0)

    def generateAll(self, myMap, x, y):  # recursion
        if (self.countEmpty(myMap) == 0):
            return myMap

        for i in range(self.countEmpty(myMap)):
            if x + 1 < len(myMap):
                if myMap[x + 1][y] == -1:
                    possibe = self.getPossible(myMap, x+1, y)
                    if len(possibe) > 0:
                        myMap[x + 1][y] = 3
                        print("Test")
                    self.generateAll(myMap, x + 1, y)

        return myMap # temp

    def getLowestEntropy(self, myMap): # returns the position of the lowest entropy
        lowestEntropy = float('inf')  # infinity
        position = []
        for i in range(len(myMap)):
            for j in range(len(myMap[i])):
                if self.getEntropy(myMap, i, j) < lowestEntropy:
                    lowestEntropy = self.getEntropy(myMap, i, j)
                    position = (i, j)

        return position

    def getPossible(self, myMap, x, y): # get all possible patterns for the square (x, y)
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

    def getEntropy(self, myMap, x, y): # returns the entropy of the given point (x, y)
        count = len(self.getPossible(myMap, x, y))
        #print("Count: " + str(count))
        return count

    def countEmpty(self, myMap):
        count = 0
        for i in range(len(myMap)):
            for j in range(len(myMap[i])):
                if myMap[i][j] == -1:
                    count += 1

        return count

    def findEnd(self, myMap):  # different concept
        a = 0
        b = 0
        while a < len(myMap):
            b = 0
            while b < len(myMap[a]):
                if myMap[a][b] != 0:
                    tempDefinition = self.definition[myMap[a][b]]
                    possibleNeighbours = []

                    if tempDefinition[0] == 1:
                        possibleNeighbours.append([a - 1, b])
                    if tempDefinition[1] == 1:
                        possibleNeighbours.append([a, b + 1])
                    if tempDefinition[2] == 1:
                        possibleNeighbours.append([a + 1, b])
                    if tempDefinition[3] == 1:
                        possibleNeighbours.append([a, b - 1])

                    print(tempDefinition)
                    print(possibleNeighbours)

                b += 1
            a += 1
