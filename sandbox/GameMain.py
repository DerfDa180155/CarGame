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

class GameMain:
    def __init__(self):
        pygame.init()
        pygame.display.init()

        pygame.display.gl_set_attribute(pygame.GL_ACCELERATED_VISUAL, 0)
        pygame.display.gl_set_attribute(pygame.GL_DOUBLEBUFFER, 1)

        self.running = True
        self.windowWidth = 1280
        self.windowHeight = 720

        self.FPS = 144
        self.TPS = 120

        self.screen = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.RESIZABLE | pygame.GL_DOUBLEBUFFER)
        pygame.display.set_caption("Car Game by David Derflinger")

        # clocks
        self.TPSClock = pygame.time.Clock()
        self.FPSClock = pygame.time.Clock()

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

        self.Player = Player.Player(100, 100, 0)

        self.modeSelectButton = Button.Button(self.screen, 100, 100, 200, self.crossing, "generateMap")
        self.settingsButton = Button.Button(self.screen, 1460, 40, 100, self.settings, "settings")
        self.linkButton = Button.Button(self.screen, 1450, 750, 100, self.empty, "https://github.com/DerfDa180155")
        self.menuButtons = [self.modeSelectButton, self.settingsButton, self.linkButton]

        self.CO = CommunicationObject.CommunicationObject(gameStatus="menu", FPSClock=self.FPSClock,
                                                          TPSClock=self.TPSClock, FPS=self.FPS, TPS=self.TPS,
                                                          TextSize=30, imageArray=self.mapArray, WFC=self.WFC,
                                                          Player=self.Player, menuButtons=self.menuButtons)

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
                        self.running = False
                        self.gameDisplay.running = False
                    if event.key == pygame.K_m: # switch status
                        if self.CO.gameStatus == "menu":
                            self.CO.gameStatus = "generateMap"
                        elif self.CO.gameStatus == "generateMap":
                            self.CO.gameStatus = "menu"
                    elif event.key == pygame.K_k and self.CO.gameStatus == "generateMap":
                        x = 4
                        y = x

                        testMap = self.CO.WFC.generate(x, y)
                        print(testMap)
                        print(self.CO.WFC.countEmpty(testMap))
                        # self.gameDisplay.myMap = testMap
                    elif event.key == pygame.K_l and self.CO.gameStatus == "generateMap":
                        self.CO.WFC.myMap = self.mapCleaner.cleanMap(self.CO.WFC.myMap)
                        print("cleaned Map:\n" + str(self.CO.WFC.myMap))

            mx, my = pygame.mouse.get_pos()

            match self.CO.gameStatus:
                case "menu":
                    for button in self.CO.menuButtons:
                        if button.clicked(mx, my, pygame.mouse.get_pressed()):
                            if "https://" in button.action:
                                if not button.hadAction:
                                    button.hadAction = True
                                    webbrowser.open(button.action)
                            else:
                                self.CO.gameStatus = button.action


            # get pressed Keys
            keys = pygame.key.get_pressed()

            if self.CO.gameStatus == "generateMap":
                # movement keys pressed --> Update player
                if keys[pygame.K_LEFT] or keys[pygame.K_a]: # turn left
                    self.CO.Player.changeDir(-1)
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]: # turn right
                    self.CO.Player.changeDir(1)
                if keys[pygame.K_UP] or keys[pygame.K_w]: # move forward
                    self.CO.Player.move(0)
                if keys[pygame.K_DOWN] or keys[pygame.K_s]: # move backward
                    self.CO.Player.move(1)




            self.TPSClock.tick(self.CO.TPS) # limit Game Ticks

        self.gameDisplay.join()
        pygame.quit()


game = GameMain()
