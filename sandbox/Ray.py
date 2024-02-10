import pygame
import os
import numpy as np


class Ray:
    def __init__(self, posX, posY, direction):
        self.posX = posX
        self.posY = posY
        self.direction = direction
        self.length = -1

    def updateRay(self, posX, posY, direction):
        self.posX = posX
        self.posY = posY
        self.direction = direction
        self.length = -1

    def calcLength(self, lines):

        tempLength = float('inf')
        for line in lines:
            x1 = line[0]
            y1 = line[1]
            x2 = line[2]
            y2 = line[3]

            x3 = self.posX
            y3 = self.posY
            x4 = self.posX + np.cos(np.deg2rad(self.direction))
            y4 = self.posY + np.sin(np.deg2rad(self.direction))

            den = ((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4))

            if den != 0: # if den is 0, the lines are parallel
                t = (((x1 - x3) * (y3 - y4)) - ((y1 - y3) * (x3 - x4))) / den
                u = (((x1 - x2) * (y1 - y3)) - ((y1 - y2) * (x1 - x3))) / (den * (-1))
                if t > 0 and t < 1 and u > 0:
                    pointX = x1 + t * (x2 - x1)
                    pointY = y1 + t * (y2 - y1)


                    newLength = np.sqrt(np.power((self.posX - pointX), 2) + np.power((self.posY - pointY), 2))
                    if newLength < tempLength:
                        tempLength = newLength

        if tempLength < float('inf'):
            self.length = tempLength
        else: # for testing
            self.length = 2000

        return self.length

    def calcOneLine(self, line):
        tempLength = float('inf')

        x1 = line[0]
        y1 = line[1]
        x2 = line[2]
        y2 = line[3]

        x3 = self.posX
        y3 = self.posY
        x4 = self.posX + np.cos(np.deg2rad(self.direction))
        y4 = self.posY + np.sin(np.deg2rad(self.direction))

        den = ((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4))

        if den != 0:  # if den is 0, the lines are parallel
            t = (((x1 - x3) * (y3 - y4)) - ((y1 - y3) * (x3 - x4))) / den
            u = (((x1 - x2) * (y1 - y3)) - ((y1 - y2) * (x1 - x3))) / (den * (-1))
            if t > 0 and t < 1 and u > 0:
                pointX = x1 + t * (x2 - x1)
                pointY = y1 + t * (y2 - y1)

                newLength = np.sqrt(np.power((self.posX - pointX), 2) + np.power((self.posY - pointY), 2))
                if newLength < tempLength:
                    tempLength = newLength

        if tempLength < float('inf'):
            return tempLength
        else:  # for testing
            return 2000
