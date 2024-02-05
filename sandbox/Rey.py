import pygame
import os
from numpy import *


class Rey:
    def __init__(self, posX, posY, direction):
        self.posX = posX
        self.posY = posY
        self.direction = direction
        self.length = -1

    def updateRey(self, posX, posY, direction):
        self.posX = posX
        self.posY = posY
        self.direction = direction
        self.length = -1

    def calcLength(self, lines):
        self.length = 100 # for Testing


        return self.length

