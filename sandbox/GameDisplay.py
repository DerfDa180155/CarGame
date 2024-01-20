import pygame
import threading
import numpy as np


class GameDisplay(threading.Thread):
    def __init__(self, screen, CO):
        threading.Thread.__init__(self)

        self.screen = screen
        self.CO = CO

        self.textPosition = [0, 0]

        self.myMap = []
        self.windowWidth = self.screen.get_width()
        self.windowHeight = self.screen.get_height()

        #self.hs = pygame.Surface((self.windowWidth, self.windowHeight), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.OPENGL)

        self.running = True

    def run(self):
        while self.running:
            self.screen.fill("black")
            self.windowWidth = self.screen.get_width()
            self.windowHeight = self.screen.get_height()
            #self.hs = pygame.Surface((self.windowWidth, self.windowHeight), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.OPENGL)

            self.myMap = self.CO.WFC.myMap
            # draw Map
            for i in range(len(self.myMap)):
                for j in range(len(self.myMap[i])):
                    if self.myMap[i][j] != -1:
                        #self.myMap[i][j] = 0
                        self.screen.blit(pygame.transform.scale(self.CO.imageArray[self.myMap[i][j]],
                                                                ((self.windowWidth/len(self.myMap))+1,
                                                                 (self.windowHeight/len(self.myMap[i]))+1)),
                                         (self.windowWidth/len(self.myMap) * i, self.windowHeight/len(self.myMap[i]) * j))


            # print Text
            self.drawText()

            # print Player:
            self.drawPlayer()

            #self.screen.blit(self.hs, (0, 0))

            # update Display
            pygame.display.flip()
            self.CO.FPSClock.tick(self.CO.FPS)  # limit FPS

    def generateText(self):
        displayText = []
        displayTextColor = []

        # FPS Display
        currentFPS = round(self.CO.FPSClock.get_fps(), 1)
        diffFPS = self.CO.FPS - currentFPS
        if diffFPS < 0:
            diffFPS = 0
        elif diffFPS > 255/2:
            diffFPS = 255/2
        displayText.append("FPS: " + str(currentFPS))
        displayTextColor.append((diffFPS*2, 255-diffFPS*2, 0))

        # TPS Display
        currentTPS = round(self.CO.TPSClock.get_fps(), 1)
        diffTPS = self.CO.TPS - currentTPS
        if diffTPS < 0:
            diffTPS = 0
        elif diffTPS > 255 / 2:
            diffTPS = 255 / 2
        displayText.append("Ticks: " + str(currentTPS))
        displayTextColor.append((diffTPS*2, 255-diffTPS*2, 0))

        # status Display
        displayText.append("Status: " + self.CO.gameStatus)
        displayTextColor.append((255, 255, 0))

        return displayText, displayTextColor

    def drawText(self):
        newTextSize = int((self.CO.TextSize * self.windowWidth) / 2000)
        displayText, displayTextColor = self.generateText()
        font = pygame.font.Font(pygame.font.get_default_font(), newTextSize)
        for line in range(len(displayText)):
            text = font.render(displayText[line], True, displayTextColor[line])
            self.screen.blit(text, (self.textPosition[0], self.textPosition[1] + (line * newTextSize)))

    def drawPlayer(self):
        x = (self.CO.Player.x * self.windowWidth) / self.CO.Player.scaleWidth
        y = (self.CO.Player.y * self.windowHeight) / self.CO.Player.scaleHeight
        playerSizeWidth = (20 * self.windowWidth) / self.CO.Player.scaleSizeWidth
        playerSizeHeight = (20 * self.windowHeight) / self.CO.Player.scaleSizeHeight
        pygame.draw.rect(self.screen, (255, 255, 255),
                         pygame.Rect(x - (playerSizeWidth / 2), y - (playerSizeHeight / 2),
                                     playerSizeWidth, playerSizeHeight))