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
import MapMaker
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
        #self.FPS = 144
        #self.TPS = 120

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
        self.displayTempSettings = Settings.Settings(self.settingsPath)
        self.mapMaker = MapMaker.MapMaker()

        # buttons
        # main menu buttons
        #self.testButton = Button.Button(self.screen, 100, 100, 150, self.crossing, "generateMap")
        self.testButton = Button.Button(self.screen, 100, 100, 150, self.crossing, "mapMaker")
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
        self.saveButton = Button.Button(self.screen, 1450, 750, 100, self.verticalLine, "save")
        self.applyButton = Button.Button(self.screen, 750, 750, 100, self.crossing, "apply")
        self.backButton = Button.Button(self.screen, 50, 750, 100, self.bottomLeft, "back")
        self.forwardKeyButton = Button.Button(self.screen, 710, 100, 45, self.verticalLine, "forwardKey")
        self.backwardKeyButton = Button.Button(self.screen, 710, 100, 45, self.verticalLine, "backwardKey")
        self.leftKeyButton = Button.Button(self.screen, 710, 100, 45, self.verticalLine, "leftKey")
        self.rightKeyButton = Button.Button(self.screen, 710, 100, 45, self.verticalLine, "rightKey")
        self.pauseKeyButton = Button.Button(self.screen, 710, 100, 45, self.verticalLine, "pauseKey")
        self.FPSScrollButton = Button.Button(self.screen, 710, 100, 45, self.verticalLine, "scrollFPS")
        self.TPSScrollButton = Button.Button(self.screen, 710, 100, 45, self.verticalLine, "scrollTPS")
        self.settingsButtons = [self.saveButton, self.applyButton, self.backButton, self.forwardKeyButton, self.backwardKeyButton, self.leftKeyButton, self.rightKeyButton, self.pauseKeyButton, self.FPSScrollButton, self.TPSScrollButton]

        # mapMaker buttons
        self.bottomRightButton = Button.Button(self.screen, 1300, 100, 100, self.bottomRight, "mapPiece-bottomRight")
        self.bottomLeftButton = Button.Button(self.screen, 1450, 100, 100, self.bottomLeft, "mapPiece-bottomLeft")
        self.topRightButton = Button.Button(self.screen, 1300, 250, 100, self.topRight, "mapPiece-topRight")
        self.topLeftButton = Button.Button(self.screen, 1450, 250, 100, self.topLeft, "mapPiece-topLeft")
        self.verticalLineButton = Button.Button(self.screen, 1300, 400, 100, self.verticalLine, "mapPiece-verticalLine")
        self.horizontalLineButton = Button.Button(self.screen, 1450, 400, 100, self.horizontalLine, "mapPiece-horizontalLine")
        self.emptyButton = Button.Button(self.screen, 1300, 550, 100, self.empty, "mapPiece-empty")
        self.eraseModeButton = Button.Button(self.screen, 1300, 750, 50, self.empty, "actionButton-eraseMode")
        self.startPieceHighlightButton = Button.Button(self.screen, 1375, 750, 50, self.empty, "actionButton-startPieceHighlight")
        self.clearButton = Button.Button(self.screen, 100, 775, 100, self.empty, "actionButton-clear")
        self.saveButton = Button.Button(self.screen, 250, 775, 100, self.empty, "actionButton-save")
        self.fillEmptyButton = Button.Button(self.screen, 400, 775, 100, self.empty, "actionButton-fillEmpty")
        self.enterNameButton = Button.Button(self.screen, 550, 775, 100, self.empty, "actionButton-enterName")
        self.createNewMapButton = Button.Button(self.screen, 700, 775, 100, self.empty, "actionButton-createNewMap")
        self.XScrollButton = Button.Button(self.screen, 920, 785, 30, self.verticalLine, "scrollButton-x")
        self.YScrollButton = Button.Button(self.screen, 920, 830, 30, self.verticalLine, "scrollButton-y")
        self.startXScrollButton = Button.Button(self.screen, 1150, 785, 30, self.verticalLine, "scrollButton-startX")
        self.startYScrollButton = Button.Button(self.screen, 1150, 830, 30, self.verticalLine, "scrollButton-startY")
        self.startDirScrollButton = Button.Button(self.screen, 1555, 830, 30, self.verticalLine, "scrollButton-startDir")
        self.mapMakerButtons = [self.bottomRightButton, self.bottomLeftButton, self.topRightButton, self.topLeftButton, self.verticalLineButton, self.horizontalLineButton, self.emptyButton, self.eraseModeButton, self.startPieceHighlightButton, self.clearButton, self.saveButton, self.fillEmptyButton, self.enterNameButton, self.createNewMapButton, self.XScrollButton, self.YScrollButton, self.startXScrollButton, self.startYScrollButton, self.startDirScrollButton]

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
                                                          TPSClock=self.TPSClock, #FPS=self.FPS, TPS=self.TPS,
                                                          TextSize=30, imageArray=self.mapArray,
                                                          mapController=self.mapController, players=self.players,
                                                          raceObject=self.raceObject, settings=self.settings,
                                                          mapMaker=self.mapMaker, displayTempSettings=self.displayTempSettings,
                                                          waitForKey=False, menuButtons=self.menuButtons,
                                                          gameModeButtons=self.gameModeButtons,
                                                          raceSettingsButtons=self.raceSettingsButtons,
                                                          leaderboardButtons=self.leaderboardButtons,
                                                          settingsButtons=self.settingsButtons,
                                                          mapMakerButtons=self.mapMakerButtons,
                                                          pauseButtons=self.pauseButtons, mapButtons=self.mapButtons,
                                                          mapButtonPage=self.mapButtonPage, officialMaps=True,
                                                          currentMode="singleplayer")

        self.gameDisplay = GameDisplay.GameDisplay(screen=self.screen, CO=self.CO)
        self.gameDisplay.start()

        self.run()

    def run(self):
        oldMousePressed = (False, False, False)
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
                        elif self.CO.gameStatus == "selectMode" or self.CO.gameStatus == "settings" or self.CO.gameStatus == "mapMaker":
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
            mousePressed = pygame.mouse.get_pressed() # get current mouse pressed
            mousePressedUp = []
            mousePressedDown = []
            for i in range(len(mousePressed)):
                mousePressedUp.append(not mousePressed[i] and oldMousePressed[i])
                mousePressedDown.append(mousePressed[i] and not oldMousePressed[i])
            #print(mousePressed)
            #print(mousePressedUp)
            #print(mousePressedDown)
            #print(oldMousePressed)
            #print("----")
            oldMousePressed = mousePressed

            match self.CO.gameStatus:
                case "menu":
                    for button in self.CO.menuButtons:
                        if button.clicked(mx, my, mousePressedUp):
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
                        if button.clicked(mx, my, mousePressedUp):
                            if button.action == "save":
                                self.CO.displayTempSettings.saveSettings()
                            elif button.action == "back":
                                self.CO.gameStatus = "menu"
                            elif button.action == "apply":
                                self.CO.settings.copyFrom(self.CO.displayTempSettings)
                            elif button.action not in ["scrollFPS", "scrollTPS"]:
                                text = ""
                                self.CO.waitForKey = True
                                while text == "":
                                    for detect in pygame.event.get():
                                        if detect.type == pygame.KEYDOWN:
                                            text = detect.key
                                self.CO.waitForKey = False
                                match button.action:
                                    case "forwardKey":
                                        self.CO.displayTempSettings.driveForwardKey = pygame.key.name(text)
                                    case "backwardKey":
                                        self.CO.displayTempSettings.driveBackwardKey = pygame.key.name(text)
                                    case "leftKey":
                                        self.CO.displayTempSettings.steerLeftKey = pygame.key.name(text)
                                    case "rightKey":
                                        self.CO.displayTempSettings.steerRightKey = pygame.key.name(text)
                                    case "pauseKey":
                                        self.CO.displayTempSettings.pauseKey = pygame.key.name(text)
                        if button.hover(mx, my):
                            match button.action:
                                case "scrollFPS":
                                    if scrolledUp:
                                        self.CO.displayTempSettings.FPS += 1
                                    if scrolledDown and self.CO.displayTempSettings.FPS > 1:
                                        self.CO.displayTempSettings.FPS -= 1
                                case "scrollTPS":
                                    if scrolledUp:
                                        self.CO.displayTempSettings.TPS += 1
                                    if scrolledDown and self.CO.displayTempSettings.TPS > 1:
                                        self.CO.displayTempSettings.TPS -= 1
                case "mapMaker":
                    if self.CO.mapMaker.enteringName:
                        text = ""
                        self.CO.waitForKey = True
                        while self.CO.waitForKey:
                            for detect in pygame.event.get():
                                if detect.type == pygame.KEYDOWN:
                                    if detect.key == 13:
                                        self.CO.waitForKey = False
                                    else:
                                        if detect.key == 8:
                                            text = text[:-1]
                                        else:
                                            text += str(detect.unicode)

                        self.CO.mapMaker.enteringName = False
                        self.CO.mapMaker.mapName = str(text)
                        print(text)
                    else:
                        # hotkeys
                        if keys[pygame.K_w]:
                            if self.CO.mapMaker.selectedPiece == 3: # bottom left
                                self.CO.mapMaker.selectedPiece = 1 # top left
                            elif self.CO.mapMaker.selectedPiece == 4: # bottom right
                                self.CO.mapMaker.selectedPiece = 2 # top right
                            elif self.CO.mapMaker.selectedPiece in [0, 6]: # empty | horizontal line
                                self.CO.mapMaker.selectedPiece = 5 # vertical line
                        elif keys[pygame.K_s]:
                            if self.CO.mapMaker.selectedPiece == 1: # top left
                                self.CO.mapMaker.selectedPiece = 3 # bottom left
                            elif self.CO.mapMaker.selectedPiece == 2: # top right
                                self.CO.mapMaker.selectedPiece = 4 # bottom right
                            elif self.CO.mapMaker.selectedPiece in [0, 6]: # empty | horizontal line
                                self.CO.mapMaker.selectedPiece = 5 # vertical line
                        elif keys[pygame.K_a]:
                            if self.CO.mapMaker.selectedPiece == 2: # top right
                                self.CO.mapMaker.selectedPiece = 1 # top left
                            elif self.CO.mapMaker.selectedPiece == 4: # bottom right
                                self.CO.mapMaker.selectedPiece = 3 # bottom left
                            elif self.CO.mapMaker.selectedPiece in [0, 5]: # empty | vertical line
                                self.CO.mapMaker.selectedPiece = 6 # horizontal line
                        elif keys[pygame.K_d]:
                            if self.CO.mapMaker.selectedPiece == 1: # top left
                                self.CO.mapMaker.selectedPiece = 2 # top right
                            elif self.CO.mapMaker.selectedPiece == 3: # bottom left
                                self.CO.mapMaker.selectedPiece = 4 # bottom right
                            elif self.CO.mapMaker.selectedPiece in [0, 5]: # empty | vertical line
                                self.CO.mapMaker.selectedPiece = 6 # horizontal line
                        elif keys[pygame.K_1]:
                            self.CO.mapMaker.selectedPiece = 0
                        elif keys[pygame.K_2]:
                            self.CO.mapMaker.selectedPiece = 1
                        elif keys[pygame.K_3]:
                            self.CO.mapMaker.selectedPiece = 2
                        elif keys[pygame.K_4]:
                            self.CO.mapMaker.selectedPiece = 3
                        elif keys[pygame.K_5]:
                            self.CO.mapMaker.selectedPiece = 4
                        elif keys[pygame.K_6]:
                            self.CO.mapMaker.selectedPiece = 5
                        elif keys[pygame.K_7]:
                            self.CO.mapMaker.selectedPiece = 6
                        elif keys[pygame.K_g]: # clear map
                            self.CO.mapMaker.clearMap()
                        elif keys[pygame.K_h]: # fill map empty
                            self.CO.mapMaker.fillMap(0)
                        elif keys[pygame.K_q]:
                            self.CO.mapMaker.enablePlace = not self.CO.mapMaker.enablePlace
                            time.sleep(0.2)
                        elif keys[pygame.K_e]:
                            self.CO.mapMaker.highlightStartingPiece = not self.CO.mapMaker.highlightStartingPiece
                            #print(self.CO.mapMaker.highlightStartingPiece)
                            time.sleep(0.2)

                        for button in self.CO.mapMakerButtons:
                            if button.clicked(mx, my, mousePressedUp):
                                if "mapPiece-" in button.action:
                                    dictionary = {
                                        "mapPiece-empty": 0,
                                        "mapPiece-topLeft": 1,
                                        "mapPiece-topRight": 2,
                                        "mapPiece-bottomLeft": 3,
                                        "mapPiece-bottomRight": 4,
                                        "mapPiece-verticalLine": 5,
                                        "mapPiece-horizontalLine": 6,
                                    }
                                    self.CO.mapMaker.selectedPiece = dictionary[button.action]
                                    #print(self.CO.mapMaker.selectedPiece)
                                elif button.action == "actionButton-clear":
                                    self.CO.mapMaker.clearMap()
                                elif button.action == "actionButton-save":
                                    self.CO.mapMaker.save(self.customMapPath)
                                elif button.action == "actionButton-fillEmpty":
                                    self.CO.mapMaker.fillMap(0)
                                elif button.action == "actionButton-enterName":
                                    self.CO.mapMaker.enteringName = True
                                elif button.action == "actionButton-eraseMode":
                                    self.CO.mapMaker.enablePlace = not self.CO.mapMaker.enablePlace
                                elif button.action == "actionButton-createNewMap":
                                    self.CO.mapMaker.createEmptyMap(self.CO.mapMaker.x, self.CO.mapMaker.y, True)
                                elif button.action == "actionButton-startPieceHighlight":
                                    self.CO.mapMaker.highlightStartingPiece = not self.CO.mapMaker.highlightStartingPiece
                            elif button.hover(mx, my):
                                match button.action:
                                    case "scrollButton-x":
                                        if scrolledUp:
                                            self.CO.mapMaker.x += 1
                                        elif scrolledDown:
                                            self.CO.mapMaker.x -= 1
                                            if self.CO.mapMaker.x < 1:
                                                self.CO.mapMaker.x = 1
                                    case "scrollButton-y":
                                        if scrolledUp:
                                            self.CO.mapMaker.y += 1
                                        elif scrolledDown:
                                            self.CO.mapMaker.y -= 1
                                            if self.CO.mapMaker.y < 1:
                                                self.CO.mapMaker.y = 1
                                    case "scrollButton-startX":
                                        if scrolledUp:
                                            self.CO.mapMaker.startingPiece[0] += 1
                                            if self.CO.mapMaker.startingPiece[0] > self.CO.mapMaker.x - 1:
                                                self.CO.mapMaker.startingPiece[0] = self.CO.mapMaker.x - 1
                                        elif scrolledDown:
                                            self.CO.mapMaker.startingPiece[0] -= 1
                                            if self.CO.mapMaker.startingPiece[0] < 0:
                                                self.CO.mapMaker.startingPiece[0] = 0
                                    case "scrollButton-startY":
                                        if scrolledUp:
                                            self.CO.mapMaker.startingPiece[1] += 1
                                            if self.CO.mapMaker.startingPiece[1] > self.CO.mapMaker.y - 1:
                                                self.CO.mapMaker.startingPiece[1] = self.CO.mapMaker.y - 1
                                        elif scrolledDown:
                                            self.CO.mapMaker.startingPiece[1] -= 1
                                            if self.CO.mapMaker.startingPiece[1] < 0:
                                                self.CO.mapMaker.startingPiece[1] = 0
                                    case "scrollButton-startDir":
                                        if scrolledUp:
                                            self.CO.mapMaker.startingDirection += 90
                                            if self.CO.mapMaker.startingDirection >= 360:
                                                self.CO.mapMaker.startingDirection -= 360
                                        elif scrolledDown:
                                            self.CO.mapMaker.startingDirection -= 90
                                            if self.CO.mapMaker.startingDirection < 0:
                                                self.CO.mapMaker.startingDirection += 360
                        # place selected piece
                        if self.CO.mapMaker.mapRect.collidepoint((mx, my)) and mousePressed[0]:
                            widthGridOne = self.CO.mapMaker.mapRect.width / self.CO.mapMaker.x
                            heightGridOne = self.CO.mapMaker.mapRect.height / self.CO.mapMaker.y
                            gridX = int((mx-self.CO.mapMaker.mapRect.x)/widthGridOne)
                            gridY = int((my-self.CO.mapMaker.mapRect.y)/heightGridOne)
                            #print(str(gridX) + " | " + str(gridY))
                            self.CO.mapMaker.place(gridX, gridY)
                case "selectMode":
                    for button in self.CO.gameModeButtons:
                        if button.clicked(mx, my, mousePressedUp):
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
                        if button.clicked(mx, my, mousePressedUp):
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
                        if button.clicked(mx, my, mousePressedUp):
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
                            if button.clicked(mx, my, mousePressedUp):
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
                            if button.clicked(mx, my, mousePressedUp):
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




            self.TPSClock.tick(self.CO.settings.TPS) # limit Game Ticks

        self.gameDisplay.join()
        pygame.quit()


game = GameMain()
