import pygame
import random
import numpy as np
import array
import Ray
import Player


class Rocket:
    def __init__(self, startX: int, startY: int, startDir: int, summonedPlayer: Player):
        self.x = startX
        self.y = startY
        self.startDir = startDir
        self.summonedPlayer = summonedPlayer

    def draw(self, surface):
        newX = (self.x * surface.get_width()) / 1600
        newY = (self.y * surface.get_height()) / 900
        size = (20 * surface.get_width()) / 2000
        pygame.draw.rect(surface, (70, 150, 70), pygame.Rect(newX - (size / 2), newY - (size / 2), size, size))

    def update(self):
        pass
