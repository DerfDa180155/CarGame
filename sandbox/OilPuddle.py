import pygame
import random
import numpy as np
import array
import Player


class OilPuddle:
    def __init__(self, x: int, y: int, summonedPlayer: Player):
        self.x = x
        self.y = y
        self.size = 30
        self.itemName = "OilPuddle"

        self.summonedPlayer = summonedPlayer

        self.hitPlayers = []

        self.liveTime = 120 * 10 # 10 seconds
        self.living = True

    def draw(self, surface):
        newX = (self.x * surface.get_width()) / 1600
        newY = (self.y * surface.get_height()) / 900

        scaledRadius = ((self.size) * surface.get_width()) / 2000
        pygame.draw.circle(surface, (10, 10, 30), (newX, newY), scaledRadius, 0)

    def update(self):
        if self.liveTime <= 0:
            self.living = False
        self.liveTime -= 1

