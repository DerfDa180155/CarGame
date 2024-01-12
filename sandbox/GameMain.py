import pygame
import random
import os
import threading
import time
import numpy
import CommunicationObject
import GameDisplay
import WaveFunctionCollapse



class GameMain:
    def __init__(self):
        pygame.init()
        pygame.display.init()

        pygame.display.gl_set_attribute(pygame.GL_ACCELERATED_VISUAL, 0)
        pygame.display.gl_set_attribute(pygame.GL_DOUBLEBUFFER, 1)

        self.running = True
        self.windowWidth = 1280
        self.windowHeight = 720

        self.FPS = 60
        self.TPS = 120

        self.screen = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.GL_DOUBLEBUFFER)
        pygame.display.set_caption("Car Game by David Derflinger")

        # clocks
        self.TPSClock = pygame.time.Clock()
        self.FPSClock = pygame.time.Clock()

        # images
        self.empty = pygame.image.load("gameFiles/images/empty.png")
        self.bottomLeft = pygame.image.load("gameFiles/images/bottom_Left.png")
        self.bottomRight = pygame.image.load("gameFiles/images/bottom_Right.png")
        self.topLeft = pygame.image.load("gameFiles/images/top_Left.png")
        self.topRight = pygame.image.load("gameFiles/images/top_Right.png")
        self.verticalLine = pygame.image.load("gameFiles/images/vertical_Line.png")
        self.horizontalLine = pygame.image.load("gameFiles/images/horizontal_line.png")
        self.crossing = pygame.image.load("gameFiles/images/crossing.png")

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





            x = 5
            y = x

            testMap = self.WFC.generate(x, y)
            print(testMap)
            print(self.WFC.countEmpty(testMap))
            #self.gameDisplay.myMap = testMap





            self.TPSClock.tick(self.CO.TPS)  # limit Game Ticks

        pygame.quit()


game = GameMain()
