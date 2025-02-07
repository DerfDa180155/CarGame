import random
import os
import numpy as np
import WaveFunctionCollapse
import MapCleaner
import RaceMap
import xml.etree.ElementTree as ET


class MapController:
    def __init__(self, WFC: WaveFunctionCollapse, MC: MapCleaner, mapPath: str, customMapPath: str):
        self.maps = []
        self.customMaps = []
        self.WFC = WFC
        self.MC = MC
        self.mapPath = mapPath
        self.customMapPath = customMapPath
        self.loadAllMaps()
        self.currentMapIndex = 0

        # variables for map generator
        self.mapGeneratorX = 5
        self.mapGeneratorY = 5

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
        self.customMaps = []
        currentPath = os.getcwd()
        mapsPath = os.path.join(currentPath, self.mapPath)
        customMapsPath = os.path.join(currentPath, self.customMapPath)
        # print(mapsPath)

        # main maps
        for root, dirs, files in os.walk(mapsPath):
            for file in sorted(files):
                if mapsPath == root:
                    print(root)
                    print(file)

                    docRoot = ET.parse(os.path.join(root, file)).getroot()
                    mapName = docRoot[0].text
                    playerStartX = float(docRoot[1].text)
                    playerStartY = float(docRoot[2].text)
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

        # custom maps
        newMap = RaceMap.RaceMap(myMap=[[4, 2], [3, 1]], name="currentGeneratedWFC", playerStartX=400, playerStartY=225, playerStartDirection=0)

        self.customMaps.append(newMap)
        print("Custom:")
        for root, dirs, files in os.walk(customMapsPath):
            for file in sorted(files):
                if customMapsPath == root:
                    print(root)
                    print(file)

                    docRoot = ET.parse(os.path.join(root, file)).getroot()
                    mapName = docRoot[0].text
                    playerStartX = float(docRoot[1].text)
                    playerStartY = float(docRoot[2].text)
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

                    self.customMaps.append(newMap)

    def addNewMap(self, path, mapName):
        # this function will get made in the future (maybe with a custom mapmaker)
        pass

    def generateNewMap(self, x: int, y: int, saveMap=False, setIndex=False, replaceOldMap=False):
        generateName = "currentGeneratedWFC"
        self.checkAndRemoveOldGenerated(generateName)

        mapArray = self.WFC.generate(x, y)
        checkEmpty = True
        while checkEmpty:
            for i in range(len(mapArray)):
                for j in range(len(mapArray[0])):
                    if mapArray[i][j] != 0:
                        checkEmpty = False
            if checkEmpty: # generate new one
                mapArray = self.WFC.generate(x, y)
                print("new map")

        mapArray = self.MC.cleanMap(mapArray)

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
        start = street[random.randint(0, len(street) - 1)]

        possibleDirections = []
        definition = self.mapDefinition[mapArray[start[0]][start[1]]]
        degArray = [270, 0, 90, 180]
        for i in range(len(definition)):
            if definition[i] == 1:
                possibleDirections.append((degArray[i]))

        startX = float(((1600 / len(mapArray)) * start[0]) + ((1600 / len(mapArray)) / 2))
        startY = float(((900 / len(mapArray[0])) * start[1]) + ((900 / len(mapArray[0])) / 2))
        startDirection = possibleDirections[random.randint(0, 1)]
        newMap = RaceMap.RaceMap(myMap=mapArray, name=generateName,
                                 playerStartX=startX, playerStartY=startY, playerStartDirection=startDirection)

        if saveMap:
            newMap.saveMap(self.mapPath)
        print(newMap.myMap)
        found = False
        if replaceOldMap:
            for i in range(len(self.customMaps)):
                if self.customMaps[i].name == generateName and not found:
                    self.customMaps[i] = newMap
                    found = True
                    if setIndex:
                        self.currentMapIndex = i
        if not found:
            self.customMaps.append(newMap)
            if setIndex:
                self.currentMapIndex = self.getCountMaps(False)-1
        return newMap

    def checkAndRemoveOldGenerated(self, name):
        index = 0
        for rMap in self.maps:
            if rMap.name == name:
                self.maps.pop(index)
            index += 1

    def getMapArray(self, useOfficialMaps: bool = True):
        if useOfficialMaps:
            return self.maps
        else:
            return self.customMaps

    def getCountMaps(self, useOfficialMaps: bool = True):
        if useOfficialMaps:
            return len(self.maps)
        else:
            return len(self.customMaps)

    def getCurrentMap(self, useOfficialMaps: bool = True):
        if useOfficialMaps:
            if len(self.maps) > 0:
                return self.maps[int(self.currentMapIndex)]
            return ""
        else:
            if len(self.customMaps) > 0:
                return self.customMaps[int(self.currentMapIndex)]
            return ""

    def getMapIndex(self, index: int, officialMaps: bool):
        if officialMaps:
            if index > self.getCountMaps()-1 or index <= 0:
                return self.maps[0]
            else:
                return self.maps[index]
        else:
            if index > self.getCountMaps()-1 or index <= 0:
                return self.customMaps[0]
            else:
                return self.customMaps[index]

    def getLastMap(self): # only for testing
        if len(self.maps) > 0:
            return self.maps[0].myMap
        if len(self.maps) >= 1:
            return self.maps[len(self.maps)-1].myMap
        return ""


