import random
import os
import numpy as np
import WaveFunctionCollapse
import MapCleaner


class mapController:
    def __init__(self, WFC: WaveFunctionCollapse, MC: MapCleaner, path: str):
        self.maps = []
        self.WFC = WFC
        self.MC = MC
        self.mapPath = path
        self.loadAllMaps()

    def loadAllMaps(self):
        pass

    def addNewMap(self, path, mapName):
        pass

    def generateNewMap(self, x: int, y: int):
        self.maps.append(self.MC.cleanMap(self.WFC.generate(x, y)))




