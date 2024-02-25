import pygame
import random
import os
import numpy
import MapController
import RaceObject
import array

class CommunicationObject:
    def __init__(self, gameStatus: str, FPSClock: pygame.time.Clock, TPSClock: pygame.time.Clock, FPS: int, TPS: int,
                 TextSize: int, imageArray: array, mapController: MapController, players: array, raceObject: RaceObject,
                 menuButtons: array, gameModeButtons: array, mapButtons: array, raceSettingsButtons: array,
                 leaderboardButtons: array, pauseButtons: array, currentMode: str):
        self.gameStatus = gameStatus
        self.FPSClock = FPSClock
        self.TPSClock = TPSClock
        self.FPS = FPS
        self.TPS = TPS
        self.TextSize = TextSize
        self.imageArray = imageArray
        self.mapController = mapController
        self.players = players
        self.raceObject = raceObject
        self.menuButtons = menuButtons
        self.gameModeButtons = gameModeButtons
        self.mapButtons = mapButtons
        self.raceSettingsButtons = raceSettingsButtons
        self.leaderboardButtons = leaderboardButtons
        self.pauseButtons = pauseButtons
        self.currentMode = currentMode


