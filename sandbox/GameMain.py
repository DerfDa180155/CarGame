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
import Bot
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
        self.settingsImg.set_colorkey((255, 255, 255))
        self.playButtonImg = pygame.image.load(self.imagePath + "playButton.png").convert()
        self.quitButtonImg = pygame.image.load(self.imagePath + "quitButton.png").convert()
        self.scrollBarImg = pygame.image.load(self.imagePath + "scrollBar.png").convert()
        self.selectButtonImg = pygame.image.load(self.imagePath + "selectButton.png").convert()
        self.returnButtonImg = pygame.image.load(self.imagePath + "returnButton.png").convert()
        self.nextPageButtonImg = pygame.image.load(self.imagePath + "nextPageButton.png").convert()
        self.previousPageButtonImg = pygame.image.load(self.imagePath + "previousPageButton.png").convert()
        self.applyButtonImg = pygame.image.load(self.imagePath + "applyButton.png").convert()
        self.saveButtonImg = pygame.image.load(self.imagePath + "saveButton.png").convert()
        self.homeButtonImg = pygame.image.load(self.imagePath + "homeButton.png").convert()
        self.restartButtonImg = pygame.image.load(self.imagePath + "restartButton.png").convert()
        self.resumeButtonImg = pygame.image.load(self.imagePath + "resumeButton.png").convert()

        self.boostItemImg = pygame.image.load(self.imagePath + "boostItem.png").convert()
        self.rocketItemImg = pygame.image.load(self.imagePath + "rocketItem.png").convert()
        self.multiRocketItemImg = pygame.image.load(self.imagePath + "multiRocketItem.png").convert()
        self.shieldItemImg = pygame.image.load(self.imagePath + "shieldItem.png").convert()
        self.godModeItemImg = pygame.image.load(self.imagePath + "godModeItem.png").convert()

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

        # items
        self.boostItem = self.boostItemImg
        self.rocketItem = self.rocketItemImg
        self.multiRocketItem = self.multiRocketItemImg
        self.shieldItem = self.shieldItemImg
        self.oilPuddleItem = self.topRight
        self.godModeItem = self.godModeItemImg
        self.itemImageDictionary = [self.boostItem, self.rocketItem, self.multiRocketItem, self.shieldItem, self.oilPuddleItem, self.godModeItem]
        self.summonedItems = []
        self.itemBoxes = []

        # cars
        self.carSkins = [(255,0,0),(255,255,0),(0,255,0),(0,255,255),(0,0,255),(255,0,255),(255,255,255),(100,100,100)]

        # player
        self.players = []
        self.players.append(Player.Player(100, 100, 0, 0, self.summonedItems))

        # bots
        self.bots = []
        self.bots.append(Bot.Bot(Player.Player(100, 100, 0, 100, self.summonedItems)))

        self.raceObject = RaceObject.RaceObject(players=self.players, bots=self.bots, raceMap=self.mapController.maps[0], amountOfItems=len(self.itemImageDictionary), summonedItems=self.summonedItems, itemBoxes=self.itemBoxes)
        self.settings = Settings.Settings(self.settingsPath)
        self.displayTempSettings = Settings.Settings(self.settingsPath)
        self.mapMaker = MapMaker.MapMaker()

        # buttons
        # main menu buttons
        #self.testButton = Button.Button(self.screen, 100, 100, 150, self.crossing, "generateMap")
        self.modeSelectButton = Button.Button(self.screen, 100, 300, 150, self.playButtonImg, "selectMode")
        self.mapMakerButton = Button.Button(self.screen, 100, 500, 150, self.crossing, "mapMaker")
        self.mapSelectButton = Button.Button(self.screen, 1350, 500, 150, self.topLeft, "selectMap")
        self.settingsButton = Button.Button(self.screen, 1460, 40, 100, self.settingsImg, "settings")
        self.linkButton = Button.Button(self.screen, 1450, 750, 100, self.empty, "https://github.com/DerfDa180155")
        self.quitButton = Button.Button(self.screen, 100, 700, 150, self.quitButtonImg, "quit")
        self.menuButtons = [self.modeSelectButton, self.mapMakerButton, self.mapSelectButton, self.settingsButton,
                            self.linkButton, self.quitButton]

        # game mode buttons
        self.singlePlayerButton = Button.Button(self.screen, 100, 100, 150, self.horizontalLine, "singleplayer")
        self.multiPlayerButton = Button.Button(self.screen, 100, 300, 150, self.crossing, "multiplayer")
        self.returnButton = Button.Button(self.screen, 75, 825, 50, self.returnButtonImg, "return")
        self.gameModeButtons = [self.singlePlayerButton, self.multiPlayerButton, self.returnButton]

        # car selector buttons
        self.returnButton = Button.Button(self.screen, 75, 825, 50, self.returnButtonImg, "return")
        self.readyButton = Button.Button(self.screen, 750, 750, 100, self.horizontalLine, "ready")
        self.carSelectorButtons = [self.returnButton, self.readyButton]

        # race settings buttons
        self.startRaceButtons = Button.Button(self.screen, 750, 720, 150, self.horizontalLine, "start")
        self.backButton = Button.Button(self.screen, 50, 770, 100, self.returnButtonImg, "back")
        self.roundsScrollButton = Button.Button(self.screen, 710, 100, 45, self.scrollBarImg, "scrollRounds")
        self.maxSpeedScrollButton = Button.Button(self.screen, 710, 100, 45, self.scrollBarImg, "scrollMaxSpeed")
        self.maxAccScrollButton = Button.Button(self.screen, 710, 100, 45, self.scrollBarImg, "scrollMaxAcc")
        self.itemsEnabledScrollButton = Button.Button(self.screen, 710, 100, 45, self.scrollBarImg, "scrollItemsEnabled")
        self.itemsSpawnCooldownScrollButton = Button.Button(self.screen, 710, 100, 45, self.scrollBarImg, "scrollISC")
        self.amountBotButton = Button.Button(self.screen, 710, 100, 45, self.scrollBarImg, "scrollAmountBot")
        self.raceSettingsButtons = [self.startRaceButtons, self.backButton, self.roundsScrollButton, self.maxSpeedScrollButton, self.maxAccScrollButton, self.itemsEnabledScrollButton, self.itemsSpawnCooldownScrollButton, self.amountBotButton]

        # settings buttons
        self.saveButton = Button.Button(self.screen, 1450, 750, 100, self.saveButtonImg, "save")
        self.applyButton = Button.Button(self.screen, 750, 750, 100, self.applyButtonImg, "apply")
        self.backButton = Button.Button(self.screen, 50, 750, 100, self.returnButtonImg, "back")
        self.forwardKeyButton = Button.Button(self.screen, 710, 100, 45, self.selectButtonImg, "forwardKey")
        self.backwardKeyButton = Button.Button(self.screen, 710, 100, 45, self.selectButtonImg, "backwardKey")
        self.leftKeyButton = Button.Button(self.screen, 710, 100, 45, self.selectButtonImg, "leftKey")
        self.rightKeyButton = Button.Button(self.screen, 710, 100, 45, self.selectButtonImg, "rightKey")
        self.itemKeyButton = Button.Button(self.screen, 710, 100, 45, self.selectButtonImg, "itemKey")
        self.pauseKeyButton = Button.Button(self.screen, 710, 100, 45, self.selectButtonImg, "pauseKey")
        self.FPSScrollButton = Button.Button(self.screen, 710, 100, 45, self.scrollBarImg, "scrollFPS")
        self.TPSScrollButton = Button.Button(self.screen, 710, 100, 45, self.scrollBarImg, "scrollTPS")
        self.secondPlayerForwardKeyButton = Button.Button(self.screen, 1510, 100, 45, self.selectButtonImg, "secondPlayerForwardKey")
        self.secondPlayerBackwardKeyButton = Button.Button(self.screen, 1510, 100, 45, self.selectButtonImg, "secondPlayerBackwardKey")
        self.secondPlayerLeftKeyButton = Button.Button(self.screen, 1510, 100, 45, self.selectButtonImg, "secondPlayerLeftKey")
        self.secondPlayerRightKeyButton = Button.Button(self.screen, 1510, 100, 45, self.selectButtonImg, "secondPlayerRightKey")
        self.secondPlayerItemKeyButton = Button.Button(self.screen, 1510, 100, 45, self.selectButtonImg, "secondPlayerItemKey")
        self.debugModeToggleButton = Button.Button(self.screen, 1510, 100, 45, self.selectButtonImg, "toggleDebugMode")
        self.displayFPSToggleButton = Button.Button(self.screen, 1510, 100, 45, self.selectButtonImg, "toggleDisplayFPS")
        self.displayTPSToggleButton = Button.Button(self.screen, 1510, 100, 45, self.selectButtonImg, "toggleDisplayTPS")
        self.settingsButtons = [self.saveButton, self.applyButton, self.backButton, self.forwardKeyButton, self.backwardKeyButton, self.leftKeyButton, self.rightKeyButton, self.itemKeyButton, self.pauseKeyButton, self.FPSScrollButton, self.TPSScrollButton, self.secondPlayerForwardKeyButton, self.secondPlayerBackwardKeyButton, self.secondPlayerLeftKeyButton, self.secondPlayerRightKeyButton, self.secondPlayerItemKeyButton, self.debugModeToggleButton, self.displayFPSToggleButton, self.displayTPSToggleButton]

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
        self.saveButton = Button.Button(self.screen, 250, 775, 100, self.saveButtonImg, "actionButton-save")
        self.fillEmptyButton = Button.Button(self.screen, 400, 775, 100, self.empty, "actionButton-fillEmpty")
        self.enterNameButton = Button.Button(self.screen, 550, 775, 100, self.empty, "actionButton-enterName")
        self.createNewMapButton = Button.Button(self.screen, 700, 775, 100, self.empty, "actionButton-createNewMap")
        self.XScrollButton = Button.Button(self.screen, 920, 785, 30, self.scrollBarImg, "scrollButton-x")
        self.YScrollButton = Button.Button(self.screen, 920, 830, 30, self.scrollBarImg, "scrollButton-y")
        self.startXScrollButton = Button.Button(self.screen, 1150, 785, 30, self.scrollBarImg, "scrollButton-startX")
        self.startYScrollButton = Button.Button(self.screen, 1150, 830, 30, self.scrollBarImg, "scrollButton-startY")
        self.startDirScrollButton = Button.Button(self.screen, 1555, 830, 30, self.scrollBarImg, "scrollButton-startDir")
        self.returnButton = Button.Button(self.screen, 75, 825, 50, self.returnButtonImg, "return")
        self.mapMakerButtons = [self.bottomRightButton, self.bottomLeftButton, self.topRightButton, self.topLeftButton, self.verticalLineButton, self.horizontalLineButton, self.emptyButton, self.eraseModeButton, self.startPieceHighlightButton, self.clearButton, self.saveButton, self.fillEmptyButton, self.enterNameButton, self.createNewMapButton, self.XScrollButton, self.YScrollButton, self.startXScrollButton, self.startYScrollButton, self.startDirScrollButton, self.returnButton]

        # leaderboard buttons
        self.mainMenu = Button.Button(self.screen, 675, 625, 50, self.homeButtonImg, "mainMenu")
        self.restartButton = Button.Button(self.screen, 875, 625, 50, self.restartButtonImg, "restart")
        self.saveButton = Button.Button(self.screen, 775, 575, 50, self.crossing, "saveMap")
        self.leaderboardButtons = [self.mainMenu, self.restartButton, self.saveButton]

        # pause buttons
        self.mainMenu = Button.Button(self.screen, 650, 625, 50, self.homeButtonImg, "mainMenu")
        self.restartButton = Button.Button(self.screen, 775, 625, 50, self.restartButtonImg, "restart")
        self.resumeButton = Button.Button(self.screen, 900, 625, 50, self.resumeButtonImg, "resume")
        self.pauseButtons = [self.mainMenu, self.restartButton, self.resumeButton]

        # mapSelector buttons
        self.mapButtons = []
        self.imageMapSize = 200
        #self.locations = [[100, 100], [400, 100], [700, 100], [1000, 100], [1300, 100],
        #                  [100, 380], [400, 380], [700, 380], [1000, 380], [1300, 380],
        #                  [100, 660], [400, 660], [700, 660], [1000, 660], [1300, 660]]
        self.locations = [[100, 130], [400, 130], [700, 130], [1000, 130], [1300, 130],
                          [100, 370], [400, 370], [700, 370], [1000, 370], [1300, 370],
                          [100, 610], [400, 610], [700, 610], [1000, 610], [1300, 610]]
        # official maps
        tempArray = []
        for i in range(self.oldMapCount):
            tempArray.append(Button.Button(self.screen, self.locations[i % 15][0], self.locations[i % 15][1], self.imageMapSize, self.empty, str(i)))
            if i >= 15:
                tempArray[len(tempArray)-1].enable = False
        self.mapButtons.append(tempArray)
        # custom maps
        tempArray = []
        for i in range(self.oldCustomMapCount):
            tempArray.append(Button.Button(self.screen, self.locations[i % 15][0], self.locations[i % 15][1], self.imageMapSize, self.empty, str(i)))
            if i >= 15:
                tempArray[len(tempArray)-1].enable = False
        self.mapButtons.append(tempArray)
        self.mapButtons[1].append(Button.Button(self.screen, 750, 700, 100, self.crossing, "generateMapWFC"))
        tempArray = []
        tempArray.append(Button.Button(self.screen, 700, 825, 50, self.previousPageButtonImg, "previousPage"))
        tempArray.append(Button.Button(self.screen, 850, 825, 50, self.nextPageButtonImg, "nextPage"))
        tempArray.append(Button.Button(self.screen, 75, 825, 50, self.returnButtonImg, "return"))
        tempArray.append(Button.Button(self.screen, 1475, 825, 50, self.selectButtonImg, "toggleMaps"))
        self.mapButtons.append(tempArray)
        self.mapButtonPage = 0

        self.CO = CommunicationObject.CommunicationObject(gameStatus="menu", FPSClock=self.FPSClock,
                                                          TPSClock=self.TPSClock, #FPS=self.FPS, TPS=self.TPS,
                                                          TextSize=30, imageArray=self.mapArray,
                                                          mapController=self.mapController, carSkins=self.carSkins,
                                                          players=self.players, bots=self.bots,
                                                          raceObject=self.raceObject, settings=self.settings,
                                                          mapMaker=self.mapMaker, displayTempSettings=self.displayTempSettings,
                                                          waitForKey=False, menuButtons=self.menuButtons,
                                                          gameModeButtons=self.gameModeButtons,
                                                          carSelectorButtons = self.carSelectorButtons,
                                                          raceSettingsButtons=self.raceSettingsButtons,
                                                          leaderboardButtons=self.leaderboardButtons,
                                                          settingsButtons=self.settingsButtons,
                                                          mapMakerButtons=self.mapMakerButtons,
                                                          pauseButtons=self.pauseButtons, mapButtons=self.mapButtons,
                                                          mapButtonPage=self.mapButtonPage, officialMaps=True,
                                                          currentMode="singleplayer",
                                                          itemImageDictionary=self.itemImageDictionary,
                                                          summonedItems=self.summonedItems, itemBoxes=self.itemBoxes)

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
                        elif self.CO.gameStatus == "selectCar":
                            self.CO.gameStatus = "selectMode"
                        elif self.CO.gameStatus == "selectMap":
                            self.CO.gameStatus = "selectCar"
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

            # toggle debug menu
            if keys[pygame.K_TAB]:
                self.CO.settings.debugMode = not self.CO.settings.debugMode
                time.sleep(0.3)

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
                            elif button.action == "toggleDebugMode":
                                self.CO.displayTempSettings.debugMode = not self.CO.displayTempSettings.debugMode
                            elif button.action == "toggleDisplayFPS":
                                self.CO.displayTempSettings.displayFPS = not self.CO.displayTempSettings.displayFPS
                            elif button.action == "toggleDisplayTPS":
                                self.CO.displayTempSettings.displayTPS = not self.CO.displayTempSettings.displayTPS
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
                                        self.CO.displayTempSettings.playerKeys[0][0] = pygame.key.name(text)
                                    case "backwardKey":
                                        self.CO.displayTempSettings.playerKeys[0][1] = pygame.key.name(text)
                                    case "leftKey":
                                        self.CO.displayTempSettings.playerKeys[0][2] = pygame.key.name(text)
                                    case "rightKey":
                                        self.CO.displayTempSettings.playerKeys[0][3] = pygame.key.name(text)
                                    case "itemKey":
                                        self.CO.displayTempSettings.playerKeys[0][4] = pygame.key.name(text)
                                    case "pauseKey":
                                        self.CO.displayTempSettings.pauseKey = pygame.key.name(text)
                                    case "secondPlayerForwardKey":
                                        self.CO.displayTempSettings.playerKeys[1][0] = pygame.key.name(text)
                                    case "secondPlayerBackwardKey":
                                        self.CO.displayTempSettings.playerKeys[1][1] = pygame.key.name(text)
                                    case "secondPlayerLeftKey":
                                        self.CO.displayTempSettings.playerKeys[1][2] = pygame.key.name(text)
                                    case "secondPlayerRightKey":
                                        self.CO.displayTempSettings.playerKeys[1][3] = pygame.key.name(text)
                                    case "secondPlayerItemKey":
                                        self.CO.displayTempSettings.playerKeys[1][4] = pygame.key.name(text)
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
                        self.CO.mapMaker.tempName = ""
                        self.CO.waitForKey = True
                        while self.CO.waitForKey:
                            for detect in pygame.event.get():
                                if detect.type == pygame.KEYDOWN:
                                    if detect.key == 13:
                                        self.CO.waitForKey = False
                                    else:
                                        if detect.key == 8:
                                            self.CO.mapMaker.tempName = self.CO.mapMaker.tempName[:-1]
                                        else:
                                            self.CO.mapMaker.tempName += str(detect.unicode)
                            time.sleep(0.001) # a little delay, because the display thread drops to 2 FPS without
                        self.CO.mapMaker.enteringName = False
                        self.CO.mapMaker.mapName = str(self.CO.mapMaker.tempName)
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
                                elif button.action == "return":
                                    self.CO.gameStatus = "menu"
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
                            if button.action == "return":
                                self.CO.gameStatus = "menu"
                            else:
                                self.CO.currentMode = button.action
                                self.CO.raceObject.mode = button.action
                                self.CO.players[0].selectedCarId = 0
                                if button.action == "singleplayer" and len(self.CO.players) == 2:
                                    self.CO.players.pop(1)
                                elif button.action == "multiplayer" and len(self.CO.players) == 1:
                                    self.CO.players.append(Player.Player(0, 0, 0, 1, self.summonedItems))
                                    self.CO.players[1].selectedCarId = 1
                                self.CO.gameStatus = "selectCar"
                                print(self.CO.currentMode)
                                self.CO.mapButtonPage = 0
                case "selectCar":
                    for i in range(len(self.CO.players)):
                        selected = -1
                        if self.CO.currentMode == "multiplayer":
                            selected = self.CO.players[1-i].selectedCarId
                        if keys[pygame.key.key_code(self.CO.settings.playerKeys[i][2])]: # left
                            self.CO.players[i].selectedCarId -= 1
                            if self.CO.players[i].selectedCarId == -1:
                                self.CO.players[i].selectedCarId = 3
                            elif self.CO.players[i].selectedCarId == 3:
                                self.CO.players[i].selectedCarId = 7
                            if self.CO.players[i].selectedCarId == selected:
                                self.CO.players[i].selectedCarId -= 1
                                if self.CO.players[i].selectedCarId == -1:
                                    self.CO.players[i].selectedCarId = 3
                                elif self.CO.players[i].selectedCarId == 3:
                                    self.CO.players[i].selectedCarId = 7
                            time.sleep(0.1)
                        if keys[pygame.key.key_code(self.CO.settings.playerKeys[i][3])]: # right
                            self.CO.players[i].selectedCarId += 1
                            if self.CO.players[i].selectedCarId == 4:
                                self.CO.players[i].selectedCarId = 0
                            elif self.CO.players[i].selectedCarId == 8:
                                self.CO.players[i].selectedCarId = 4
                            if self.CO.players[i].selectedCarId == selected:
                                self.CO.players[i].selectedCarId += 1
                                if self.CO.players[i].selectedCarId == 4:
                                    self.CO.players[i].selectedCarId = 0
                                elif self.CO.players[i].selectedCarId == 8:
                                    self.CO.players[i].selectedCarId = 4
                            time.sleep(0.1)
                        if keys[pygame.key.key_code(self.CO.settings.playerKeys[i][0])]: # up
                            self.CO.players[i].selectedCarId -= 4
                            if self.CO.players[i].selectedCarId <= -1:
                                self.CO.players[i].selectedCarId += 8
                            if self.CO.players[i].selectedCarId == selected:
                                self.CO.players[i].selectedCarId -= 4
                                if self.CO.players[i].selectedCarId <= -1:
                                    self.CO.players[i].selectedCarId += 8
                            time.sleep(0.1)
                        if keys[pygame.key.key_code(self.CO.settings.playerKeys[i][1])]: # down
                            self.CO.players[i].selectedCarId += 4
                            if self.CO.players[i].selectedCarId >= 8:
                                self.CO.players[i].selectedCarId -= 8
                            if self.CO.players[i].selectedCarId == selected:
                                self.CO.players[i].selectedCarId += 4
                                if self.CO.players[i].selectedCarId >= 8:
                                    self.CO.players[i].selectedCarId -= 8
                            time.sleep(0.1)


                    for button in self.CO.carSelectorButtons:
                        if button.clicked(mx, my, mousePressedUp):
                            if button.action == "return":
                                self.CO.gameStatus = "selectMode"
                            elif button.action == "ready":
                                self.CO.gameStatus = "selectMap"
                case "selectMap":
                    # calculate max page
                    maxPageOfficialMaps = round((len(self.CO.mapButtons[0])/15)+0.5)-1
                    maxPageCustomMaps = round((len(self.CO.mapButtons[1])/15)+0.5)-1

                    # previous and next page buttons enable and disable
                    for button in self.CO.mapButtons[2]:
                        if button.action == "previousPage":
                            button.enable = self.CO.mapButtonPage > 0
                        elif button.action == "nextPage":
                            button.enable = (self.CO.officialMaps and (self.CO.mapButtonPage < maxPageOfficialMaps)) or (not self.CO.officialMaps and (self.CO.mapButtonPage < maxPageCustomMaps))


                    # hotkeys for debugging and testing
                    if keys[pygame.K_j]:
                        if self.CO.mapButtonPage != 0:
                            self.CO.mapButtonPage -= 1
                            print(self.CO.mapButtonPage)
                            time.sleep(0.3)
                    elif keys[pygame.K_k]:
                        if self.CO.officialMaps:
                            if self.CO.mapButtonPage < maxPageOfficialMaps:
                                self.CO.mapButtonPage += 1
                                print(self.CO.mapButtonPage)
                                time.sleep(0.3)
                        else:
                            if self.CO.mapButtonPage < maxPageCustomMaps:
                                self.CO.mapButtonPage += 1
                                print(self.CO.mapButtonPage)
                                time.sleep(0.3)
                    elif keys[pygame.K_l]: # toggle official and custom maps
                        self.CO.officialMaps = not self.CO.officialMaps
                        time.sleep(0.3)

                    index = 1
                    if self.CO.officialMaps:
                        index = 0

                    if self.CO.officialMaps: # official maps
                        for button in self.CO.mapButtons[0]:
                            button.enable = self.CO.mapButtonPage * 15 <= int(button.action) <= (self.CO.mapButtonPage + 1) * 15
                        for button in self.CO.mapButtons[1]:
                            button.enable = False

                    else: # custom maps
                        for button in self.CO.mapButtons[0]:
                            button.enable = False
                        for button in self.CO.mapButtons[1]:
                            if button.action == "generateMapWFC":
                                button.enable = True
                            else:
                                button.enable = (self.CO.mapButtonPage-maxPageOfficialMaps) * 15 <= int(button.action) <= ((self.CO.mapButtonPage-maxPageOfficialMaps) + 1) * 15

                    for button in self.CO.mapButtons[index] + self.CO.mapButtons[2]:
                        if button.clicked(mx, my, mousePressedUp):
                            if not button.action.isnumeric():
                                if button.action == "generateMapWFC":
                                    #self.CO.mapController.generateNewMap(random.randint(2, 6), random.randint(2, 6), False, True)
                                    #self.CO.gameStatus = "raceSettings"
                                    #self.CO.raceObject.reset(True)
                                    self.CO.gameStatus = "generateMapWFC"
                                elif button.action == "previousPage":
                                    if self.CO.mapButtonPage > 0:
                                        self.CO.mapButtonPage -= 1
                                        print(self.CO.mapButtonPage)
                                elif button.action == "nextPage":
                                    if self.CO.officialMaps:
                                        if self.CO.mapButtonPage < maxPageOfficialMaps:
                                            self.CO.mapButtonPage += 1
                                            print(self.CO.mapButtonPage)
                                    else:
                                        if self.CO.mapButtonPage < maxPageCustomMaps:
                                            self.CO.mapButtonPage += 1
                                            print(self.CO.mapButtonPage)
                                elif button.action == "return":
                                    self.CO.gameStatus = "selectCar"
                                elif button.action == "toggleMaps":
                                    self.CO.officialMaps = not self.CO.officialMaps
                                    self.CO.mapButtonPage = 0
                            else:
                                self.CO.mapController.currentMapIndex = button.action
                                for player in self.CO.players:
                                    player.reset(x=self.CO.mapController.getCurrentMap(self.CO.officialMaps).playerStartX,
                                                 y=self.CO.mapController.getCurrentMap(self.CO.officialMaps).playerStartY,
                                                 direction=self.CO.mapController.getCurrentMap(self.CO.officialMaps).playerStartDirection)
                                self.CO.gameStatus = "raceSettings"
                                self.CO.raceObject.reset(True)
                case "generateMapWFC":
                    pass
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
                                        self.CO.raceObject.itemSpawnCooldown += 30
                                    elif scrolledDown:
                                        self.CO.raceObject.itemSpawnCooldown -= 30
                                        if self.CO.raceObject.itemSpawnCooldown < 30:
                                            self.CO.raceObject.itemSpawnCooldown = 30
                                case "scrollAmountBot":
                                    if scrolledUp:
                                        self.CO.raceObject.amountOfBots += 1
                                        if self.CO.raceObject.mode == "singleplayer":
                                            if self.CO.raceObject.amountOfBots > 7:
                                                self.CO.raceObject.amountOfBots = 7
                                        else:
                                            if self.CO.raceObject.amountOfBots > 6:
                                                self.CO.raceObject.amountOfBots = 6
                                    elif scrolledDown:
                                        self.CO.raceObject.amountOfBots -= 1
                                        if self.CO.raceObject.amountOfBots < 0:
                                            self.CO.raceObject.amountOfBots = 0

                case "race":
                    # update raceObject
                    self.CO.raceObject.update()

                    if keys[pygame.K_t]:
                        self.CO.raceObject.reset()
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
                            if keys[pygame.key.key_code(self.CO.settings.playerKeys[0][2])] or keys[pygame.key.key_code(self.CO.settings.playerKeys[1][2])]: # turn left
                                self.CO.players[0].changeDir(False)
                            if keys[pygame.key.key_code(self.CO.settings.playerKeys[0][3])] or keys[pygame.key.key_code(self.CO.settings.playerKeys[1][3])]: # turn right
                                self.CO.players[0].changeDir(True)
                            if keys[pygame.key.key_code(self.CO.settings.playerKeys[0][0])] or keys[pygame.key.key_code(self.CO.settings.playerKeys[1][0])]: # move forward
                                self.CO.players[0].move(True)
                            if keys[pygame.key.key_code(self.CO.settings.playerKeys[0][1])] or keys[pygame.key.key_code(self.CO.settings.playerKeys[1][1])]: # move backward
                                self.CO.players[0].move(False)
                            if keys[pygame.key.key_code(self.CO.settings.playerKeys[0][4])] or keys[pygame.key.key_code(self.CO.settings.playerKeys[1][4])]: # item
                                self.CO.players[0].useItem()
                        elif self.CO.currentMode == "multiplayer":
                            i = 0
                            for player in self.CO.players:
                                if not player.isDone:
                                    if keys[pygame.key.key_code(self.CO.settings.playerKeys[i][2])]: # turn left
                                        player.changeDir(False)
                                    if keys[pygame.key.key_code(self.CO.settings.playerKeys[i][3])]: # turn right
                                        player.changeDir(True)
                                    if keys[pygame.key.key_code(self.CO.settings.playerKeys[i][0])]: # move forward
                                        player.move(True)
                                    if keys[pygame.key.key_code(self.CO.settings.playerKeys[i][1])]: # move backward
                                        player.move(False)
                                    if keys[pygame.key.key_code(self.CO.settings.playerKeys[i][4])]:  # item
                                        player.useItem()
                                i += 1

                        # update the players (position, speed, rays, ..)
                        for player in self.CO.players:
                            player.update()
                            # update ray length
                            player.updateRays(self.CO.mapController.getCurrentMap(self.CO.officialMaps).boundsMap)

                        # update the bots
                        if self.CO.raceObject.amountOfBots > 0:
                            for bot in self.CO.bots:
                                bot.player.update()
                                # update ray length
                                bot.player.updateRays(self.CO.mapController.getCurrentMap(self.CO.officialMaps).boundsMap)

                        # update items
                        for item in self.CO.summonedItems:
                            item.update()
                            match item.itemName:
                                case "Rocket" | "MultiRocket":
                                    item.updateRays(self.CO.mapController.getCurrentMap(self.CO.officialMaps).boundsMap)
                    elif self.CO.raceObject.raceStatus == "raceOver": # leaderboard buttons
                        for button in self.CO.leaderboardButtons:
                            if button.clicked(mx, my, mousePressedUp):
                                if button.action == "restart":
                                    self.CO.raceObject.reset()
                                    self.CO.raceObject.start(self.CO.mapController.getCurrentMap(self.CO.officialMaps))
                                elif button.action == "mainMenu":
                                    self.CO.gameStatus = "menu"
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
                                    self.CO.raceObject.start(self.CO.mapController.getCurrentMap(self.CO.officialMaps))
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
