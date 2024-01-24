import pygame
import random
import os
import numpy
import mapController
import Player
import array

class CommunicationObject:
    def __init__(self, gameStatus: str, FPSClock: pygame.time.Clock, TPSClock: pygame.time.Clock, FPS: int, TPS: int, TextSize: int, imageArray: array, mapController: mapController, Player: Player, menuButtons: array):
        self.gameStatus = gameStatus
        self.FPSClock = FPSClock
        self.TPSClock = TPSClock
        self.FPS = FPS
        self.TPS = TPS
        self.TextSize = TextSize
        self.imageArray = imageArray
        self.mapController = mapController
        self.Player = Player
        self.menuButtons = menuButtons


