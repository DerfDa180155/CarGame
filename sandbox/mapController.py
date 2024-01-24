import random
import os
import numpy as np
import WaveFunctionCollapse
import MapCleaner
import RaceMap


class mapController:
    def __init__(self, WFC: WaveFunctionCollapse, MC: MapCleaner, path: str):
        self.maps = []
        self.WFC = WFC
        self.MC = MC
        self.mapPath = path
        self.loadAllMaps()

    def loadAllMaps(self):
        # load all maps from the path into the maps array
        pass

    def addNewMap(self, path, mapName):
        # this function will get made in the future (maybe with a custom mapmaker)
        pass

    def generateNewMap(self, x: int, y: int):
        newMap = RaceMap.RaceMap(myMap=self.MC.cleanMap(self.WFC.generate(x, y)))
        newMap.saveMap(self.mapPath)
        print(newMap.myMap)
        self.maps.append(newMap)
        return newMap

    def getLastMap(self):
        if len(self.maps) >= 1:
            return self.maps[len(self.maps)-1].myMap
        return ""


