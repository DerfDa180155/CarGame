import random
import numpy as np
import array
import Ray
import Player


class Rocket:
    def __init__(self, startX: int, startY: int, startDir: int, summonedPlayer: Player):
        self.startX = startX
        self.startY = startY
        self.startDir = startDir
        self.summonedPlayer = summonedPlayer

    def update(self):
        pass
