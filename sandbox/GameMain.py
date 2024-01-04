import pygame
import random
import os
import threading
import time
import numpy
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
        self.TPS = 3

        self.screen = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.GL_DOUBLEBUFFER)
        pygame.display.set_caption("Car Game by David Derflinger")

        self.TPSClock = pygame.time.Clock()
        self.FPSClock = pygame.time.Clock()

        self.empty = pygame.image.load("gameFiles/images/empty.png")
        self.bottomLeft = pygame.image.load("gameFiles/images/bottom_Left.png")
        self.bottomRight = pygame.image.load("gameFiles/images/bottom_Right.png")
        self.topLeft = pygame.image.load("gameFiles/images/top_Left.png")
        self.topRight = pygame.image.load("gameFiles/images/top_Right.png")

        self.mapArray = [self.empty, self.topLeft, self.topRight, self.bottomLeft, self.bottomRight]
        self.mapArrayDefinition = [[0, 0, 0, 0], # top, right, bottom, left
                                   [1, 0, 0, 1],
                                   [1, 1, 0, 0],
                                   [0, 0, 1, 1],
                                   [0, 1, 1, 0]]
        self.WFC = WaveFunctionCollapse.WaveFunctionCollapse(self.mapArray, self.mapArrayDefinition)

        self.run()

    def run(self):
        # pygame setup
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Quit the Game
                    self.running = False

            x = 10
            y = x

            a = 0
            b = 0
            testMap = []
            while a < x:
                temp = []
                b = 0
                while b < y:
                    temp.append(random.randint(0, 4))
                    b+=1
                testMap.append(temp)
                a+=1

            testMap = self.WFC.generate(x, y)

            #self.screen.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

            for i in range(len(testMap)):
                for j in range(len(testMap[i])):
                    self.screen.blit(pygame.transform.scale(self.mapArray[testMap[i][j]], ((self.windowWidth/len(testMap[i]))+1, (self.windowHeight/len(testMap))+1)), (self.windowWidth/len(testMap[i]) * j, self.windowHeight/len(testMap) * i))




            pygame.display.set_caption(str(self.TPSClock.get_fps()))
            pygame.display.flip()
            self.TPSClock.tick(self.TPS)  # limit Game Ticks


        pygame.quit()


game = GameMain()
