import math

import pygame
import random
import os
import time
import numpy


class WaveFunctionCollapse:
    def __init__(self, images, imageDefinition):
        self.images = images
        self.definition = imageDefinition
        self.myMap = []

    def generate(self, x, y):
        myMap = self.createEmptyMap(x, y)


        self.myMap = myMap
        #a = random.randint(0, x - 1)
        #b = random.randint(0, y - 1)
        a = 0
        b = 0
        possible = self.getPossible(myMap, a, b)
        myMap[a][b] = possible[random.randint(0, len(possible)-1)]

        self.myMap = myMap
        return self.generateAll(myMap, a, b)

    def generateAll(self, myMap, x, y):
        while self.countEmpty(myMap) != 0:
            myMap = self.checkEntropy1(myMap)
            self.myMap = myMap
            if self.countEmpty(myMap) != 0:
                position = self.getEmptyClosestTo(myMap, x, y)
                possible = self.getPossible(myMap, position[0], position[1])
                if len(possible) >= 1:
                    index = random.randint(0, len(possible)-1)
                    myMap[position[0]][position[1]] = possible[index]
                else:
                    print(str(position[0]) + " " + str(position[1]))
                    myMap[position[0]][position[1]] = 0
                self.myMap = myMap

        return myMap

    def getEmptyClosestTo(self, myMap, x, y):
        lowestDistance = float('inf')  # infinity
        lowestX = -1
        lowestY = -1
        for i in range(len(myMap)):
            for j in range(len(myMap[0])):
                if myMap[i][j] == -1:
                    absX = x - i
                    absY = y - j
                    distance = math.sqrt(math.pow(absX, 2) + math.pow(absY, 2))
                    if distance < lowestDistance:
                        lowestDistance = distance
                        lowestX = i
                        lowestY = j
        return [lowestX, lowestY]

    def getLowestEntropy(self, myMap): # returns the position of the lowest entropy (only the first)
        lowestEntropy = float('inf')  # infinity
        position = [-1, -1]
        for i in range(len(myMap)):
            for j in range(len(myMap[i])):
                if myMap[i][j] == -1:
                    if self.getEntropy(myMap, i, j) < lowestEntropy:
                        lowestEntropy = self.getEntropy(myMap, i, j)
                        position = (i, j)

        return position

    def checkEntropy1(self, myMap): # fills the map where the entropy is 1
        lowestEntropy = self.getLowestEntropy(myMap)
        if lowestEntropy[0] != -1:
            entropy = self.getEntropy(myMap, lowestEntropy[0], lowestEntropy[1])
            while entropy == 1:
                myMap[lowestEntropy[0]][lowestEntropy[1]] = self.getPossible(myMap, lowestEntropy[0], lowestEntropy[1])[0]
                lowestEntropy = self.getLowestEntropy(myMap)
                if lowestEntropy[0] != -1:
                    entropy = self.getEntropy(myMap, lowestEntropy[0], lowestEntropy[1])
                else:
                    entropy = 0

        return myMap

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
        return count

    def countEmpty(self, myMap): # returns the number of empty fields in the map (counts the -1)
        count = 0
        for i in range(len(myMap)):
            for j in range(len(myMap[i])):
                if myMap[i][j] == -1:
                    count += 1

        return count

    def createEmptyMap(self, x, y):
        myMap = []

        for i in range(x):
            temp = []
            for j in range(y):
                temp.append(-1)
            myMap.append(temp)

        return myMap
