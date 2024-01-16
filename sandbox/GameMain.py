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

        self.screen = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.GL_DOUBLEBUFFER)
        pygame.display.set_caption("Car Game by David Derflinger")

        # clocks
        self.TPSClock = pygame.time.Clock()
        self.FPSClock = pygame.time.Clock()

        imagePath = "gameFiles/images/"

        # images
        self.empty = pygame.image.load(imagePath + "empty.png")
        self.bottomLeft = pygame.image.load(imagePath + "bottom_Left.png")
        self.bottomRight = pygame.image.load(imagePath + "bottom_Right.png")
        self.topLeft = pygame.image.load(imagePath + "top_Left.png")
        self.topRight = pygame.image.load(imagePath + "top_Right.png")
        self.verticalLine = pygame.image.load(imagePath + "vertical_Line.png")
        self.horizontalLine = pygame.image.load(imagePath + "horizontal_line.png")
        self.crossing = pygame.image.load(imagePath + "crossing.png")

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

        self.CO = CommunicationObject.CommunicationObject(gameStatus="menu", FPSClock=self.FPSClock,
                                                          TPSClock=self.TPSClock, FPS=self.FPS, TPS=self.TPS,
                                                          TextSize=40, imageArray=self.mapArray, WFC=self.WFC)

        self.gameDisplay = GameDisplay.GameDisplay(screen=self.screen, CO=self.CO)
        self.gameDisplay.start()

        self.run()

    def run(self):
        # pygame setup
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Quit the Game
                    self.running = False
                    self.gameDisplay.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m: # switch status
                        if self.CO.gameStatus == "menu":
                            self.CO.gameStatus = "generateMap"
                        elif self.CO.gameStatus == "generateMap":
                            self.CO.gameStatus = "menu"
                    elif event.key == pygame.K_k and self.CO.gameStatus == "generateMap":
                        x = 20
                        y = x

                        testMap = self.CO.WFC.generate(x, y)
                        print(testMap)
                        print(self.CO.WFC.countEmpty(testMap))
                        # self.gameDisplay.myMap = testMap
                    elif event.key == pygame.K_l and self.CO.gameStatus == "generateMap":
                        self.CO.WFC.myMap = self.mapCleaner.cleanMap(self.CO.WFC.myMap)
                        print("cleaned Map:\n" + str(self.CO.WFC.myMap))





            self.TPSClock.tick(self.CO.TPS)  # limit Game Ticks

        pygame.quit()


game = GameMain()
