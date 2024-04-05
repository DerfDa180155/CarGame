import pygame
import random
import os
import threading
import time
import numpy
import datetime
import CommunicationObject
import GameDisplay
import Settings
import WaveFunctionCollapse
import MapCleaner
import Player
import RaceObject
import Button
import webbrowser
import MapController

class GameMain:
    def __init__(self):
        pygame.init()
        pygame.display.init()

        pygame.display.gl_set_attribute(pygame.GL_ACCELERATED_VISUAL, 0)
        pygame.display.gl_set_attribute(pygame.GL_DOUBLEBUFFER, 1)

        self.running = True
        self.windowWidth = 1280
        self.windowHeight = 720

        # FPS and TPS for the game
        self.FPS = 144
        self.TPS = 120

        self.screen = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.RESIZABLE | pygame.GL_DOUBLEBUFFER)
        pygame.display.set_caption("Car Game by David Derflinger")

        # clocks
        self.TPSClock = pygame.time.Clock()
        self.FPSClock = pygame.time.Clock()

        # paths for different game files (images, maps, settings, ...)
        self.mapPath = "gameFiles/maps/"
        self.customMapPath = "gameFiles/maps/customMaps/"
        self.imagePath = "gameFiles/images/"
        self.settingsPath = "gameFiles/settings/"

        # images
        self.empty = pygame.image.load(self.imagePath + "empty.png").convert()
        self.bottomLeft = pygame.image.load(self.imagePath + "bottom_Left.png").convert()
        self.bottomRight = pygame.image.load(self.imagePath + "bottom_Right.png").convert()
        self.topLeft = pygame.image.load(self.imagePath + "top_Left.png").convert()
        self.topRight = pygame.image.load(self.imagePath + "top_Right.png").convert()
        self.verticalLine = pygame.image.load(self.imagePath + "vertical_Line.png").convert()
        self.horizontalLine = pygame.image.load(self.imagePath + "horizontal_line.png").convert()
        self.crossing = pygame.image.load(self.imagePath + "crossing.png").convert()
        self.settingsImg = pygame.image.load(self.imagePath + "settings.png").convert()

        self.mapArray = [self.empty, self.topLeft, self.topRight, self.bottomLeft, self.bottomRight, self.verticalLine, self.horizontalLine]
        self.mapArrayDefinition = [[0, 0, 0, 0], # top, right, bottom, left
                                   [1, 0, 0, 1],
                                   [1, 1, 0, 0],
                                   [0, 0, 1, 1],
                                   [0, 1, 1, 0],
                                   [1, 0, 1, 0],
                                   [0, 1, 0, 1]]
                                   #[1, 1, 1, 1]]

        self.WFC = WaveFunctionCollapse.WaveFunctionCollapse(self.mapArray, self.mapArrayDefinition)
        self.mapCleaner = MapCleaner.MapCleaner(self.mapArrayDefinition)
        self.mapController = MapController.MapController(WFC=self.WFC, MC=self.mapCleaner, mapPath=self.mapPath, customMapPath=self.customMapPath)
        #self.mapController.loadAllMaps() # load all saved maps
        self.oldMapCount = self.mapController.getCountMaps(True)
        self.oldCustomMapCount = self.mapController.getCountMaps(False)

        self.players = []
        self.players.append(Player.Player(100, 100, 0))

        self.raceObject = RaceObject.RaceObject(players=self.players, raceMap=self.mapController.maps[0])
        self.settings = Settings.Settings(self.settingsPath)

        # buttons
        # main menu buttons
        self.testButton = Button.Button(self.screen, 100, 100, 150, self.crossing, "generateMap")
        self.modeSelectButton = Button.Button(self.screen, 100, 300, 150, self.topRight, "selectMode")
        self.mapSelectButton = Button.Button(self.screen, 100, 500, 150, self.topLeft, "selectMap")
        self.settingsButton = Button.Button(self.screen, 1460, 40, 100, self.settingsImg, "settings")
        self.linkButton = Button.Button(self.screen, 1450, 750, 100, self.empty, "https://github.com/DerfDa180155")
        self.quitButton = Button.Button(self.screen, 100, 700, 150, self.empty, "quit")
        self.menuButtons = [self.testButton, self.modeSelectButton, self.mapSelectButton, self.settingsButton,
                            self.linkButton, self.quitButton]

        # game mode buttons
        self.singlePlayerButton = Button.Button(self.screen, 100, 100, 150, self.horizontalLine, "singleplayer")
        self.multiPlayerButton = Button.Button(self.screen, 100, 300, 150, self.crossing, "multiplayer")
        self.gameModeButtons = [self.singlePlayerButton, self.multiPlayerButton]

        # race settings buttons
        self.startRaceButtons = Button.Button(self.screen, 750, 720, 150, self.horizontalLine, "start")
        self.backButton = Button.Button(self.screen, 50, 770, 100, self.crossing, "back")
        self.roundsScrollButton = Button.Button(self.screen, 710, 100, 45, self.verticalLine, "scrollRounds")
        self.maxSpeedScrollButton = Button.Button(self.screen, 710, 100, 45, self.verticalLine, "scrollMaxSpeed")
        self.maxAccScrollButton = Button.Button(self.screen, 710, 100, 45, self.verticalLine, "scrollMaxAcc")
        self.itemsEnabledScrollButton = Button.Button(self.screen, 710, 100, 45, self.verticalLine, "scrollItemsEnabled")
        self.itemsSpawnCooldownScrollButton = Button.Button(self.screen, 710, 100, 45, self.verticalLine, "scrollISC")
        self.raceSettingsButtons = [self.startRaceButtons, self.backButton, self.roundsScrollButton, self.maxSpeedScrollButton, self.maxAccScrollButton, self.itemsEnabledScrollButton, self.itemsSpawnCooldownScrollButton]

        # settings buttons
        self.forwardKeyButtons = Button.Button(self.screen, 710, 100, 45, self.verticalLine, "forwardKey")
        self.backwardKeyButtons = Button.Button(self.screen, 710, 100, 45, self.verticalLine, "backwardKey")
        self.leftKeyButtons = Button.Button(self.screen, 710, 100, 45, self.verticalLine, "leftKey")
        self.rightKeyButtons = Button.Button(self.screen, 710, 100, 45, self.verticalLine, "rightKey")
        self.pauseKeyButtons = Button.Button(self.screen, 710, 100, 45, self.verticalLine, "pauseKey")
        self.settingsButtons = [self.forwardKeyButtons, self.backwardKeyButtons, self.leftKeyButtons, self.rightKeyButtons, self.pauseKeyButtons]

        # leaderboard buttons
        self.choseMap = Button.Button(self.screen, 675, 625, 50, self.topLeft, "choseMap")
        self.restartButton = Button.Button(self.screen, 875, 625, 50, self.topRight, "restart")
        self.saveButton = Button.Button(self.screen, 775, 575, 50, self.crossing, "saveMap")
        self.leaderboardButtons = [self.choseMap, self.restartButton, self.saveButton]

        # pause buttons
        self.mainMenu = Button.Button(self.screen, 650, 625, 50, self.topLeft, "mainMenu")
        self.restartButton = Button.Button(self.screen, 775, 625, 50, self.topRight, "restart")
        self.resumeButton = Button.Button(self.screen, 900, 625, 50, self.topRight, "resume")
        self.pauseButtons = [self.mainMenu, self.restartButton, self.resumeButton]

        self.mapButtons = []
        self.imageMapSize = 200
        #self.locations = [[100, 100], [400, 100], [700, 100], [1000, 100], [1300, 100],
        #                  [100, 400], [400, 400], [700, 400], [1000, 400], [1300, 400],
        #                  [100, 700], [400, 700], [700, 700], [1000, 700], [1300, 700]]
        self.locations = [[100, 100], [400, 100], [700, 100], [1000, 100], [1300, 100],
                          [100, 380], [400, 380], [700, 380], [1000, 380], [1300, 380],
                          [100, 660], [400, 660], [700, 660], [1000, 660], [1300, 660]]
        # official maps
        tempArray = []
        for i in range(self.oldMapCount):
            tempArray.append(Button.Button(self.screen, self.locations[i % 15][0], self.locations[i % 15][1], self.imageMapSize, self.empty, str(i)))
            if i >= 15:
                tempArray[len(self.mapButtons)-1].enable = False
        self.mapButtons.append(tempArray)
        # custom maps
        tempArray = []
        for i in range(self.oldCustomMapCount):
            tempArray.append(Button.Button(self.screen, self.locations[i % 15][0], self.locations[i % 15][1], self.imageMapSize, self.empty, str(i)))
            if i >= 15:
                tempArray[len(self.mapButtons)-1].enable = False
        self.mapButtons.append(tempArray)
        self.mapButtons[0].append(Button.Button(self.screen, 750, 750, 100, self.crossing, "generateMapWFC"))
        tempArray = []
        tempArray.append(Button.Button(self.screen, 75, 800, 50, self.crossing, "previousPage"))
        tempArray.append(Button.Button(self.screen, 1475, 800, 50, self.crossing, "nextPage"))
        self.mapButtons.append(tempArray)
        self.mapButtonPage = 0

        self.CO = CommunicationObject.CommunicationObject(gameStatus="menu", FPSClock=self.FPSClock,
                                                          TPSClock=self.TPSClock, FPS=self.FPS, TPS=self.TPS,
                                                          TextSize=30, imageArray=self.mapArray,
                                                          mapController=self.mapController, players=self.players,
                                                          raceObject=self.raceObject, settings=self.settings,
                                                          menuButtons=self.menuButtons, gameModeButtons=self.gameModeButtons,
                                                          raceSettingsButtons=self.raceSettingsButtons,
                                                          leaderboardButtons=self.leaderboardButtons,
                                                          settingsButtons=self.settingsButtons,
                                                          pauseButtons=self.pauseButtons, mapButtons=self.mapButtons,
                                                          mapButtonPage=self.mapButtonPage, officialMaps=True,
                                                          currentMode="singleplayer")

        self.gameDisplay = GameDisplay.GameDisplay(screen=self.screen, CO=self.CO)
        self.gameDisplay.start()

        self.run()

    def run(self):
        # pygame setup
        while self.running:
            scrolledUp = False
            scrolledDown = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    scrolledUp = (event.button == 4)
                    scrolledDown = (event.button == 5)
                elif event.type == pygame.QUIT: # Quit the Game
                    self.running = False
                    self.gameDisplay.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.key.key_code(self.CO.settings.pauseKey): # Quit the Game
                        if self.CO.gameStatus == "menu":
                            self.running = False
                            self.gameDisplay.running = False
                        elif self.CO.gameStatus == "generateMap": # only for testing
                            self.CO.gameStatus = "menu"
                        elif self.CO.gameStatus == "selectMode" or self.CO.gameStatus == "settings":
                            self.CO.gameStatus = "menu"
                        elif self.CO.gameStatus == "selectMap":
                            self.CO.gameStatus = "selectMode"
                        elif self.CO.gameStatus == "raceSettings":
                            self.CO.gameStatus = "selectMap"
                        elif self.CO.gameStatus == "race":
                            #self.CO.gameStatus = "selectMap"
                            self.CO.raceObject.togglePause()
                    elif event.key == pygame.K_m: # switch status (only for testing)
                        if self.CO.gameStatus == "menu":
                            self.CO.gameStatus = "generateMap"
                        elif self.CO.gameStatus == "generateMap":
                            self.CO.gameStatus = "menu"
                    elif event.key == pygame.K_k and self.CO.gameStatus == "generateMap":
                        x = 4
                        y = x

                        testMap = self.CO.mapController.generateNewMap(x, y)
                        print("Name: " + testMap.name + "\nMap: " + str(testMap.myMap))
                        self.CO.players[0].reset(x=testMap.playerStartX, y=testMap.playerStartY, direction=testMap.playerStartDirection)

            # get pressed Keys
            keys = pygame.key.get_pressed()
            mx, my = pygame.mouse.get_pos() # get mouse positions for the buttons

            match self.CO.gameStatus:
                case "menu":
                    for button in self.CO.menuButtons:
                        if button.clicked(mx, my, pygame.mouse.get_pressed()):
                            if "https://" in button.action:
                                if not button.hadAction:
                                    button.hadAction = True
                                    webbrowser.open(button.action)
                            elif "quit" in button.action: # quit the game
                                self.running = False
                                self.gameDisplay.running = False
                            else:
                                self.CO.gameStatus = button.action
                case "settings":
                    # hotkeys for debugging and testing
                    if keys[pygame.K_s]:
                        self.CO.settings.saveSettings()
                        time.sleep(0.3)

                    for button in self.CO.settingsButtons:
                        if button.clicked(mx, my, pygame.mouse.get_pressed()):
                            print(button.action)
                            text = ""
                            while text == "":
                                for detect in pygame.event.get():
                                    if detect.type == pygame.KEYDOWN:
                                        text = detect.key
                            match button.action:
                                case "forwardKey":
                                    self.CO.settings.driveForwardKey = pygame.key.name(text)
                                case "backwardKey":
                                    self.CO.settings.driveBackwardKey = pygame.key.name(text)
                                case "leftKey":
                                    self.CO.settings.steerLeftKey = pygame.key.name(text)
                                case "rightKey":
                                    self.CO.settings.steerRightKey = pygame.key.name(text)
                                case "pauseKey":
                                    self.CO.settings.pauseKey = pygame.key.name(text)
                case "selectMode":
                    for button in self.CO.gameModeButtons:
                        if button.clicked(mx, my, pygame.mouse.get_pressed()):
                            self.CO.currentMode = button.action
                            self.CO.raceObject.mode = button.action
                            if button.action == "singleplayer" and len(self.CO.players) == 2:
                                self.CO.players.pop(1)
                            elif button.action == "multiplayer" and len(self.CO.players) == 1:
                                self.CO.players.append(Player.Player(0, 0, 0))
                            self.CO.gameStatus = "selectMap"
                            print(self.CO.currentMode)
                            self.CO.mapButtonPage = 0
                case "selectMap":
                    if self.oldMapCount != self.CO.mapController.getCountMaps(True):
                        self.oldMapCount = self.CO.mapController.getCountMaps(True)
                        self.mapButtons = []
                        for i in range(self.oldMapCount):
                            self.mapButtons.append(
                                Button.Button(self.screen, self.locations[i][0], self.locations[i][1], self.imageMapSize, self.empty, str(i)))


                    maxPageOfficialMaps = int((len(self.CO.mapButtons[0])/15)+0.5)
                    maxPageCustomMaps = int((len(self.CO.mapButtons[1])/15)+0.5)
                    maxPage = maxPageOfficialMaps + maxPageCustomMaps
                    if self.CO.mapButtonPage >= maxPageOfficialMaps:
                        index = 1
                        self.CO.officialMaps = False
                    else:
                        index = 0
                        self.CO.officialMaps = True

                    if index == 0:
                        count = 0
                        for button in self.CO.mapButtons[0]:
                            if button.action == str(count): # only toggle the map buttons
                                button.enable = self.CO.mapButtonPage * 15 <= count <= (self.CO.mapButtonPage + 1) * 15
                                count += 1
                            elif button.action == "generateMapWFC":
                                button.enable = True
                        for button in self.CO.mapButtons[1]:
                            button.enable = False
                    elif index == 1: # custom maps
                        for button in self.CO.mapButtons[0]:
                            button.enable = False
                        count = 0
                        for button in self.CO.mapButtons[1]:
                            if button.action == str(count):  # only toggle the map buttons
                                button.enable = (self.CO.mapButtonPage-maxPageOfficialMaps) * 15 <= count <= ((self.CO.mapButtonPage-maxPageOfficialMaps) + 1) * 15
                                count += 1

                    # hotkeys for debugging and testing
                    if keys[pygame.K_j]:
                        if self.CO.mapButtonPage != 0:
                            self.CO.mapButtonPage -= 1
                            print(self.CO.mapButtonPage)
                            time.sleep(0.3)
                    elif keys[pygame.K_k]:
                        if self.CO.mapButtonPage < maxPage:
                            self.CO.mapButtonPage += 1
                            print(self.CO.mapButtonPage)
                            time.sleep(0.3)

                    for button in self.CO.mapButtons[index] + self.CO.mapButtons[2]:
                        if button.clicked(mx, my, pygame.mouse.get_pressed()):
                            if not button.action.isnumeric():
                                if button.action == "generateMapWFC":
                                    self.CO.mapController.generateNewMap(random.randint(2, 6), random.randint(2, 6), False, True)
                                    self.CO.gameStatus = "raceSettings"
                                    self.CO.raceObject.reset()
                                    if self.CO.mapButtonPage != 0:
                                        self.CO.mapButtonPage -= 1
                                        print(self.CO.mapButtonPage)
                                elif button.action == "previousPage":
                                    if self.CO.mapButtonPage != 0:
                                        self.CO.mapButtonPage -= 1
                                        print(self.CO.mapButtonPage)
                                elif button.action == "nextPage":
                                    if self.CO.mapButtonPage < maxPage:
                                        self.CO.mapButtonPage += 1
                                        print(self.CO.mapButtonPage)
                            else:
                                self.CO.mapController.currentMapIndex = button.action
                                print(button.action)
                                for player in self.CO.players:
                                    player.reset(x=self.CO.mapController.getCurrentMap(self.CO.officialMaps).playerStartX,
                                                 y=self.CO.mapController.getCurrentMap(self.CO.officialMaps).playerStartY,
                                                 direction=self.CO.mapController.getCurrentMap(self.CO.officialMaps).playerStartDirection)
                                self.CO.gameStatus = "raceSettings"
                                self.CO.raceObject.reset()
                case "raceSettings":
                    for button in self.CO.raceSettingsButtons:
                        if button.clicked(mx, my, pygame.mouse.get_pressed()):
                            if button.action == "start":
                                if self.CO.raceObject.rounds > 0:
                                    self.CO.gameStatus = "race"
                                    self.CO.raceObject.start(self.CO.mapController.getCurrentMap(self.CO.officialMaps))
                            elif button.action == "back":
                                self.CO.gameStatus = "selectMap"
                        if button.hover(mx, my):
                            match button.action:
                                case "scrollRounds":
                                    if scrolledUp:
                                        self.CO.raceObject.rounds += 1
                                    elif scrolledDown:
                                        self.CO.raceObject.rounds -= 1
                                        if self.CO.raceObject.rounds < 0:
                                            self.CO.raceObject.rounds = 0
                                case "scrollMaxSpeed":
                                    if scrolledUp:
                                        self.CO.raceObject.maxSpeed += 1
                                    elif scrolledDown:
                                        self.CO.raceObject.maxSpeed -= 1
                                        if self.CO.raceObject.maxSpeed < 0:
                                            self.CO.raceObject.maxSpeed = 0
                                case "scrollMaxAcc":
                                    if scrolledUp:
                                        self.CO.raceObject.maxAcc += 1
                                    elif scrolledDown:
                                        self.CO.raceObject.maxAcc -= 1
                                        if self.CO.raceObject.maxAcc < 0:
                                            self.CO.raceObject.maxAcc = 0
                                case "scrollItemsEnabled":
                                    if scrolledUp:
                                        self.CO.raceObject.itemsEnabled = True
                                    elif scrolledDown:
                                        self.CO.raceObject.itemsEnabled = False
                                case "scrollISC":
                                    if scrolledUp:
                                        self.CO.raceObject.itemSpawnCooldown += 1
                                    elif scrolledDown:
                                        self.CO.raceObject.itemSpawnCooldown -= 1
                                        if self.CO.raceObject.itemSpawnCooldown < 0:
                                            self.CO.raceObject.itemSpawnCooldown = 0

                case "race":
                    # update raceObject
                    self.CO.raceObject.update()

                    if keys[pygame.K_t]:
                        self.CO.raceObject.rounds = 1
                        self.CO.raceObject.start(self.CO.mapController.getCurrentMap(self.CO.officialMaps))
                    elif keys[pygame.K_z]:
                        self.CO.raceObject.stop()
                    elif keys[pygame.K_u]:
                        self.CO.raceObject.resume()
                    elif keys[pygame.K_i]:
                        self.CO.raceObject.reset()

                    if self.CO.mapController.getCurrentMap(self.CO.officialMaps).name == "generatedWFC":
                        if keys[pygame.K_o]: # save custom map
                            self.CO.mapController.getCurrentMap(self.CO.officialMaps).saveMap(self.customMapPath)

                    if self.CO.raceObject.raceStatus == "race":
                        # movement keys pressed --> Update players
                        if self.CO.currentMode == "singleplayer" and not self.CO.players[0].isDone:
                            if keys[pygame.key.key_code(self.CO.settings.steerLeftKey)]: # turn left
                                self.CO.players[0].changeDir(False)
                            if keys[pygame.key.key_code(self.CO.settings.steerRightKey)]: # turn right
                                self.CO.players[0].changeDir(True)
                            if keys[pygame.key.key_code(self.CO.settings.driveForwardKey)]: # move forward
                                self.CO.players[0].move(True)
                            if keys[pygame.key.key_code(self.CO.settings.driveBackwardKey)]: # move backward
                                self.CO.players[0].move(False)
                        elif self.CO.currentMode == "multiplayer":
                            i = 0
                            for player in self.CO.players:
                                if not player.isDone:
                                    if keys[pygame.K_LEFT] and i == 1 or keys[pygame.K_a] and i == 0: # turn left
                                        player.changeDir(False)
                                    if keys[pygame.K_RIGHT] and i == 1 or keys[pygame.K_d] and i == 0: # turn right
                                        player.changeDir(True)
                                    if keys[pygame.K_UP] and i == 1 or keys[pygame.K_w] and i == 0: # move forward
                                        player.move(True)
                                    if keys[pygame.K_DOWN] and i == 1 or keys[pygame.K_s] and i == 0: # move backward
                                        player.move(False)
                                i += 1

                        # update the players (position, speed, rays, ..)
                        for player in self.CO.players:
                            player.update()
                            # update ray length
                            player.updateRays(self.CO.mapController.getCurrentMap(self.CO.officialMaps).boundsMap)
                    elif self.CO.raceObject.raceStatus == "raceOver": # leaderboard buttons
                        for button in self.CO.leaderboardButtons:
                            if button.clicked(mx, my, pygame.mouse.get_pressed()):
                                if button.action == "restart":
                                    self.CO.raceObject.reset()
                                elif button.action == "choseMap":
                                    self.CO.gameStatus = "selectMap"
                                elif button.action == "saveMap" and self.CO.mapController.getCurrentMap(self.CO.officialMaps).name == "generatedWFC":
                                    currentTime = datetime.datetime.now()
                                    name = "generated map: "
                                    name += str(currentTime.hour) + ":"
                                    name += str(currentTime.minute) + ":"
                                    name += str(currentTime.second) + " | "
                                    name += str(currentTime.day) + "."
                                    name += str(currentTime.month) + "."
                                    name += str(currentTime.year)
                                    self.CO.mapController.getCurrentMap(self.CO.officialMaps).saveMap(self.customMapPath, name)
                    elif self.CO.raceObject.raceStatus == "paused":
                        for button in self.CO.pauseButtons: # paused menu buttons
                            if button.clicked(mx, my, pygame.mouse.get_pressed()):
                                if button.action == "resume":
                                    self.CO.raceObject.resume()
                                elif button.action == "restart":
                                    self.CO.raceObject.reset()
                                elif button.action == "mainMenu":
                                    self.CO.gameStatus = "menu"



            if self.CO.gameStatus == "generateMap":
                # movement keys pressed --> Update player
                if keys[pygame.K_LEFT] or keys[pygame.K_a]: # turn left
                    self.CO.players[0].changeDir(False)
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]: # turn right
                    self.CO.players[0].changeDir(True)
                if keys[pygame.K_UP] or keys[pygame.K_w]: # move forward
                    self.CO.players[0].move(True)
                if keys[pygame.K_DOWN] or keys[pygame.K_s]: # move backward
                    self.CO.players[0].move(False)

                self.CO.players[0].update()




            self.TPSClock.tick(self.CO.TPS) # limit Game Ticks

        self.gameDisplay.join()
        pygame.quit()


game = GameMain()
