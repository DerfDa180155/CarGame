import pygame
import random
import os
from numpy import *
import array


class MapCleaner:
    def __init__(self, mapDefinition: array):
        self.mapDefinition = mapDefinition

    def cleanMap(self, inputMap: array, zoomIn: bool = True):
        myMap = list(map(list, inputMap))
        newMap = self.createEmptyMap(len(myMap), len(myMap[0]))

        streets = []
        for i in range(len(myMap)):
            for j in range(len(myMap[0])):
                if myMap[i][j] != 0:
                    streets.append(self.getStreet(myMap, i, j))
                    print(streets)
                    myMap = self.removeStreet(myMap, streets[len(streets)-1])

        newMap = self.addStreet(newMap, inputMap, self.getLongestStreet(streets))
        print("count streets: " + str(len(streets)))
        print("streets:\n" + str(streets))
        print("myMap:\n" + str(myMap))
        print("newMap:\n" + str(newMap))

        if zoomIn:
            # left column
            remove = True
            while remove:
                for i in newMap[0]:
                    if i != 0:
                        remove = False
                if remove:
                    print("remove left:")
                    print(newMap)
                    newMap.pop(0)
                    print(newMap)

            # right column
            remove = True
            while remove:
                for i in newMap[len(newMap)-1]:
                    if i != 0:
                        remove = False
                if remove:
                    print("remove right:")
                    print(newMap)
                    newMap.pop(len(newMap)-1)
                    print(newMap)

            # top row
            remove = True
            while remove:
                for i in newMap:
                    if i[0] != 0:
                        remove = False
                if remove:
                    print("remove top:")
                    print(newMap)
                    for i in newMap:
                        i.pop(0)
                    print(newMap)

            # bottom row
            remove = True
            while remove:
                for i in newMap:
                    if i[len(newMap[len(newMap)-1])-1] != 0:
                        remove = False
                if remove:
                    print("remove bottom:")
                    print(newMap)
                    for i in newMap:
                        i.pop(len(newMap[len(newMap)-1])-1)
                    print(newMap)

        return newMap

    def getStreet(self, myMap: array, x: int, y: int):
        street = [[x, y]]

        currentX = x
        currentY = y
        complete = False

        while not complete:
            currentDefinition = self.mapDefinition[myMap[currentX][currentY]]
            checkAdded = False
            if currentDefinition[0] == 1: # top
                if [currentX, currentY-1] not in street:
                    street.append([currentX, currentY-1])
                    checkAdded = True
                    currentY -= 1
            if currentDefinition[1] == 1 and not checkAdded: # right
                if [currentX+1, currentY] not in street:
                    street.append([currentX+1, currentY])
                    checkAdded = True
                    currentX += 1
            if currentDefinition[2] == 1 and not checkAdded: # down
                if [currentX, currentY+1] not in street:
                    street.append([currentX, currentY+1])
                    checkAdded = True
                    currentY += 1
            if currentDefinition[3] == 1 and not checkAdded: # left
                if [currentX-1, currentY] not in street:
                    street.append([currentX-1, currentY])
                    checkAdded = True
                    currentX -= 1

            if not checkAdded:
                complete = True

        return street

    def removeStreet(self, myMap: array, street: array):
        for i in range(len(street)):
            myMap[street[i][0]][street[i][1]] = 0
        return myMap

    def getLongestStreet(self, streets: array):
        size = 0
        index = 0
        for i in range(len(streets)):
            newSize = len(streets[i])
            if newSize > size:
                size = newSize
                index = i

        return streets[index]

    def addStreet(self, newMap: array, myMap: array, street: array):
        for i in range(len(street)):
            newMap[street[i][0]][street[i][1]] = myMap[street[i][0]][street[i][1]]
        return newMap

    def createEmptyMap(self, x: int, y: int):
        myMap = []

        for i in range(x):
            temp = []
            for j in range(y):
                temp.append(0)
            myMap.append(temp)

        return myMap
