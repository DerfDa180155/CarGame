import pygame
import random
import numpy as np
import array


class ItemBox:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.size = 25
        self.cooldown = 0
        self.currentCooldown = 0

    def draw(self, surface):
        if self.currentCooldown == 0:
            newX = (self.x * surface.get_width()) / 1600
            newY = (self.y * surface.get_height()) / 900

            scaledSize = (self.size * surface.get_width()) / 2000
            pygame.draw.rect(surface, (0, 150, 200), pygame.Rect(newX - (scaledSize / 2), newY - (scaledSize / 2), scaledSize, scaledSize))

    def checkCollected(self, players):
        for player in players:
            x = player.x - self.x
            y = player.y - self.y
            distance = np.sqrt(np.power(x, 2) + np.power(y, 2))

            if distance <= self.size:
                self.currentCooldown = self.cooldown

    def update(self):
        if self.currentCooldown > 0:
            self.currentCooldown -= 1
