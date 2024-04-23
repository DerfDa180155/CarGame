import time
import pygame
import random


class MapMaker:
    def __init__(self):
        self.selectedPiece = 0

        self.emptyMapFiller = -1

        self.x = 5
        self.y = 5
        self.myMap = self.createEmptyMap(self.x, self.y)

    def reset(self):
        self.x = 5
        self.y = 5
        self.myMap = self.createEmptyMap(self.x, self.y)

    def createEmptyMap(self, x, y):
        newMap = []
        for i in range(x):
            temp = []
            for j in range(y):
                temp.append(self.emptyMapFiller)
            newMap.append(temp)

        return newMap

    def clearMap(self):
        for i in range(len(self.myMap)):
            for j in range(len(self.myMap[0])):
                self.myMap[i][j] = self.emptyMapFiller
