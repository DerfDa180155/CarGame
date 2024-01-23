import pygame
import random
import os
import numpy
import array


class RaceMap:
    def __init__(self, myMap: array, name: str = "Unknown", playerStartX: int = 0, playerStartY: int = 0, playerStartDirection: int = 0):
        self.name = name
        self.myMap = myMap

        self.playerStartX = playerStartX
        self.playerStartY = playerStartY
        self.playerStartDirection = playerStartDirection


    def saveMap(self, path):
        # this function will save the map in a file (with xml or json)
        pass

