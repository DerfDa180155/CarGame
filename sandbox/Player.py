import random
import numpy as np
import array
import Ray
import Rocket
import OilPuddle
import GodMode


class Player:
    def __init__(self, x: int, y: int, direction: int, id: int, summonedItems: array):
        self.x = x
        self.y = y
        self.direction = direction
        self.summonedItems = summonedItems

        self.scaleWidth = 1600
        self.scaleHeight = 900
        self.scaleSizeWidth = 1600
        self.scaleSizeHeight = 900

        #self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.selectedCarId = -1

        self.frontRaysViewAngle = 90
        self.frontRaysDeg = 22.5
        self.frontRays = []
        self.backRays = []
        self.nextCheckpointDirection = 0
        self.nextCheckpointLength = 0

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
        self.id = id

        self.currentItem = -1
        self.stunTime = 0
        self.shieldTime = 0
        self.godMode = False

        self.generateFrontRays()
        self.generateBackRays()

    def generateFrontRays(self):
        self.frontRays = []
        i = self.frontRaysViewAngle / (-2)
        while i <= self.frontRaysViewAngle / 2:
            self.frontRays.append(Ray.Ray(self.x, self.y, self.direction + i))
            i += self.frontRaysDeg

    def generateBackRays(self):
        self.backRays = []
        self.backRays.append(Ray.Ray(self.x, self.y, self.direction + 180))

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

        for playerRay in self.frontRays:
            playerRay.length = -1

        for playerRay in self.backRays:
            playerRay.length = -1

        self.currentItem = -1
        self.stunTime = 0
        self.shieldTime = 0
        self.godMode = False

        self.isDone = False  # for the race

    def updateRays(self, bounds: array):
        for ray in self.frontRays:
            ray.calcLength(bounds)
        for ray in self.backRays:
            ray.calcLength(bounds)

    def updatedNextCheckpointDirection(self, bound: array):
        newX = 0
        newY = 0
        # calculate middle point of the bound
        if bound[0] == bound[2]:
            newX = bound[0]
            newY = bound[3] + ((bound[1] - bound[3]) / 2)
        elif bound[1] == bound[3]:
            newY = bound[1]
            newX = bound[2] + ((bound[0] - bound[2]) / 2)

        deltaX = newX-self.x
        deltaY = newY-self.y
        self.nextCheckpointLength = np.sqrt(np.power(deltaX, 2) + np.power(deltaY, 2))
        self.nextCheckpointDirection = np.rad2deg(np.arctan(deltaY/deltaX))
        if deltaX < 0:
            self.nextCheckpointDirection += 180
        if self.nextCheckpointDirection < 0:
            self.nextCheckpointDirection += 360

    def move(self, forward: bool):
        self.isMoving = True
        if forward:
            self.acc += 1
        else:
            self.acc -= 1

    def changeDir(self, right: bool):
        changeDir = 0

        if self.speed != 0:
            if self.speed > 0:
                changeDir = 0.7
            else:
                changeDir = -0.7

        if right:
            self.direction += changeDir
            self.isSteeringRight = True
        else:
            self.direction -= changeDir
            self.isSteeringLeft = True

        if self.direction < 0:
            self.direction += 360
        elif self.direction > 360:
            self.direction -= 360

    def useItem(self):
        if self.currentItem == -1 or self.stunTime > 0:
            return

        match self.currentItem:
            case 0:
                # speed boost
                speedBootsValue = 50
                self.currentMaxSpeed += speedBootsValue
                self.speed += speedBootsValue
            case 1:
                # rocket
                item = Rocket.Rocket(self.x, self.y, self.direction, self)
                self.summonedItems.append(item)
            case 2:
                # multi rocket
                angle = 5
                i = self.direction - angle
                while i <= self.direction + angle:
                    item = Rocket.Rocket(self.x, self.y, i, self)
                    item.itemName = "MultiRocket"
                    self.summonedItems.append(item)
                    i += angle
            case 3:
                # shield
                self.shieldTime += 120 * 5 # 5 seconds
            case 4:
                # oil puddle
                item = OilPuddle.OilPuddle(self.x, self.y, self)
                self.summonedItems.append(item)
            case 5:
                # god mode
                checkExist = False
                for item in self.summonedItems:
                    if item.itemName == "GodMode" and item.summonedPlayer.id == self.id:
                        item.resetCounter()
                        checkExist = True

                if not checkExist:
                    item = GodMode.GodMode(self)
                    self.summonedItems.append(item)

        # remove Item
        self.currentItem = -1

    def itemHit(self, itemName):
        if not self.godMode:
            match itemName:
                case "Rocket":
                    if self.shieldTime > 0:
                        self.shieldTime = 0
                    else:
                        self.speed = 0
                        self.currentMaxSpeed = 0
                        if self.stunTime == 0:
                            self.stunTime = 120 * 3 # 3 seconds
                case "MultiRocket":
                    if self.shieldTime > 0:
                        self.shieldTime = 0
                    else:
                        self.speed = 0
                        self.currentMaxSpeed = 0
                        if self.stunTime == 0:
                            self.stunTime = int(120 * 1.5) # 1.5 seconds
                case "OilPuddle":
                    if self.shieldTime > 0:
                        self.shieldTime = 0
                    else:
                        self.speed = 0
                        self.currentMaxSpeed = 0
                        self.stunTime = 120 * 5
                case "GodMode":
                    self.shieldTime = 0
                    self.speed = 0
                    self.currentMaxSpeed = 0
                    self.stunTime = 120 * 3

    def update(self):
        if self.shieldTime > 0:
            self.shieldTime -= 1

        if self.stunTime > 0:
            self.stunTime -= 1
            return

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
        checkFrontMove = True
        for ray in self.frontRays:
            if ray.length <= 10:
                checkFrontMove = False
        checkBackMove = True
        for ray in self.backRays:
            if ray.length <= 10:
                checkBackMove = False
        moved = False

        if (checkFrontMove and self.speed > 0) or (checkBackMove and self.speed < 0) or (not checkFrontMove and not checkBackMove and self.speed >= 0):
            # update coordinates based on direction and speed
            self.x += (self.speed / 100) * np.cos(np.deg2rad(self.direction))
            self.y += (self.speed / 100) * np.sin(np.deg2rad(self.direction))
            moved = True
        else:
            self.speed = 0
            self.acc = 0

        # sliding
        if moved and self.speed > 0:
            if self.isSteeringRight and not self.isSteeringLeft and np.abs(self.speed) > 30:
                self.x -= (self.speed / 400) * np.cos(np.deg2rad(self.direction + 90))
                self.y -= (self.speed / 400) * np.sin(np.deg2rad(self.direction + 90))
                self.countSteering += 1
            elif self.isSteeringLeft and not self.isSteeringRight and np.abs(self.speed) > 30:
                self.x -= (self.speed / 400) * np.cos(np.deg2rad(self.direction - 90))
                self.y -= (self.speed / 400) * np.sin(np.deg2rad(self.direction - 90))
                self.countSteering += 1
            else:
                if self.countSteering > 30 and not self.godMode: # disabled in god mode
                    self.currentMaxSpeed += self.countSteering / 5
                    self.speed += self.countSteering / 5
                self.countSteering = 0
        else:
            self.countSteering = 0

        # more max speed after steering
        if not self.godMode: # disabled in god mode
            if self.currentMaxSpeed > self.maxSpeed:
                self.currentMaxSpeed -= 0.2
            elif self.currentMaxSpeed < self.maxSpeed:
                self.currentMaxSpeed = self.maxSpeed

        self.isSteeringRight = False
        self.isSteeringLeft = False

        # Rays update
        i = self.frontRaysViewAngle / (-2)
        for ray in self.frontRays:
            ray.updateRay(self.x, self.y, self.direction + i)
            i += self.frontRaysDeg
        self.backRays[0].updateRay(self.x, self.y, self.direction + 180)


