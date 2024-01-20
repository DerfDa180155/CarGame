import numpy as np

class Player:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 300
        self.scaleWidth = 1600
        self.scaleHeight = 900
        self.scaleSizeWidth = 1600
        self.scaleSizeHeight = 900

    def move(self, moveDir):
        if moveDir == 0:
            # update coordinates based on direction and speed
            self.x += (self.speed / 100) * np.cos(np.deg2rad(self.direction))
            self.y += (self.speed / 100) * np.sin(np.deg2rad(self.direction))
        elif moveDir == 1:
            # update coordinates based on direction and speed
            self.x -= (self.speed / 100) * np.cos(np.deg2rad(self.direction))
            self.y -= (self.speed / 100) * np.sin(np.deg2rad(self.direction))

    def changeDir(self, direction):
        self.direction += direction

    def reset(self, x, y, direction):
        self.direction = direction
        self.x = x
        self.y = y


