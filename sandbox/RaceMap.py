import pygame
import random
import os
import numpy
import array
import xml.etree.cElementTree as ET


class RaceMap:
    def __init__(self, myMap: array, name: str = "Unknown", playerStartX: int = 0, playerStartY: int = 0, playerStartDirection: int = 0):
        self.name = name
        self.myMap = myMap

        self.playerStartX = playerStartX
        self.playerStartY = playerStartY
        self.playerStartDirection = playerStartDirection

        self.mapDefinition = [[0, 0, 0, 0],  # top, right, bottom, left
                              [1, 0, 0, 1],
                              [1, 1, 0, 0],
                              [0, 0, 1, 1],
                              [0, 1, 1, 0],
                              [1, 0, 1, 0],
                              [0, 1, 0, 1]]

        self.boundsMap = []
        self.generateLineMap()

        self.checkpoints = []
        self.generateCheckpoints()

    def saveMap(self, path):
        root = ET.Element("raceMap")
        ET.SubElement(root, "name").text = self.name
        ET.SubElement(root, "playerStartX").text = str(self.playerStartX)
        ET.SubElement(root, "playerStartY").text = str(self.playerStartY)
        ET.SubElement(root, "playerStartDirection").text = str(self.playerStartDirection)
        ET.SubElement(root, "mapSizeX").text = str(len(self.myMap))
        ET.SubElement(root, "mapSizeY").text = str(len(self.myMap[0]))
        testMap = ET.SubElement(root, "map", type="array")
        for i in self.myMap:
            x = ET.SubElement(testMap, "x")
            for j in i:
                y = ET.SubElement(x, "y").text = str(j)

        print(path + self.name + ".xml")
        ET.ElementTree(root).write(path + self.name + ".xml")

    def generateLineMap(self):
        # this functions creates the bounds of the map
        self.boundsMap = []
        #self.boundsMap.append([0,0,1500,100])

        sizeX = len(self.myMap)
        sizeY = len(self.myMap[0])

        sizeXOneSquare = 1600 / sizeX
        sizeYOneSquare = 900 / sizeY

        for i in range(len(self.myMap)):
            for j in range(len(self.myMap[0])):
                match self.myMap[i][j]:
                    case 1: # topLeft
                        # top line horizontal
                        startX = sizeXOneSquare * i
                        startY = sizeYOneSquare * j + sizeYOneSquare * 9 / 32
                        endX = sizeXOneSquare * i + sizeXOneSquare * 9 / 32
                        endY = sizeYOneSquare * j + sizeYOneSquare * 9 / 32
                        self.boundsMap.append([startX, startY, endX, endY])

                        # bottom line horizontal
                        startX = sizeXOneSquare * i
                        startY = sizeYOneSquare * j + sizeYOneSquare * 23 / 32
                        endX = sizeXOneSquare * i + sizeXOneSquare * 23 / 32
                        endY = sizeYOneSquare * j + sizeYOneSquare * 23 / 32
                        self.boundsMap.append([startX, startY, endX, endY])

                        # left line vertical
                        startX = sizeXOneSquare * i + sizeXOneSquare * 9 / 32
                        startY = sizeYOneSquare * j
                        endX = sizeXOneSquare * i + sizeXOneSquare * 9 / 32
                        endY = sizeYOneSquare * j + sizeYOneSquare * 9 / 32
                        self.boundsMap.append([startX, startY, endX, endY])

                        # right line vertical
                        startX = sizeXOneSquare * i + sizeXOneSquare * 23 / 32
                        startY = sizeYOneSquare * j
                        endX = sizeXOneSquare * i + sizeXOneSquare * 23 / 32
                        endY = sizeYOneSquare * j + sizeYOneSquare * 23 / 32
                        self.boundsMap.append([startX, startY, endX, endY])
                    case 2: # topRight
                        # top line horizontal
                        startX = sizeXOneSquare * i + sizeXOneSquare * 23 / 32
                        startY = sizeYOneSquare * j + sizeYOneSquare * 9 / 32
                        endX = sizeXOneSquare * (i + 1)
                        endY = sizeYOneSquare * j + sizeYOneSquare * 9 / 32
                        self.boundsMap.append([startX, startY, endX, endY])

                        # bottom line horizontal
                        startX = sizeXOneSquare * i + sizeXOneSquare * 9 / 32
                        startY = sizeYOneSquare * j + sizeYOneSquare * 23 / 32
                        endX = sizeXOneSquare * (i + 1)
                        endY = sizeYOneSquare * j + sizeYOneSquare * 23 / 32
                        self.boundsMap.append([startX, startY, endX, endY])

                        # left line vertical
                        startX = sizeXOneSquare * i + sizeXOneSquare * 9 / 32
                        startY = sizeYOneSquare * j
                        endX = sizeXOneSquare * i + sizeXOneSquare * 9 / 32
                        endY = sizeYOneSquare * j + sizeYOneSquare * 23 / 32
                        self.boundsMap.append([startX, startY, endX, endY])

                        # right line vertical
                        startX = sizeXOneSquare * i + sizeXOneSquare * 23 / 32
                        startY = sizeYOneSquare * j
                        endX = sizeXOneSquare * i + sizeXOneSquare * 23 / 32
                        endY = sizeYOneSquare * j + sizeYOneSquare * 9 / 32
                        self.boundsMap.append([startX, startY, endX, endY])
                    case 3: # bottomLeft
                        # top line horizontal
                        startX = sizeXOneSquare * i
                        startY = sizeYOneSquare * j + sizeYOneSquare * 9 / 32
                        endX = sizeXOneSquare * i + sizeXOneSquare * 23 / 32
                        endY = sizeYOneSquare * j + sizeYOneSquare * 9 / 32
                        self.boundsMap.append([startX, startY, endX, endY])

                        # bottom line horizontal
                        startX = sizeXOneSquare * i
                        startY = sizeYOneSquare * j + sizeYOneSquare * 23 / 32
                        endX = sizeXOneSquare * i + sizeXOneSquare * 9 / 32
                        endY = sizeYOneSquare * j + sizeYOneSquare * 23 / 32
                        self.boundsMap.append([startX, startY, endX, endY])

                        # left line vertical
                        startX = sizeXOneSquare * i + sizeXOneSquare * 9 / 32
                        startY = sizeYOneSquare * j + sizeYOneSquare * 23 / 32
                        endX = sizeXOneSquare * i + sizeXOneSquare * 9 / 32
                        endY = sizeYOneSquare * (j + 1)
                        self.boundsMap.append([startX, startY, endX, endY])

                        # right line vertical
                        startX = sizeXOneSquare * i + sizeXOneSquare * 23 / 32
                        startY = sizeYOneSquare * j + sizeYOneSquare * 9 / 32
                        endX = sizeXOneSquare * i + sizeXOneSquare * 23 / 32
                        endY = sizeYOneSquare * (j + 1)
                        self.boundsMap.append([startX, startY, endX, endY])
                    case 4: # bottomRight
                        # top line horizontal
                        startX = sizeXOneSquare * i + sizeXOneSquare * 9 / 32
                        startY = sizeYOneSquare * j + sizeYOneSquare * 9 / 32
                        endX = sizeXOneSquare * (i + 1)
                        endY = sizeYOneSquare * j + sizeYOneSquare * 9 / 32
                        self.boundsMap.append([startX, startY, endX, endY])

                        # bottom line horizontal
                        startX = sizeXOneSquare * i + sizeXOneSquare * 23 / 32
                        startY = sizeYOneSquare * j + sizeYOneSquare * 23 / 32
                        endX = sizeXOneSquare * (i + 1)
                        endY = sizeYOneSquare * j + sizeYOneSquare * 23 / 32
                        self.boundsMap.append([startX, startY, endX, endY])

                        # left line vertical
                        startX = sizeXOneSquare * i + sizeXOneSquare * 9 / 32
                        startY = sizeYOneSquare * j + sizeYOneSquare * 9 / 32
                        endX = sizeXOneSquare * i + sizeXOneSquare * 9 / 32
                        endY = sizeYOneSquare * (j + 1)
                        self.boundsMap.append([startX, startY, endX, endY])

                        # right line vertical
                        startX = sizeXOneSquare * i + sizeXOneSquare * 23 / 32
                        startY = sizeYOneSquare * j + sizeYOneSquare * 23 / 32
                        endX = sizeXOneSquare * i + sizeXOneSquare * 23 / 32
                        endY = sizeYOneSquare * (j + 1)
                        self.boundsMap.append([startX, startY, endX, endY])
                    case 5: # verticalLine
                        # left line
                        startX = sizeXOneSquare * i + sizeXOneSquare * 9 / 32
                        startY = sizeYOneSquare * j
                        endX = sizeXOneSquare * i + sizeXOneSquare * 9 / 32
                        endY = sizeYOneSquare * (j + 1)
                        self.boundsMap.append([startX, startY, endX, endY])

                        # right line
                        startX = sizeXOneSquare * i + sizeXOneSquare * 23 / 32
                        endX = sizeXOneSquare * i + sizeXOneSquare * 23 / 32
                        self.boundsMap.append([startX, startY, endX, endY])
                    case 6: # horizontalLine
                        # top line
                        startX = sizeXOneSquare * i
                        startY = sizeYOneSquare * j + sizeYOneSquare * 9 / 32
                        endX = sizeXOneSquare * (i + 1)
                        endY = sizeYOneSquare * j + sizeYOneSquare * 9 / 32
                        self.boundsMap.append([startX, startY, endX, endY])

                        # bottom line
                        startY = sizeYOneSquare * j + sizeYOneSquare * 23 / 32
                        endY = sizeYOneSquare * j + sizeYOneSquare * 23 / 32
                        self.boundsMap.append([startX, startY, endX, endY])

    def generateCheckpoints(self):
        self.checkpoints = []
        sizeX = 1600 / len(self.myMap)
        sizeY = 900 / len(self.myMap[0])

        x = 0
        y = 0
        tempX = self.playerStartX
        tempY = self.playerStartY

        found = False
        while not found:
            if tempX > sizeX:
                x += 1
                tempX -= sizeX
            else:
                found = True

        found = False
        while not found:
            if tempY > sizeY:
                y += 1
                tempY -= sizeY
            else:
                found = True

        if self.myMap[x][y] == 0:
            found = False
            for i in range(len(self.myMap)):
                for j in range(len(self.myMap[0])):
                    if self.myMap[i][j] != 0 and not found:
                        x = i
                        y = j
                        found = True

        street = self.getStreet(self.myMap, x, y)

        sizeX = len(self.myMap)
        sizeY = len(self.myMap[0])

        sizeXOneSquare = 1600 / sizeX
        sizeYOneSquare = 900 / sizeY

        for streetPiece in street:
            if len(self.checkpoints) == 0:
                if self.myMap[streetPiece[0]][streetPiece[1]] == 1 or self.myMap[streetPiece[0]][streetPiece[1]] == 2 or self.myMap[streetPiece[0]][streetPiece[1]] == 5: # top
                    startX = sizeXOneSquare * streetPiece[0] + sizeXOneSquare * 9 / 32
                    startY = sizeYOneSquare * streetPiece[1]
                    endX = sizeXOneSquare * streetPiece[0] + sizeXOneSquare * 23 / 32
                    endY = sizeYOneSquare * streetPiece[1]
                    self.checkpoints.append((startX, startY, endX, endY))
                elif self.myMap[streetPiece[0]][streetPiece[1]] == 4 or self.myMap[streetPiece[0]][streetPiece[1]] == 6: # right
                    startX = sizeXOneSquare * (streetPiece[0] + 1)
                    startY = sizeYOneSquare * streetPiece[1] + sizeYOneSquare * 9 / 32
                    endX = sizeXOneSquare * (streetPiece[0] + 1)
                    endY = sizeYOneSquare * streetPiece[1] + sizeYOneSquare * 23 / 32
                    self.checkpoints.append((startX, startY, endX, endY))
                elif self.myMap[streetPiece[0]][streetPiece[1]] == 3: # left
                    startX = sizeXOneSquare * streetPiece[0]
                    startY = sizeYOneSquare * streetPiece[1] + sizeYOneSquare * 9 / 32
                    endX = sizeXOneSquare * streetPiece[0]
                    endY = sizeYOneSquare * streetPiece[1] + sizeYOneSquare * 23 / 32
                    self.checkpoints.append((startX, startY, endX, endY))
            else:
                match self.myMap[streetPiece[0]][streetPiece[1]]:
                    case 1: # topLeft
                        startX = sizeXOneSquare * streetPiece[0] + sizeXOneSquare * 9 / 32
                        startY = sizeYOneSquare * streetPiece[1]
                        endX = sizeXOneSquare * streetPiece[0] + sizeXOneSquare * 23 / 32
                        endY = sizeYOneSquare * streetPiece[1]
                        checkpointOne = (startX, startY, endX, endY)
                        if self.checkpoints[len(self.checkpoints) - 1] == checkpointOne:
                            startX = sizeXOneSquare * streetPiece[0]
                            startY = sizeYOneSquare * streetPiece[1] + sizeYOneSquare * 9 / 32
                            endX = sizeXOneSquare * streetPiece[0]
                            endY = sizeYOneSquare * streetPiece[1] + sizeYOneSquare * 23 / 32
                            self.checkpoints.append((startX, startY, endX, endY))
                        else:
                            self.checkpoints.append(checkpointOne)
                    case 2: # topRight
                        startX = sizeXOneSquare * streetPiece[0] + sizeXOneSquare * 9 / 32
                        startY = sizeYOneSquare * streetPiece[1]
                        endX = sizeXOneSquare * streetPiece[0] + sizeXOneSquare * 23 / 32
                        endY = sizeYOneSquare * streetPiece[1]
                        checkpointOne = (startX, startY, endX, endY)
                        if self.checkpoints[len(self.checkpoints) - 1] == checkpointOne:
                            startX = sizeXOneSquare * (streetPiece[0] + 1)
                            startY = sizeYOneSquare * streetPiece[1] + sizeYOneSquare * 9 / 32
                            endX = sizeXOneSquare * (streetPiece[0] + 1)
                            endY = sizeYOneSquare * streetPiece[1] + sizeYOneSquare * 23 / 32
                            self.checkpoints.append((startX, startY, endX, endY))
                        else:
                            self.checkpoints.append(checkpointOne)
                    case 3: # bottomLeft
                        startX = sizeXOneSquare * streetPiece[0] + sizeXOneSquare * 9 / 32
                        startY = sizeYOneSquare * (streetPiece[1] + 1)
                        endX = sizeXOneSquare * streetPiece[0] + sizeXOneSquare * 23 / 32
                        endY = sizeYOneSquare * (streetPiece[1] + 1)
                        checkpointOne = (startX, startY, endX, endY)
                        if self.checkpoints[len(self.checkpoints) - 1] == checkpointOne:
                            startX = sizeXOneSquare * streetPiece[0]
                            startY = sizeYOneSquare * streetPiece[1] + sizeYOneSquare * 9 / 32
                            endX = sizeXOneSquare * streetPiece[0]
                            endY = sizeYOneSquare * streetPiece[1] + sizeYOneSquare * 23 / 32
                            self.checkpoints.append((startX, startY, endX, endY))
                        else:
                            self.checkpoints.append(checkpointOne)
                    case 4: # bottomRight
                        startX = sizeXOneSquare * streetPiece[0] + sizeXOneSquare * 9 / 32
                        startY = sizeYOneSquare * (streetPiece[1] + 1)
                        endX = sizeXOneSquare * streetPiece[0] + sizeXOneSquare * 23 / 32
                        endY = sizeYOneSquare * (streetPiece[1] + 1)
                        checkpointOne = (startX, startY, endX, endY)
                        if self.checkpoints[len(self.checkpoints) - 1] == checkpointOne:
                            startX = sizeXOneSquare * (streetPiece[0] + 1)
                            startY = sizeYOneSquare * streetPiece[1] + sizeYOneSquare * 9 / 32
                            endX = sizeXOneSquare * (streetPiece[0] + 1)
                            endY = sizeYOneSquare * streetPiece[1] + sizeYOneSquare * 23 / 32
                            self.checkpoints.append((startX, startY, endX, endY))
                        else:
                            self.checkpoints.append(checkpointOne)
                    case 5: # verticalLine
                        startX = sizeXOneSquare * streetPiece[0] + sizeXOneSquare * 9 / 32 # top
                        startY = sizeYOneSquare * streetPiece[1]
                        endX = sizeXOneSquare * streetPiece[0] + sizeXOneSquare * 23 / 32
                        endY = sizeYOneSquare * streetPiece[1]
                        checkpointOne = (startX, startY, endX, endY)
                        if self.checkpoints[len(self.checkpoints) - 1] == checkpointOne: # bottom
                            startX = sizeXOneSquare * streetPiece[0] + sizeXOneSquare * 9 / 32
                            startY = sizeYOneSquare * (streetPiece[1] + 1)
                            endX = sizeXOneSquare * streetPiece[0] + sizeXOneSquare * 23 / 32
                            endY = sizeYOneSquare * (streetPiece[1] + 1)
                            self.checkpoints.append((startX, startY, endX, endY))
                        else:
                            self.checkpoints.append(checkpointOne)
                    case 6: # horizontalLine
                        startX = sizeXOneSquare * streetPiece[0] # left
                        startY = sizeYOneSquare * streetPiece[1] + sizeYOneSquare * 9 / 32
                        endX = sizeXOneSquare * streetPiece[0]
                        endY = sizeYOneSquare * streetPiece[1] + sizeYOneSquare * 23 / 32
                        checkpointOne = (startX, startY, endX, endY)
                        if self.checkpoints[len(self.checkpoints) - 1] == checkpointOne: # right
                            startX = sizeXOneSquare * (streetPiece[0] + 1)
                            startY = sizeYOneSquare * streetPiece[1] + sizeYOneSquare * 9 / 32
                            endX = sizeXOneSquare * (streetPiece[0] + 1)
                            endY = sizeYOneSquare * streetPiece[1] + sizeYOneSquare * 23 / 32
                            self.checkpoints.append((startX, startY, endX, endY))
                        else:
                            self.checkpoints.append(checkpointOne)

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


