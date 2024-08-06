import pygame
import random
import numpy as np
import array
import Player


class Bot:
    def __init__(self, player: Player):
        self.player = player
        self.player.frontRaysDeg = 9
        self.player.generateFrontRays()

    def reset(self, x: int, y: int, direction: int):
        self.player.reset(x, y, direction)

    def update(self):
        if self.player.isDone:
            return

        driveForward = True
        for ray in self.player.frontRays:
            if ray.length < 10:
                driveForward = False

        if self.player.frontRays[5].length > 50 and driveForward:
            self.player.move(True) # for testing
        else:
            driveForward = False
            self.player.move(False)

        sum1 = 0
        sum2 = 0

        for i in range(5):
            sum1 += self.player.frontRays[i].length
            sum2 += self.player.frontRays[i+6].length

        if np.abs(sum1 - sum2) > 50 and driveForward and self.player.speed > 0:
            self.player.changeDir(sum2 > sum1)

        if self.player.currentItem != -1:
            self.player.useItem()
