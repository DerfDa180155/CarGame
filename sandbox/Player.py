import random
import numpy as np
import array
import Rey


class Player:
    def __init__(self, x: int, y: int, direction: int):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 300
        self.scaleWidth = 1600
        self.scaleHeight = 900
        self.scaleSizeWidth = 1600
        self.scaleSizeHeight = 900
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        self.frontReys = [Rey.Rey(self.x, self.y, self.direction - 45),
                          Rey.Rey(self.x, self.y, self.direction),
                          Rey.Rey(self.x, self.y, self.direction + 45)]

    def move(self, moveDir: int):
        if moveDir == 0:
            # update coordinates based on direction and speed
            self.x += (self.speed / 100) * np.cos(np.deg2rad(self.direction))
            self.y += (self.speed / 100) * np.sin(np.deg2rad(self.direction))
        elif moveDir == 1:
            # update coordinates based on direction and speed
            self.x -= (self.speed / 100) * np.cos(np.deg2rad(self.direction))
            self.y -= (self.speed / 100) * np.sin(np.deg2rad(self.direction))

    def changeDir(self, direction: int):
        self.direction += direction

    def reset(self, x: int, y: int, direction: int):
        self.direction = direction
        self.x = x
        self.y = y

    def update(self):
        # car physics




        # Reys update
        i = -45
        for rey in self.frontReys:
            rey.updateRey(self.x, self.y, self.direction + i)
            i += 45


    def updateReys(self, bounds: array):
        for rey in self.frontReys:
            rey.calcLength(bounds)

