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
        map = []
        a = 0
        while a < x:
            temp = []
            b = 0
            while b < y:
                temp.append(random.randint(0,4))
                b += 1
            map.append(temp)
            a += 1

        a = random.randint(0, x-1)
        b = random.randint(0, y-1)

        map[a][b] = random.randint(1, 4)

        #self.findEnd(map) # different concept

        return self.generateAll(map, a, b)

    def generateAll(self, map, x, y): # recursion
        if(self.countEmpty(map) == 0):
            return map




    def countEmpty(self, map):
        a = 0
        b = 0
        count = 0
        while a < len(map):
            b = 0
            while b < len(map[a]):
                if (map[a][b] == -1):
                    count += 1
                b += 1
            a += 1

        return count

    def findEnd(self, map): # different concept
        a = 0
        b = 0
        while a < len(map):
            b = 0
            while b < len(map[a]):
                if(map[a][b]!=0):
                    tempDefinition = self.definition[map[a][b]]
                    possibleNeighbours = []

                    if (tempDefinition[0] == 1):
                        possibleNeighbours.append([a - 1, b])
                    if (tempDefinition[1] == 1):
                        possibleNeighbours.append([a, b + 1])
                    if (tempDefinition[2] == 1):
                        possibleNeighbours.append([a + 1, b])
                    if (tempDefinition[3] == 1):
                        possibleNeighbours.append([a, b - 1])

                    print(tempDefinition)
                    print(possibleNeighbours)

                b+=1
            a+=1