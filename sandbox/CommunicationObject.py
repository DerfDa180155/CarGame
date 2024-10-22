import pygame
import random
import os
import numpy
import MapController
import RaceObject
import Settings
import MapMaker
import array

class CommunicationObject:
    def __init__(self, gameStatus: str, FPSClock: pygame.time.Clock, TPSClock: pygame.time.Clock, #FPS: int, TPS: int,
                 TextSize: int, imageArray: array, mapController: MapController, carSkins: array, players: array, bots: array,
                 raceObject: RaceObject, settings: Settings, mapMaker: MapMaker, displayTempSettings: Settings,
                 waitForKey: bool, menuButtons: array, gameModeButtons: array, generateMapButtons: array,
                 carSelectorButtons: array, raceSettingsButtons: array, settingsButtons: array, mapMakerButtons: array,
                 leaderboardButtons: array, pauseButtons: array, mapButtons: array, mapButtonPage: int,
                 officialMaps: bool, currentMode: str, itemImageDictionary: array, summonedItems: array, itemBoxes: array):
        self.gameStatus = gameStatus
        self.FPSClock = FPSClock
        self.TPSClock = TPSClock
        #self.FPS = FPS
        #self.TPS = TPS
        self.TextSize = TextSize
        self.imageArray = imageArray
        self.mapController = mapController
        self.carSkins = carSkins
        self.players = players
        self.bots = bots
        self.raceObject = raceObject
        self.settings = settings
        self.mapMaker = mapMaker
        self.displayTempSettings = displayTempSettings
        self.waitForKey = waitForKey
        self.itemImageDictionary = itemImageDictionary
        self.summonedItems = summonedItems
        self.itemBoxes = itemBoxes

        # buttons
        self.menuButtons = menuButtons
        self.gameModeButtons = gameModeButtons
        self.generateMapButtons = generateMapButtons
        self.carSelectorButtons = carSelectorButtons
        self.raceSettingsButtons = raceSettingsButtons
        self.settingsButtons = settingsButtons
        self.mapMakerButtons = mapMakerButtons
        self.leaderboardButtons = leaderboardButtons
        self.pauseButtons = pauseButtons
        self.mapButtons = mapButtons
        self.mapButtonPage = mapButtonPage
        self.officialMaps = officialMaps


        self.currentMode = currentMode


