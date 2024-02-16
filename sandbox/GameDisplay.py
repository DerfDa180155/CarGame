import pygame
import threading
import numpy as np
import CommunicationObject


class GameDisplay(threading.Thread):
    def __init__(self, screen, CO: CommunicationObject):
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

            self.windowWidth = self.screen.get_width()
            self.windowHeight = self.screen.get_height()
            # self.hs = pygame.Surface((self.windowWidth, self.windowHeight), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.OPENGL)

            match self.CO.gameStatus:
                case "menu":
                    self.drawMenu()
                case "generateMap": # for testing
                    self.drawMap()

                    # draw Player:
                    self.drawPlayers()
                case "settings":
                    self.drawSettings()
                case "selectMode":
                    self.drawModeSelector()
                case "selectMap":
                    self.drawMapSelector()
                case "race":
                    self.drawRace()

            # print Text
            self.drawText()
            #self.screen.blit(self.hs, (0, 0))

            # update Display
            pygame.display.flip()
            self.CO.FPSClock.tick(self.CO.FPS)  # limit FPS

    def drawMenu(self):
        self.screen.fill((50, 200, 200)) # background

        # draw buttons
        for button in self.CO.menuButtons:
            button.draw(self.windowWidth, self.windowHeight)

    def drawSettings(self):
        self.screen.fill((200, 200, 100)) # background

    def drawModeSelector(self):
        self.screen.fill((100, 150, 200)) # background

        # draw buttons
        for button in self.CO.gameModeButtons:
            button.draw(self.windowWidth, self.windowHeight)

    def drawMapSelector(self):
        self.screen.fill((100, 150, 250)) # background

        # draw buttons
        for button in self.CO.mapButtons:
            button.draw(self.windowWidth, self.windowHeight)

    def drawRace(self):
        self.screen.fill((100, 100, 250))  # background

        # draw map
        self.drawMap()

        # draw bounds (for testing)
        self.drawBoundsMap()

        # draw checkpoints (for testing)
        self.drawCheckpoints()

        # draw text
        self.drawRoundsText()

        # draw player
        self.drawPlayers()

        # draw rays
        self.drawPlayerRays()

        # draw starting sequenz
        if self.CO.raceObject.raceStatus == "startRace":
            self.drawStartingSequenz()

        # draw leaderboard
        if self.CO.raceObject.raceStatus == "raceOver":
            self.drawLeaderboard()
            # draw buttons
            for button in self.CO.leaderboardButtons:
                button.draw(self.windowWidth, self.windowHeight)

        # draw paused screen
        if self.CO.raceObject.raceStatus == "paused":
            self.drawPaused()
            # draw buttons
            for button in self.CO.pauseButtons:
                button.draw(self.windowWidth, self.windowHeight)

    def drawMap(self):
        self.myMap = self.CO.mapController.getCurrentMap().myMap
        # draw Map
        if self.myMap != "":
            for i in range(len(self.myMap)):
                for j in range(len(self.myMap[i])):
                    if self.myMap[i][j] != -1:
                        # self.myMap[i][j] = 0
                        self.screen.blit(pygame.transform.scale(self.CO.imageArray[self.myMap[i][j]],
                                                                ((self.windowWidth / len(self.myMap)) + 1,
                                                                 (self.windowHeight / len(self.myMap[i])) + 1)),
                                         (self.windowWidth / len(self.myMap) * i,
                                          self.windowHeight / len(self.myMap[i]) * j))
        else:
            self.screen.fill((50, 200, 200))

    def drawBoundsMap(self):
        boundsMap = self.CO.mapController.getCurrentMap().boundsMap
        for bound in boundsMap:
            start = ((bound[0] * self.windowWidth) / 1600, (bound[1] * self.windowHeight) / 900)
            end = ((bound[2] * self.windowWidth) / 1600, (bound[3] * self.windowHeight) / 900)
            pygame.draw.line(self.screen, (255, 255, 255), start, end, 4)

    def drawCheckpoints(self):
        i = 255
        checkpoints = self.CO.mapController.getCurrentMap().checkpoints
        for checkpoint in checkpoints:
            start = ((checkpoint[0] * self.windowWidth) / 1600, (checkpoint[1] * self.windowHeight) / 900)
            end = ((checkpoint[2] * self.windowWidth) / 1600, (checkpoint[3] * self.windowHeight) / 900)
            pygame.draw.line(self.screen, (i, 150, 255), start, end, 4)
            i -= 255 / len(checkpoints)

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

        # stopwatch Display
        if self.CO.gameStatus == "race":
            nanoSeconds = self.CO.raceObject.stopwatch
            seconds = int((nanoSeconds / 1000000000))
            minutes = int(seconds/60)
            displayText.append("Time: " + str(minutes).zfill(2) + ":" + str(seconds%60).zfill(2) + ":" + str(int((nanoSeconds/1000000)%1000)).zfill(3))
            displayTextColor.append((255, 255, 0))

        return displayText, displayTextColor

    def drawText(self):
        newTextSize = int((self.CO.TextSize * self.windowWidth) / 2000)
        displayText, displayTextColor = self.generateText()
        font = pygame.font.Font(pygame.font.get_default_font(), newTextSize)
        for line in range(len(displayText)):
            text = font.render(displayText[line], True, displayTextColor[line])
            self.screen.blit(text, (self.textPosition[0], self.textPosition[1] + (line * newTextSize)))

    def drawRoundsText(self):
        newTextSize = int((40 * self.windowWidth) / 2000)
        text = str(self.CO.raceObject.playerRoundsList[0]) + " / " + str(self.CO.raceObject.maxRounds)

        font = pygame.font.Font(pygame.font.get_default_font(), newTextSize)
        text = font.render(text, True, (255, 255, 255))
        #self.screen.blit(text, (positionX, positionY))
        newRect = text.get_rect()
        newRect.bottomleft = (newTextSize/5, self.windowHeight)
        self.screen.blit(text, newRect)


        if self.CO.raceObject.mode == "multiplayer":
            text = str(self.CO.raceObject.playerRoundsList[1]) + " / " + str(self.CO.raceObject.maxRounds)

            font = pygame.font.Font(pygame.font.get_default_font(), newTextSize)
            text = font.render(text, True, (255, 255, 255))
            #self.screen.blit(text, (positionX, positionY))
            newRect = text.get_rect()
            newRect.bottomright = (self.windowWidth - (newTextSize / 5), self.windowHeight)
            self.screen.blit(text, newRect)

    def drawLeaderboard(self):
        # rectangle
        x = (400 * self.windowWidth) / 1600
        y = (200 * self.windowHeight) / 900
        sizeWidth = (800 * self.windowWidth) / 1600
        sizeHeight = (500 * self.windowHeight) / 900
        rectangle = pygame.Rect(x, y, sizeWidth, sizeHeight)

        pygame.draw.rect(self.screen, (128, 128, 128), rectangle)

        # text
        newTextSize = int((50 * self.windowWidth) / 2000)
        font = pygame.font.Font(pygame.font.get_default_font(), newTextSize)

        text = font.render("Leaderboard", True, (255, 255, 255))
        newRect = text.get_rect()
        newRect.centerx = rectangle.centerx
        newRect.y = rectangle.y + (newTextSize / 2)
        self.screen.blit(text, newRect)

        i = 0
        for entry in self.CO.raceObject.leaderboard:
            text = font.render("Player " + str(entry[0]), True, (255, 255, 255))
            newRect = text.get_rect()
            newRect.x = rectangle.x + (newTextSize / 2)
            newRect.y = rectangle.y + (newTextSize * (3 + i))
            self.screen.blit(text, newRect)

            nanoSec = entry[1]
            seconds = int((nanoSec / 1000000000))
            minutes = int(seconds / 60)

            timeText = str(minutes).zfill(2) + ":" + str(seconds % 60).zfill(2) + ":" + str(int((nanoSec / 1000000) % 1000)).zfill(3)


            text = font.render(timeText, True, (255, 255, 255))
            newRect = text.get_rect()
            newRect.right = rectangle.right - (newTextSize / 2)
            newRect.y = rectangle.y + (newTextSize * (3 + i))
            self.screen.blit(text, newRect)

            i += 1

    def drawStartingSequenz(self):
        # text
        newTextSize = int((500 * self.windowWidth) / 2000)
        font = pygame.font.Font(pygame.font.get_default_font(), newTextSize)

        text = font.render(self.CO.raceObject.countDown, True, (255, 255, 255))
        newRect = text.get_rect()
        newRect.center = (self.windowWidth / 2), (self.windowHeight / 2)
        self.screen.blit(text, newRect)

    def drawPaused(self):
        # rectangle
        x = (400 * self.windowWidth) / 1600
        y = (200 * self.windowHeight) / 900
        sizeWidth = (800 * self.windowWidth) / 1600
        sizeHeight = (500 * self.windowHeight) / 900
        rectangle = pygame.Rect(x, y, sizeWidth, sizeHeight)

        pygame.draw.rect(self.screen, (128, 128, 128), rectangle)

        # text
        newTextSize = int((50 * self.windowWidth) / 2000)
        font = pygame.font.Font(pygame.font.get_default_font(), newTextSize)

        text = font.render("Paused", True, (255, 255, 255))
        newRect = text.get_rect()
        newRect.centerx = rectangle.centerx
        newRect.y = rectangle.y + (newTextSize / 2)
        self.screen.blit(text, newRect)


    def drawPlayers(self):
        i = 0
        for player in self.CO.players:
            if (self.CO.currentMode == "singleplayer" and i == 0) or self.CO.currentMode == "multiplayer":
                x = (player.x * self.windowWidth) / player.scaleWidth
                y = (player.y * self.windowHeight) / player.scaleHeight
                playerSizeWidth = (20 * self.windowWidth) / player.scaleSizeWidth
                playerSizeHeight = (20 * self.windowHeight) / player.scaleSizeHeight
                pygame.draw.rect(self.screen, player.color,
                                 pygame.Rect(x - (playerSizeWidth / 2), y - (playerSizeHeight / 2),
                                             playerSizeWidth, playerSizeHeight))
            i += 1

    def drawPlayerRays(self):
        i = 0
        for player in self.CO.players:
            if (self.CO.currentMode == "singleplayer" and i == 0) or self.CO.currentMode == "multiplayer":
                for ray in player.frontRays:
                    rayLengthX = (ray.length * self.windowWidth) / 1600
                    rayLengthY = (ray.length * self.windowHeight) / 900
                    x1 = (player.x * self.windowWidth) / player.scaleWidth
                    y1 = (player.y * self.windowHeight) / player.scaleHeight
                    x2 = x1 + rayLengthX * np.cos(np.deg2rad(ray.direction))
                    y2 = y1 + rayLengthY * np.sin(np.deg2rad(ray.direction))
                    pygame.draw.line(self.screen, player.color, (x1, y1), (x2, y2), 4)
            i += 1


