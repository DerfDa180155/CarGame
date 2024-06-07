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
        self.direction = startDir
        self.itemName = "Rocket"

        self.summonedPlayer = summonedPlayer
        self.speed = summonedPlayer.maxSpeed * 3

        self.rays = [Ray.Ray(self.x, self.y, self.direction)]

        self.living = True
        self.explode = False
        self.explodeRadius = 0

    def draw(self, surface):
        newX = (self.x * surface.get_width()) / 1600
        newY = (self.y * surface.get_height()) / 900
        if not self.explode:
            size = (20 * surface.get_width()) / 2000
            pygame.draw.rect(surface, (70, 150, 70), pygame.Rect(newX - (size / 2), newY - (size / 2), size, size))
        else:
            scaledRadius = ((self.explodeRadius + 10) * surface.get_width()) / 2000
            pygame.draw.circle(surface, (200, 150, 10), (newX, newY), scaledRadius, 0)

    def updateRays(self, bounds: array):
        for ray in self.rays:
            ray.calcLength(bounds)

    def update(self):
        for ray in self.rays:
            if ray.length <= 10 and ray.length >= 0:
                self.explode = True

        if not self.explode:
            self.x += (self.speed / 100) * np.cos(np.deg2rad(self.direction))
            self.y += (self.speed / 100) * np.sin(np.deg2rad(self.direction))

            for ray in self.rays:
                ray.updateRay(self.x, self.y, self.direction)

        else:
            self.explodeRadius += 0.5
            if self.explodeRadius >= 20:
                self.living = False
