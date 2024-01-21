import pygame
import random
import os
import numpy


class CommunicationObject:
    def __init__(self, gameStatus, FPSClock, TPSClock, FPS, TPS, TextSize, imageArray, WFC, Player, menuButtons):
        self.gameStatus = gameStatus
        self.FPSClock = FPSClock
        self.TPSClock = TPSClock
        self.FPS = FPS
        self.TPS = TPS
        self.TextSize = TextSize
        self.imageArray = imageArray
        self.WFC = WFC
        self.Player = Player
        self.menuButtons = menuButtons


