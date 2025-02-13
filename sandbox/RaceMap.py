import pygame
import random
import os
import numpy
import array
import xml.etree.cElementTree as ET
import ItemBox


class RaceMap:
    def __init__(self, myMap: array, name: str = "Unknown", playerStartX: float = 0, playerStartY: float = 0, playerStartDirection: int = 0):
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

        self.startPositions = []
        self.generateStartPositions()

        self.itemBoxes = []
        self.generateItemBoxes()

    def saveMap(self, path: str, name: str = ""):
        root = ET.Element("raceMap")
        if name == "":
            ET.SubElement(root, "name").text = self.name
        else:
            ET.SubElement(root, "name").text = name
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

        if name == "":
            print(path + self.name + ".xml")
            ET.ElementTree(root).write(path + self.name + ".xml")
        else:
            print(path + name + ".xml")
            ET.ElementTree(root).write(path + name + ".xml")

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

    def getBoundsOnePiece(self, x, y, adjacentPieces = False):
        bounds = []

        sizeX = len(self.myMap)
        sizeY = len(self.myMap[0])

        sizeXOneSquare = 1600 / sizeX
        sizeYOneSquare = 900 / sizeY

        pieces = []
        pieces.append([x, y])

        if adjacentPieces:
            if x-1 >= 0:
                pieces.append([x-1, y])
            if x+1 < len(self.myMap):
                pieces.append([x+1, y])
            if y-1 >= 0:
                pieces.append([x, y-1])
            if y+1 < len(self.myMap[0]):
                pieces.append([x, y+1])

        for piece in pieces:
            x = piece[0]
            y = piece[1]
            match self.myMap[x][y]:
                case 1:  # topLeft
                    # top line horizontal
                    startX = sizeXOneSquare * x
                    startY = sizeYOneSquare * y + sizeYOneSquare * 9 / 32
                    endX = sizeXOneSquare * x + sizeXOneSquare * 9 / 32
                    endY = sizeYOneSquare * y + sizeYOneSquare * 9 / 32
                    bounds.append([startX, startY, endX, endY])

                    # bottom line horizontal
                    startX = sizeXOneSquare * x
                    startY = sizeYOneSquare * y + sizeYOneSquare * 23 / 32
                    endX = sizeXOneSquare * x + sizeXOneSquare * 23 / 32
                    endY = sizeYOneSquare * y + sizeYOneSquare * 23 / 32
                    bounds.append([startX, startY, endX, endY])

                    # left line vertical
                    startX = sizeXOneSquare * x + sizeXOneSquare * 9 / 32
                    startY = sizeYOneSquare * y
                    endX = sizeXOneSquare * x + sizeXOneSquare * 9 / 32
                    endY = sizeYOneSquare * y + sizeYOneSquare * 9 / 32
                    bounds.append([startX, startY, endX, endY])

                    # right line vertical
                    startX = sizeXOneSquare * x + sizeXOneSquare * 23 / 32
                    startY = sizeYOneSquare * y
                    endX = sizeXOneSquare * x + sizeXOneSquare * 23 / 32
                    endY = sizeYOneSquare * y + sizeYOneSquare * 23 / 32
                    bounds.append([startX, startY, endX, endY])
                case 2:  # topRight
                    # top line horizontal
                    startX = sizeXOneSquare * x + sizeXOneSquare * 23 / 32
                    startY = sizeYOneSquare * y + sizeYOneSquare * 9 / 32
                    endX = sizeXOneSquare * (x + 1)
                    endY = sizeYOneSquare * y + sizeYOneSquare * 9 / 32
                    bounds.append([startX, startY, endX, endY])

                    # bottom line horizontal
                    startX = sizeXOneSquare * x + sizeXOneSquare * 9 / 32
                    startY = sizeYOneSquare * y + sizeYOneSquare * 23 / 32
                    endX = sizeXOneSquare * (x + 1)
                    endY = sizeYOneSquare * y + sizeYOneSquare * 23 / 32
                    bounds.append([startX, startY, endX, endY])

                    # left line vertical
                    startX = sizeXOneSquare * x + sizeXOneSquare * 9 / 32
                    startY = sizeYOneSquare * y
                    endX = sizeXOneSquare * x + sizeXOneSquare * 9 / 32
                    endY = sizeYOneSquare * y + sizeYOneSquare * 23 / 32
                    bounds.append([startX, startY, endX, endY])

                    # right line vertical
                    startX = sizeXOneSquare * x + sizeXOneSquare * 23 / 32
                    startY = sizeYOneSquare * y
                    endX = sizeXOneSquare * x + sizeXOneSquare * 23 / 32
                    endY = sizeYOneSquare * y + sizeYOneSquare * 9 / 32
                    bounds.append([startX, startY, endX, endY])
                case 3:  # bottomLeft
                    # top line horizontal
                    startX = sizeXOneSquare * x
                    startY = sizeYOneSquare * y + sizeYOneSquare * 9 / 32
                    endX = sizeXOneSquare * x + sizeXOneSquare * 23 / 32
                    endY = sizeYOneSquare * y + sizeYOneSquare * 9 / 32
                    bounds.append([startX, startY, endX, endY])

                    # bottom line horizontal
                    startX = sizeXOneSquare * x
                    startY = sizeYOneSquare * y + sizeYOneSquare * 23 / 32
                    endX = sizeXOneSquare * x + sizeXOneSquare * 9 / 32
                    endY = sizeYOneSquare * y + sizeYOneSquare * 23 / 32
                    bounds.append([startX, startY, endX, endY])

                    # left line vertical
                    startX = sizeXOneSquare * x + sizeXOneSquare * 9 / 32
                    startY = sizeYOneSquare * y + sizeYOneSquare * 23 / 32
                    endX = sizeXOneSquare * x + sizeXOneSquare * 9 / 32
                    endY = sizeYOneSquare * (y + 1)
                    bounds.append([startX, startY, endX, endY])

                    # right line vertical
                    startX = sizeXOneSquare * x + sizeXOneSquare * 23 / 32
                    startY = sizeYOneSquare * y + sizeYOneSquare * 9 / 32
                    endX = sizeXOneSquare * x + sizeXOneSquare * 23 / 32
                    endY = sizeYOneSquare * (y + 1)
                    bounds.append([startX, startY, endX, endY])
                case 4:  # bottomRight
                    # top line horizontal
                    startX = sizeXOneSquare * x + sizeXOneSquare * 9 / 32
                    startY = sizeYOneSquare * y + sizeYOneSquare * 9 / 32
                    endX = sizeXOneSquare * (x + 1)
                    endY = sizeYOneSquare * y + sizeYOneSquare * 9 / 32
                    bounds.append([startX, startY, endX, endY])

                    # bottom line horizontal
                    startX = sizeXOneSquare * x + sizeXOneSquare * 23 / 32
                    startY = sizeYOneSquare * y + sizeYOneSquare * 23 / 32
                    endX = sizeXOneSquare * (x + 1)
                    endY = sizeYOneSquare * y + sizeYOneSquare * 23 / 32
                    bounds.append([startX, startY, endX, endY])

                    # left line vertical
                    startX = sizeXOneSquare * x + sizeXOneSquare * 9 / 32
                    startY = sizeYOneSquare * y + sizeYOneSquare * 9 / 32
                    endX = sizeXOneSquare * x + sizeXOneSquare * 9 / 32
                    endY = sizeYOneSquare * (y + 1)
                    bounds.append([startX, startY, endX, endY])

                    # right line vertical
                    startX = sizeXOneSquare * x + sizeXOneSquare * 23 / 32
                    startY = sizeYOneSquare * y + sizeYOneSquare * 23 / 32
                    endX = sizeXOneSquare * x + sizeXOneSquare * 23 / 32
                    endY = sizeYOneSquare * (y + 1)
                    bounds.append([startX, startY, endX, endY])
                case 5:  # verticalLine
                    # left line
                    startX = sizeXOneSquare * x + sizeXOneSquare * 9 / 32
                    startY = sizeYOneSquare * y
                    endX = sizeXOneSquare * x + sizeXOneSquare * 9 / 32
                    endY = sizeYOneSquare * (y + 1)
                    bounds.append([startX, startY, endX, endY])

                    # right line
                    startX = sizeXOneSquare * x + sizeXOneSquare * 23 / 32
                    endX = sizeXOneSquare * x + sizeXOneSquare * 23 / 32
                    bounds.append([startX, startY, endX, endY])
                case 6:  # horizontalLine
                    # top line
                    startX = sizeXOneSquare * x
                    startY = sizeYOneSquare * y + sizeYOneSquare * 9 / 32
                    endX = sizeXOneSquare * (x + 1)
                    endY = sizeYOneSquare * y + sizeYOneSquare * 9 / 32
                    bounds.append([startX, startY, endX, endY])

                    # bottom line
                    startY = sizeYOneSquare * y + sizeYOneSquare * 23 / 32
                    endY = sizeYOneSquare * y + sizeYOneSquare * 23 / 32
                    bounds.append([startX, startY, endX, endY])

        return bounds

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
                elif self.myMap[streetPiece[0]][streetPiece[1]] == 3: # bottom
                    #startX = sizeXOneSquare * streetPiece[0]
                    #startY = sizeYOneSquare * streetPiece[1] + sizeYOneSquare * 9 / 32
                    #endX = sizeXOneSquare * streetPiece[0]
                    #endY = sizeYOneSquare * streetPiece[1] + sizeYOneSquare * 23 / 32
                    startX = sizeXOneSquare * streetPiece[0] + sizeXOneSquare * 9 / 32
                    startY = sizeYOneSquare * (streetPiece[1] + 1)
                    endX = sizeXOneSquare * streetPiece[0] + sizeXOneSquare * 23 / 32
                    endY = sizeYOneSquare * (streetPiece[1] + 1)
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

        invert = False
        definition = self.mapDefinition[self.myMap[x][y]]

        # get raw angles
        angles = []
        if definition[0] == 1: # top
            angles.append([270 - 45, 270 + 45])
        if definition[1] == 1: # right
            angles.append([360 - 45, 0 + 45])
        if definition[2] == 1: # bottom
            angles.append([90 - 45, 90 + 45])
        if definition[3] == 1: # left
            angles.append([180 - 45, 180 + 45])

        # get all angles (0-360)
        complete = False
        if angles[0][1] > angles[1][0]:
            angles[1][0] += 360
        elif angles[1][1] > angles[0][0]:
            angles[0][0] += 360
        while not complete:
            if angles[0][0] > angles[1][1]:
                angles[0][0] -= 1
                angles[1][1] += 1
            elif angles[0][1] < angles[1][0]:
                angles[0][1] += 1
                angles[1][0] -= 1
            else:
                complete = True

        # check if checkpoints array need to be flipped
        if angles[0][0] > angles[0][1]:
            if self.playerStartDirection >= angles[0][0] or self.playerStartDirection <= angles[0][1]:
                invert = False
            else:
                invert = True
        if angles[1][0] > angles[1][1]:
            if self.playerStartDirection >= angles[1][0] or self.playerStartDirection <= angles[1][1]:
                invert = True
            else:
                invert = False

        if invert: # flip array
            tempCheckpoint = []
            for i in reversed(range(len(self.checkpoints))):
                tempCheckpoint.append(self.checkpoints[i])
            self.checkpoints = tempCheckpoint

    def generateStartPositions(self):
        self.startPositions = []

        sizeX = len(self.myMap)
        sizeY = len(self.myMap[0])

        sizeXOneSquare = 1600 / sizeX
        sizeYOneSquare = 900 / sizeY

        xOffset = sizeXOneSquare/10
        yOffset = sizeYOneSquare/10

        match self.playerStartDirection:
            case 0: # right
                for i in range(4):
                    temp = []
                    temp.append(self.playerStartX - (xOffset * i) + (xOffset*2))
                    temp.append(self.playerStartY - yOffset)
                    self.startPositions.append(temp)
                    temp = []
                    temp.append(self.playerStartX - (xOffset * (i + 0.5)) + (xOffset*2))
                    temp.append(self.playerStartY + yOffset)
                    self.startPositions.append(temp)
            case 90: # down
                for i in range(4):
                    temp = []
                    temp.append(self.playerStartX + xOffset)
                    temp.append(self.playerStartY - (yOffset * i) + (yOffset * 2))
                    self.startPositions.append(temp)
                    temp = []
                    temp.append(self.playerStartX - xOffset)
                    temp.append(self.playerStartY - (yOffset * (i + 0.5)) + (yOffset * 2))
                    self.startPositions.append(temp)
            case 180: # left
                for i in range(4):
                    temp = []
                    temp.append(self.playerStartX + (xOffset * i) - (xOffset * 2))
                    temp.append(self.playerStartY + yOffset)
                    self.startPositions.append(temp)
                    temp = []
                    temp.append(self.playerStartX + (xOffset * (i + 0.5)) - (xOffset * 2))
                    temp.append(self.playerStartY - yOffset)
                    self.startPositions.append(temp)
            case 270: # up
                for i in range(4):
                    temp = []
                    temp.append(self.playerStartX - xOffset)
                    temp.append(self.playerStartY + (yOffset * i) - (yOffset*2))
                    self.startPositions.append(temp)
                    temp = []
                    temp.append(self.playerStartX + xOffset)
                    temp.append(self.playerStartY + (yOffset * (i + 0.5)) - (yOffset*2))
                    self.startPositions.append(temp)
            case _: # default
                for i in range(8):
                    temp = []
                    temp.append(self.playerStartX)
                    temp.append(self.playerStartY)
                    self.startPositions.append(temp)

    def generateItemBoxes(self):
        self.itemBoxes = []

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
            if self.myMap[streetPiece[0]][streetPiece[1]] == 5:
                newX1 = int(((sizeXOneSquare * streetPiece[0]) + (sizeXOneSquare/2)) - ((sizeXOneSquare*1.5)/16))
                newX2 = int(((sizeXOneSquare * streetPiece[0]) + (sizeXOneSquare/2)) + ((sizeXOneSquare*1.5)/16))
                newY = int((sizeYOneSquare * streetPiece[1]) + (sizeYOneSquare/2))
                self.itemBoxes.append(ItemBox.ItemBox(newX1, newY))
                self.itemBoxes.append(ItemBox.ItemBox(newX2, newY))
            elif self.myMap[streetPiece[0]][streetPiece[1]] == 6:
                newX = int((sizeXOneSquare * streetPiece[0]) + (sizeXOneSquare / 2))
                newY1 = int(((sizeYOneSquare * streetPiece[1]) + (sizeYOneSquare / 2)) - ((sizeYOneSquare*1.5)/16))
                newY2 = int(((sizeYOneSquare * streetPiece[1]) + (sizeYOneSquare / 2)) + ((sizeYOneSquare*1.5)/16))
                self.itemBoxes.append(ItemBox.ItemBox(newX, newY1))
                self.itemBoxes.append(ItemBox.ItemBox(newX, newY2))
            else:
                newX = int((sizeXOneSquare * streetPiece[0]) + (sizeXOneSquare / 2))
                newY = int((sizeYOneSquare * streetPiece[1]) + (sizeYOneSquare / 2))
                self.itemBoxes.append(ItemBox.ItemBox(newX, newY))

    def getStreet(self, myMap, x: int, y: int):
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


