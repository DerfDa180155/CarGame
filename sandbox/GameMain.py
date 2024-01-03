import pygame
import random
import os
import threading
import time
import numpy

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

        self.run()

    def run(self):
        # pygame setup
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Quit the Game
                    self.running = False

            #self.screen.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

            self.screen.blit(pygame.transform.scale(self.mapArray[random.randint(0, 4)], (self.windowWidth, self.windowHeight)), (0, 0))


            pygame.display.set_caption(str(self.TPSClock.get_fps()))
            pygame.display.flip()
            self.TPSClock.tick(self.TPS)  # limit Game Ticks


        pygame.quit()


game = GameMain()
