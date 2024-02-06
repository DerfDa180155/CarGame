import random
import numpy as np
import array
import Ray


class Player:
    def __init__(self, x: int, y: int, direction: int):
        self.x = x
        self.y = y
        self.direction = direction
        self.maxSpeed = 150
        self.scaleWidth = 1600
        self.scaleHeight = 900
        self.scaleSizeWidth = 1600
        self.scaleSizeHeight = 900
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        self.frontRaysViewAngle = 90
        self.frontRaysDeg = 22.5
        self.frontRays = []

        i = self.frontRaysViewAngle / (-2)
        while i <= self.frontRaysViewAngle / 2:
            self.frontRays.append(Ray.Ray(self.x, self.y, self.direction + i))
            i += self.frontRaysDeg

    def move(self, moveDir: int):
        if moveDir == 0:
            checkMove = True

            for ray in self.frontRays:
                if ray.length <= 10:
                    checkMove = False

            if checkMove:
                # update coordinates based on direction and speed
                self.x += (self.maxSpeed / 100) * np.cos(np.deg2rad(self.direction))
                self.y += (self.maxSpeed / 100) * np.sin(np.deg2rad(self.direction))
        elif moveDir == 1:
            # update coordinates based on direction and speed
            self.x -= (self.maxSpeed / 200) * np.cos(np.deg2rad(self.direction))
            self.y -= (self.maxSpeed / 200) * np.sin(np.deg2rad(self.direction))

    def changeDir(self, direction: int):
        self.direction += direction

    def reset(self, x: int, y: int, direction: int):
        self.direction = direction
        self.x = x
        self.y = y

    def updateRays(self, bounds: array):
        for ray in self.frontRays:
            ray.calcLength(bounds)

    def update(self):
        # car physics




        # Rays update
        i = self.frontRaysViewAngle / (-2)
        for ray in self.frontRays:
            ray.updateRay(self.x, self.y, self.direction + i)
            i += self.frontRaysDeg




