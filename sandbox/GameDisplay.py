import pygame
import threading
import numpy as np


class GameDisplay(threading.Thread):
    def __init__(self, screen, FPS, TPS, textSize, FPSClock, TPSClock, mapArray, WFC):
        threading.Thread.__init__(self)

        self.screen = screen
        self.FPS = FPS
        self.TPS = TPS

        self.textSize = textSize
        self.textPosition = [0, 0]

        self.FPSClock = FPSClock
        self.TPSClock = TPSClock
        self.mapArray = mapArray

        self.myMap = []
        self.windowWidth = 1280
        self.windowHeight = 720
        self.WFC = WFC

        self.running = True

    def run(self):
        while self.running:
            self.screen.fill("black")

            self.myMap = self.WFC.myMap
            # draw Map
            for i in range(len(self.myMap)):
                for j in range(len(self.myMap[i])):
                    if self.myMap[i][j] != -1:
                        #self.myMap[i][j] = 0
                        self.screen.blit(pygame.transform.scale(self.mapArray[self.myMap[i][j]], ((self.windowWidth/len(self.myMap))+1, (self.windowHeight/len(self.myMap[i]))+1)), (self.windowWidth/len(self.myMap) * i, self.windowHeight/len(self.myMap[i]) * j))


            # print Text
            displayText, displayTextColor = self.generateText()
            font = pygame.font.Font(pygame.font.get_default_font(), self.textSize)
            for line in range(len(displayText)):
                text = font.render(displayText[line], True, displayTextColor[line])
                self.screen.blit(text, (self.textPosition[0], self.textPosition[1] + (line * self.textSize)))



            # update Display
            pygame.display.flip()
            self.FPSClock.tick(self.FPS)  # limit FPS

    def generateText(self):
        displayText = []
        displayTextColor = []

        # FPS Display
        currentFPS = round(self.FPSClock.get_fps(), 1)
        diffFPS = self.FPS - currentFPS
        if diffFPS < 0:
            diffFPS = 0
        displayText.append("FPS: " + str(currentFPS))
        displayTextColor.append((diffFPS*2, 255-diffFPS*2, 0))

        # TPS Display
        currentTPS = round(self.TPSClock.get_fps(), 1)
        diffTPS = self.TPS - currentTPS
        if diffTPS < 0:
            diffTPS = 0
        displayText.append("Ticks: " + str(currentTPS))
        displayTextColor.append((diffTPS*2, 255-diffTPS*2, 30))



        return displayText, displayTextColor

