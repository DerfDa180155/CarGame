import pygame
import threading
import numpy as np


class GameDisplay(threading.Thread):
    def __init__(self, screen, FPS, textSize, displayClock, gameTickClock):
        threading.Thread.__init__(self)

        self.screen = screen
        self.FPS = FPS

        self.textSize = textSize
        self.textPosition = [0, 0]

        self.displayClock = displayClock
        self.gameTickClock = gameTickClock


        self.running = True

    def run(self):
        while self.running:
            self.screen.fill("black")

            # print Text
            displayText, displayTextColor = self.generateText()
            font = pygame.font.Font(pygame.font.get_default_font(), self.textSize)
            for line in range(len(displayText)):
                text = font.render(displayText[line], True, displayTextColor[line])
                self.screen.blit(text, (self.textPosition[0], self.textPosition[1] + (line * self.textSize)))


            # update Display
            pygame.display.flip()
            self.displayClock.tick(self.FPS)  # limit FPS

    def generateText(self):
        displayText = []
        displayTextColor = []

        # FPS Display
        currentFPS = round(self.displayClock.get_fps(), 1)
        displayText.append("FPS: " + str(currentFPS))
        displayTextColor.append((0, 255, 0))

        # Game Tick Display
        currentTicks = round(self.gameTickClock.get_fps(), 1)
        displayText.append("Ticks: " + str(currentTicks))
        displayTextColor.append((0, 255, 0))



        return displayText, displayTextColor

