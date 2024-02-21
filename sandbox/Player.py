import random
import numpy as np
import array
import Ray


class Player:
    def __init__(self, x: int, y: int, direction: int):
        self.x = x
        self.y = y
        self.direction = direction

        self.scaleWidth = 1600
        self.scaleHeight = 900
        self.scaleSizeWidth = 1600
        self.scaleSizeHeight = 900

        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        self.frontRaysViewAngle = 90
        self.frontRaysDeg = 22.5
        self.frontRays = []

        self.maxSpeed = 150
        self.currentMaxSpeed = self.maxSpeed
        self.maxAcc = 30
        self.speed = 0
        self.acc = 0
        self.isMoving = False
        self.isSteeringLeft = False
        self.isSteeringRight = False
        self.countSteering = 0

        self.isDone = False # for the race

        i = self.frontRaysViewAngle / (-2)
        while i <= self.frontRaysViewAngle / 2:
            self.frontRays.append(Ray.Ray(self.x, self.y, self.direction + i))
            i += self.frontRaysDeg

    def reset(self, x: int, y: int, direction: int):
        self.direction = direction
        self.x = x
        self.y = y
        self.speed = 0
        self.acc = 0
        self.isMoving = False
        self.isSteeringLeft = False
        self.isSteeringRight = False
        self.countSteering = 0
        self.currentMaxSpeed = self.maxSpeed

        self.isDone = False  # for the race

    def updateRays(self, bounds: array):
        for ray in self.frontRays:
            ray.calcLength(bounds)

    def move(self, forward: bool):
        self.isMoving = True
        if forward:
            self.acc += 1
        else:
            self.acc -= 1

    def changeDir(self, right: bool):
        changeDir = 0

        if self.speed != 0:
            changeDir = 0.7

        if right:
            self.direction += changeDir
            self.isSteeringRight = True
        else:
            self.direction -= changeDir
            self.isSteeringLeft = True

    def update(self):
        # car physics
        self.speed += self.acc * 0.05

        if not self.isMoving:
            if self.speed > 10:
                self.speed -= 0.5
            elif self.speed < -10:
                self.speed += 0.5
            else:
                self.speed = 0

            if self.acc > 0:
                self.acc -= 1
            elif self.acc < 0:
                self.acc += 1
        else:
            self.isMoving = False

        # speed limiter
        if self.speed < (-self.currentMaxSpeed / 2):
            self.speed = -self.currentMaxSpeed / 2
        elif self.speed > self.currentMaxSpeed:
            self.speed = self.currentMaxSpeed

        # acc limiter
        if self.acc < (-self.maxAcc / 1.5):
            self.acc = -self.maxAcc / 1.5
        elif self.acc > self.maxAcc:
            self.acc = self.maxAcc

        #print(self.speed)
        #print(self.acc)


        # bounds check
        checkMove = True
        for ray in self.frontRays:
            if ray.length <= 10:
                checkMove = False
        moved = False
        #checkMove = True
        if checkMove or (self.acc < 0):
            # update coordinates based on direction and speed
            self.x += (self.speed / 100) * np.cos(np.deg2rad(self.direction))
            self.y += (self.speed / 100) * np.sin(np.deg2rad(self.direction))
            moved = True
        else:
            self.speed = 0
            self.acc = 0

        # sliding
        if moved:
            if self.isSteeringRight and not self.isSteeringLeft and np.abs(self.speed) > 30:
                self.x -= (self.speed / 400) * np.cos(np.deg2rad(self.direction + 90))
                self.y -= (self.speed / 400) * np.sin(np.deg2rad(self.direction + 90))
                self.countSteering += 1
            elif self.isSteeringLeft and not self.isSteeringRight and np.abs(self.speed) > 30:
                self.x -= (self.speed / 400) * np.cos(np.deg2rad(self.direction - 90))
                self.y -= (self.speed / 400) * np.sin(np.deg2rad(self.direction - 90))
                self.countSteering += 1
            else:
                self.countSteering = 0
        else:
            self.countSteering = 0

        # more max speed after steering
        if self.countSteering > 30:
            self.currentMaxSpeed += 0.1
        elif self.currentMaxSpeed > self.maxSpeed:
            self.currentMaxSpeed -= 0.1
        elif self.currentMaxSpeed < self.maxSpeed:
            self.currentMaxSpeed = self.maxSpeed

        self.isSteeringRight = False
        self.isSteeringLeft = False

        # Rays update
        i = self.frontRaysViewAngle / (-2)
        for ray in self.frontRays:
            ray.updateRay(self.x, self.y, self.direction + i)
            i += self.frontRaysDeg




