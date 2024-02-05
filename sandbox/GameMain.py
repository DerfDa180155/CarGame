import pygame
import random
import os
import threading
import time
import numpy
import CommunicationObject
import GameDisplay
import WaveFunctionCollapse
import MapCleaner
import Player
import Button
import webbrowser
import mapController

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
        mapPath = "gameFiles/maps/"
        imagePath = "gameFiles/images/"

        # images
        self.empty = pygame.image.load(imagePath + "empty.png").convert()
        self.bottomLeft = pygame.image.load(imagePath + "bottom_Left.png").convert()
        self.bottomRight = pygame.image.load(imagePath + "bottom_Right.png").convert()
        self.topLeft = pygame.image.load(imagePath + "top_Left.png").convert()
        self.topRight = pygame.image.load(imagePath + "top_Right.png").convert()
        self.verticalLine = pygame.image.load(imagePath + "vertical_Line.png").convert()
        self.horizontalLine = pygame.image.load(imagePath + "horizontal_line.png").convert()
        self.crossing = pygame.image.load(imagePath + "crossing.png").convert()
        self.settings = pygame.image.load(imagePath + "settings.png").convert()

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
        self.mapController = mapController.mapController(WFC=self.WFC, MC=self.mapCleaner, path=mapPath)
        #self.mapController.loadAllMaps() # load all saved maps
        self.oldMapCount = self.mapController.getCountMaps()

        self.players = []
        self.players.append(Player.Player(100, 100, 0))
        self.players.append(Player.Player(100, 200, 0))

        self.testButton = Button.Button(self.screen, 100, 100, 150, self.crossing, "generateMap")
        self.modeSelectButton = Button.Button(self.screen, 100, 300, 150, self.topRight, "selectMode")
        self.mapSelectButton = Button.Button(self.screen, 100, 500, 150, self.topLeft, "selectMap")
        self.settingsButton = Button.Button(self.screen, 1460, 40, 100, self.settings, "settings")
        self.linkButton = Button.Button(self.screen, 1450, 750, 100, self.empty, "https://github.com/DerfDa180155")
        self.quitButton = Button.Button(self.screen, 100, 700, 150, self.empty, "quit")
        self.menuButtons = [self.testButton, self.modeSelectButton, self.mapSelectButton, self.settingsButton,
                            self.linkButton, self.quitButton]

        self.singlePlayerButton = Button.Button(self.screen, 100, 100, 150, self.horizontalLine, "singleplayer")
        self.multiPlayerButton = Button.Button(self.screen, 100, 300, 150, self.crossing, "multiplayer")
        self.gameModeButtons = [self.singlePlayerButton, self.multiPlayerButton]

        self.mapButtons = []
        self.imageMapSize = 200
        self.locations = [[100, 100], [400, 100], [700, 100], [1000, 100], [1300, 100],
                     [100, 400], [400, 400], [700, 400], [1000, 400], [1300, 400],
                     [100, 700], [400, 700], [700, 700], [1000, 700], [1300, 700]]
        for i in range(self.oldMapCount):
            self.mapButtons.append(Button.Button(self.screen, self.locations[i][0], self.locations[i][1], self.imageMapSize, self.empty, str(i)))

        self.CO = CommunicationObject.CommunicationObject(gameStatus="menu", FPSClock=self.FPSClock,
                                                          TPSClock=self.TPSClock, FPS=self.FPS, TPS=self.TPS,
                                                          TextSize=30, imageArray=self.mapArray,
                                                          mapController=self.mapController, players=self.players,
                                                          menuButtons=self.menuButtons,
                                                          gameModeButtons=self.gameModeButtons,
                                                          mapButtons=self.mapButtons, currentMode="singleplayer")

        self.gameDisplay = GameDisplay.GameDisplay(screen=self.screen, CO=self.CO)
        self.gameDisplay.start()

        self.run()

    def run(self):
        # pygame setup
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Quit the Game
                    self.running = False
                    self.gameDisplay.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: # Quit the Game
                        if self.CO.gameStatus == "menu":
                            self.running = False
                            self.gameDisplay.running = False
                        elif self.CO.gameStatus == "generateMap": # only for testing
                            self.CO.gameStatus = "menu"
                        elif self.CO.gameStatus == "selectMode" or self.CO.gameStatus == "settings":
                            self.CO.gameStatus = "menu"
                        elif self.CO.gameStatus == "selectMap":
                            self.CO.gameStatus = "selectMode"
                        elif self.CO.gameStatus == "race":
                            self.CO.gameStatus = "selectMap" # for testing, will be changed in the future (with pause menu)
                    if event.key == pygame.K_m: # switch status (only for testing)
                        if self.CO.gameStatus == "menu":
                            self.CO.gameStatus = "generateMap"
                        elif self.CO.gameStatus == "generateMap":
                            self.CO.gameStatus = "menu"
                    elif event.key == pygame.K_k and self.CO.gameStatus == "generateMap":
                        x = 5
                        y = x

                        testMap = self.CO.mapController.generateNewMap(x, y)
                        print("Name: " + testMap.name + "\nMap: " + str(testMap.myMap))
                        self.CO.players[0].reset(x=testMap.playerStartX, y=testMap.playerStartY, direction=testMap.playerStartDirection)
                    elif event.key == pygame.K_l and self.CO.gameStatus == "generateMap":
                        pass # maybe no longer needed, because of the new map controller
                        #self.CO.WFC.myMap = self.mapCleaner.cleanMap(self.CO.WFC.myMap)
                        #print("cleaned Map:\n" + str(self.CO.WFC.myMap))

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
                case "selectMode":
                    for button in self.CO.gameModeButtons:
                        if button.clicked(mx, my, pygame.mouse.get_pressed()):
                            self.CO.currentMode = button.action
                            self.CO.gameStatus = "selectMap"
                            print(self.CO.currentMode)
                case "selectMap":
                    if self.oldMapCount != self.mapController.getCountMaps():
                        self.oldMapCount = self.mapController.getCountMaps()
                        self.mapButtons = []
                        for i in range(self.oldMapCount):
                            self.mapButtons.append(
                                Button.Button(self.screen, self.locations[i][0], self.locations[i][1], self.imageMapSize, self.empty, str(i)))

                    for button in self.CO.mapButtons:
                        if button.clicked(mx, my, pygame.mouse.get_pressed()):
                            self.CO.mapController.currentMapIndex = button.action
                            print(button.action)
                            self.CO.gameStatus = "race"
                            self.CO.players[0].reset(x=self.CO.mapController.getCurrentMap().playerStartX,
                                                     y=self.CO.mapController.getCurrentMap().playerStartY,
                                                     direction=self.CO.mapController.getCurrentMap().playerStartDirection)
                            self.CO.players[1].reset(x=self.CO.mapController.getCurrentMap().playerStartX,
                                                     y=self.CO.mapController.getCurrentMap().playerStartY,
                                                     direction=self.CO.mapController.getCurrentMap().playerStartDirection)
                case "race":
                    # movement keys pressed --> Update players
                    if self.CO.currentMode == "singleplayer":
                        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  # turn left
                            self.CO.players[0].changeDir(-1)
                        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:  # turn right
                            self.CO.players[0].changeDir(1)
                        if keys[pygame.K_UP] or keys[pygame.K_w]:  # move forward
                            self.CO.players[0].move(0)
                        if keys[pygame.K_DOWN] or keys[pygame.K_s]:  # move backward
                            self.CO.players[0].move(1)
                    elif self.CO.currentMode == "multiplayer":
                        i = 0
                        for player in self.CO.players:
                            if keys[pygame.K_LEFT] and i == 1 or keys[pygame.K_a] and i == 0:  # turn left
                                player.changeDir(-1)
                            if keys[pygame.K_RIGHT] and i == 1 or keys[pygame.K_d] and i == 0:  # turn right
                                player.changeDir(1)
                            if keys[pygame.K_UP] and i == 1 or keys[pygame.K_w] and i == 0:  # move forward
                                player.move(0)
                            if keys[pygame.K_DOWN] and i == 1 or keys[pygame.K_s] and i == 0:  # move backward
                                player.move(1)
                            i += 1

                    # update the players (position, speed, rays, ..)
                    for player in self.CO.players:
                        player.update()
                        # update ray length
                        player.updateRays(self.CO.mapController.getCurrentMap().boundsMap)


                    # TODO
                    # Bots movement
                    # round counter
                    # ...


            if self.CO.gameStatus == "generateMap":
                # movement keys pressed --> Update player
                if keys[pygame.K_LEFT] or keys[pygame.K_a]: # turn left
                    self.CO.players[0].changeDir(-1)
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]: # turn right
                    self.CO.players[0].changeDir(1)
                if keys[pygame.K_UP] or keys[pygame.K_w]: # move forward
                    self.CO.players[0].move(0)
                if keys[pygame.K_DOWN] or keys[pygame.K_s]: # move backward
                    self.CO.players[0].move(1)




            self.TPSClock.tick(self.CO.TPS) # limit Game Ticks

        self.gameDisplay.join()
        pygame.quit()


game = GameMain()
