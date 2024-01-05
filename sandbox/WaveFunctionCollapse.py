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
        myMap[1][0] = 2

        self.getEntropy(myMap, 2, 0)

        # self.findEnd(myMap) # different concept

        return self.generateAll(myMap, a, b)

    def generateAll(self, myMap, x, y):  # recursion
        if (self.countEmpty(myMap) == 0):
            return myMap

        return myMap # temp

    def getLowestEntropy(self, myMap): # returns positions of the lowest entropys
        a = 0
        b = 0
        lowestEntropy = float('inf')  # infinity
        positions = []
        while a < len(myMap):
            b = 0
            while b <= len(myMap[a]):
                if self.getEntropy(myMap, a, b) < lowestEntropy:
                    lowestEntropy = self.getEntropy(myMap, a, b)
                    positions.append((a, b))
                b += 1
            a += 1

        return positions

    def getEntropy(self, myMap, x, y): # returns the entropy of the given point (x, y)
        # This function is not very clean
        count = 0

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
            if myMap[x][y -1] == -1:
                possibleTop.append(0)
                possibleTop.append(1)
            else:
                possibleTop.append(self.definition[myMap[x][y - 1]][3])

        # Bottom
        if y + 1 > len(myMap[0]) - 1:
            possibleBottom.append(0)
        else:
            if myMap[x][y + 1] == -1:
                possibleBottom.append(0)
                possibleBottom.append(1)
            else:
                possibleBottom.append(self.definition[myMap[x][y + 1]][1])

        print(possibleTop)
        print(possibleRight)
        print(possibleBottom)
        print(possibleLeft)


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
                count += 1


        print("Count: " + str(count))
        return count

    def countEmpty(self, myMap):
        a = 0
        b = 0
        count = 0
        while a < len(myMap):
            b = 0
            while b < len(myMap[a]):
                if myMap[a][b] == -1:
                    count += 1
                b += 1
            a += 1

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
