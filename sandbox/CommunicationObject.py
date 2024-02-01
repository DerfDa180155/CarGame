import pygame
import random
import os
import numpy
import mapController
import array

class CommunicationObject:
    def __init__(self, gameStatus: str, FPSClock: pygame.time.Clock, TPSClock: pygame.time.Clock, FPS: int, TPS: int,
                 TextSize: int, imageArray: array, mapController: mapController, players: array, menuButtons: array,
                 gameModeButtons: array, mapButtons: array, currentMode: str):
        self.gameStatus = gameStatus
        self.FPSClock = FPSClock
        self.TPSClock = TPSClock
        self.FPS = FPS
        self.TPS = TPS
        self.TextSize = TextSize
        self.imageArray = imageArray
        self.mapController = mapController
        self.players = players
        self.menuButtons = menuButtons
        self.gameModeButtons = gameModeButtons
        self.mapButtons = mapButtons
        self.currentMode = currentMode


