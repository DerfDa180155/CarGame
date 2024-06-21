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

        self.maxLiveTime = 120 * 50 # 10 seconds
        self.liveTime = self.maxLiveTime
        self.living = True

        self.summonedPlayer.godMode = True
        self.summonedPlayer.currentMaxSpeed = self.summonedPlayer.maxSpeed + 70

    def draw(self, surface):
        pass # no draw function right now

    def update(self):
        if self.liveTime <= 0:
            self.summonedPlayer.godMode = False
            self.summonedPlayer.currentMaxSpeed = self.summonedPlayer.maxSpeed
            self.living = False
        self.liveTime -= 1

    def resetCounter(self):
        self.liveTime = self.maxLiveTime

