import pygame
import random
import numpy as np
import array
import Player


class GodMode:
    def __init__(self, summonedPlayer: Player):
        self.itemName = "GodMode"
        self.summonedPlayer = summonedPlayer

        self.hitPlayers = []

        self.maxLiveTime = 120 * 10 # 10 seconds
        self.liveTime = self.maxLiveTime
        self.living = True

        self.summonedPlayer.godMode = True
        self.summonedPlayer.currentMaxSpeed = self.summonedPlayer.maxSpeed + 70

    def draw(self, surface):
        x = (self.summonedPlayer.x * surface.get_width()) / self.summonedPlayer.scaleWidth
        y = (self.summonedPlayer.y * surface.get_height()) / self.summonedPlayer.scaleHeight
        playerSizeWidth = (20 * surface.get_width()) / self.summonedPlayer.scaleSizeWidth
        playerSizeHeight = (20 * surface.get_height()) / self.summonedPlayer.scaleSizeHeight

        pygame.draw.circle(surface, (200, 150, 10), (x, y), playerSizeWidth, 0)

    def update(self):
        if self.liveTime <= 0:
            self.summonedPlayer.godMode = False
            self.summonedPlayer.currentMaxSpeed = self.summonedPlayer.maxSpeed
            self.living = False
        self.liveTime -= 1

    def resetCounter(self):
        self.liveTime = self.maxLiveTime

