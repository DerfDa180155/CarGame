import time
import pygame
import random
import RaceMap


class MapMaker:
    def __init__(self):
        self.mapPosition = [0, 0, 10, 10]
        self.mapRect = pygame.Rect(0, 0, 10, 10)
        self.mapName = ""
        self.enteringName = False

        self.selectedPiece = 0

        self.emptyMapFiller = -1

        self.x = 5
        self.y = 5
        self.myMap = self.createEmptyMap(self.x, self.y)

    def reset(self):
        self.x = 5
        self.y = 5
        self.myMap = self.createEmptyMap(self.x, self.y)

    def place(self, x, y):
        self.myMap[x][y] = self.selectedPiece

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
