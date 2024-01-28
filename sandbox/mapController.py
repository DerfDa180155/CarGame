import random
import os
import numpy as np
import WaveFunctionCollapse
import MapCleaner
import RaceMap
import xml.etree.ElementTree as ET


class mapController:
    def __init__(self, WFC: WaveFunctionCollapse, MC: MapCleaner, path: str):
        self.maps = []
        self.WFC = WFC
        self.MC = MC
        self.mapPath = path
        #self.loadAllMaps()
        self.currentMapIndex = 0

    def loadAllMaps(self):
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


        # load all maps from the path into the maps array
        pass

    def addNewMap(self, path, mapName):
        # this function will get made in the future (maybe with a custom mapmaker)
        pass

    def generateNewMap(self, x: int, y: int):
        newMap = RaceMap.RaceMap(myMap=self.MC.cleanMap(self.WFC.generate(x, y)), name="Unknown - " + str(random.randint(1000, 9999)))
        newMap.saveMap(self.mapPath)
        print(newMap.myMap)
        self.maps.append(newMap)
        return newMap

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


