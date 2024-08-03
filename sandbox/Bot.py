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
        self.player.move(True) # for testing

        sum1 = self.player.frontRays[0].length
        sum1 += self.player.frontRays[1].length
        sum1 += self.player.frontRays[2].length
        sum1 += self.player.frontRays[3].length
        sum1 += self.player.frontRays[4].length

        sum2 = self.player.frontRays[6].length
        sum2 += self.player.frontRays[7].length
        sum2 += self.player.frontRays[8].length
        sum2 += self.player.frontRays[9].length
        sum2 += self.player.frontRays[10].length

        if np.abs(sum1 - sum2) > 50:
            self.player.changeDir(sum2 > sum1)
