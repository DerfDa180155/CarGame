import pygame
import random
import os
import numpy
import MapController
import RaceObject
import Settings
import array

class CommunicationObject:
    def __init__(self, gameStatus: str, FPSClock: pygame.time.Clock, TPSClock: pygame.time.Clock, FPS: int, TPS: int,
                 TextSize: int, imageArray: array, mapController: MapController, players: array, raceObject: RaceObject,
                 settings: Settings, menuButtons: array, gameModeButtons: array, raceSettingsButtons: array,
                 settingsButtons: array, leaderboardButtons: array, pauseButtons: array, mapButtons: array,
                 mapButtonPage: int, officialMaps: bool, currentMode: str):
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
        self.settings = settings

        self.menuButtons = menuButtons
        self.gameModeButtons = gameModeButtons
        self.raceSettingsButtons = raceSettingsButtons
        self.settingsButtons = settingsButtons
        self.leaderboardButtons = leaderboardButtons
        self.pauseButtons = pauseButtons
        self.mapButtons = mapButtons
        self.mapButtonPage = mapButtonPage
        self.officialMaps = officialMaps


        self.currentMode = currentMode


