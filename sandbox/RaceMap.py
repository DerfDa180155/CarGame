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

        self.boundsMap = []
        self.generateLineMap()


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






