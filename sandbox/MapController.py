import random
import os
import numpy as np
import WaveFunctionCollapse
import MapCleaner
import RaceMap
import xml.etree.ElementTree as ET


class MapController:
    def __init__(self, WFC: WaveFunctionCollapse, MC: MapCleaner, path: str):
        self.maps = []
        self.WFC = WFC
        self.MC = MC
        self.mapPath = path
        self.loadAllMaps()
        self.currentMapIndex = 0

        self.mapDefinition = [[0, 0, 0, 0],  # top, right, bottom, left
                              [1, 0, 0, 1],
                              [1, 1, 0, 0],
                              [0, 0, 1, 1],
                              [0, 1, 1, 0],
                              [1, 0, 1, 0],
                              [0, 1, 0, 1]]

    def loadAllMaps(self):
        # load all maps from the path into the maps array
        self.maps = []
        currentPath = os.getcwd()
        mapsPath = os.path.join(currentPath, self.mapPath)
        # print(mapsPath)

        for root, dirs, files in os.walk(mapsPath):
            for file in files:
                print(root)
                print(file)

                docRoot = ET.parse(os.path.join(root, file)).getroot()
                mapName = docRoot[0].text
                playerStartX = int(docRoot[1].text)
                playerStartY = int(docRoot[2].text)
                playerStartDirection = int(docRoot[3].text)
                mapSizeX = int(docRoot[4].text)
                mapSizeY = int(docRoot[5].text)

                myMap = []
                for i in range(0, mapSizeX):
                    temp = []
                    for j in range(0, mapSizeY):
                        temp.append(int(docRoot[6][i][j].text))
                    myMap.append(temp)
                print(myMap)

                newMap = RaceMap.RaceMap(myMap=myMap, name=mapName, playerStartX=playerStartX, playerStartY=playerStartY,
                                         playerStartDirection=playerStartDirection)

                self.maps.append(newMap)
        print(self.maps)

    def addNewMap(self, path, mapName):
        # this function will get made in the future (maybe with a custom mapmaker)
        pass

    def generateNewMap(self, x: int, y: int, saveMap=False, setIndex=False):
        generateName = "generatedWFC"
        self.checkAndRemoveOldGenerated(generateName)

        mapArray = self.MC.cleanMap(self.WFC.generate(x, y))

        found = False
        x = 0
        y = 0
        for i in range(len(mapArray)):
            for j in range(len(mapArray[0])):
                if mapArray[i][j] != 0 and not found:
                    x = i
                    y = j
                    found = True

        street = self.MC.getStreet(mapArray, x, y)
        start = street[random.randint(0, len(street))]

        possibleDirections = []
        definition = self.mapDefinition[mapArray[start[0]][start[1]]]
        degArray = [270, 0, 90, 180]
        for i in range(len(definition)):
            if definition[i] == 1:
                possibleDirections.append((degArray[i]))

        startX = ((1600 / len(mapArray)) * start[0]) + ((1600 / len(mapArray)) / 2)
        startY = ((900 / len(mapArray[0])) * start[1]) + ((900 / len(mapArray[0])) / 2)
        startDirection = possibleDirections[random.randint(0, 1)]
        newMap = RaceMap.RaceMap(myMap=mapArray, name=generateName,
                                 playerStartX=startX, playerStartY=startY, playerStartDirection=startDirection)

        if saveMap:
            newMap.saveMap(self.mapPath)
        print(newMap.myMap)
        self.maps.append(newMap)
        if setIndex:
            self.currentMapIndex = self.getCountMaps()-1
        return newMap

    def checkAndRemoveOldGenerated(self, name):
        index = 0
        for rMap in self.maps:
            if rMap.name == name:
                self.maps.pop(index)
            index += 1

    def getCountMaps(self):
        return len(self.maps)

    def getCurrentMap(self):
        if len(self.maps) > 0:
            return self.maps[int(self.currentMapIndex)]
        return ""

    def getLastMap(self): # only for testing
        if len(self.maps) > 0:
            return self.maps[0].myMap
        if len(self.maps) >= 1:
            return self.maps[len(self.maps)-1].myMap
        return ""


