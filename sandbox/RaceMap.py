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
        self.boundsMap.append([0,0,1500,100])

        for i in range(len(self.myMap)):
            for j in range(len(self.myMap[0])):
                if self.myMap[i][j] != 0:
                    print(self.myMap[i][j])
                    # TODO add the lines for the bounds





