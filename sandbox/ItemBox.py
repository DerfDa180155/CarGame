import pygame
import random
import numpy as np
import array


class ItemBox:
    def __init__(self, x: int, y: int,):
        self.x = x
        self.y = y
        self.size = 25

    def draw(self, surface):
        newX = (self.x * surface.get_width()) / 1600
        newY = (self.y * surface.get_height()) / 900

        scaledSize = (self.size * surface.get_width()) / 2000
        pygame.draw.rect(surface, (0, 150, 200), pygame.Rect(newX, newY, scaledSize, scaledSize))

