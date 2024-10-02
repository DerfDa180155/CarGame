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

        self.running = True

    def run(self):
        while self.running:
            self.windowWidth = self.screen.get_width()
            self.windowHeight = self.screen.get_height()

            match self.CO.gameStatus:
                case "menu":
                    self.drawMenu()
                case "generateMap":  # for testing
                    self.drawMap()

                    # draw Player:
                    self.drawPlayers()
                case "settings":
                    self.drawSettings()
                case "mapMaker":
                    self.drawMapMaker()
                case "selectMode":
                    self.drawModeSelector()
                case "selectCar":
                    self.drawCarSelector()
                case "selectMap":
                    self.drawMapSelector()
                case "raceSettings":
                    self.drawRaceSettings()
                case "race":
                    self.drawRace()

            # print Text
            self.drawText()

            # update Display
            pygame.display.flip()
            self.CO.FPSClock.tick(self.CO.settings.FPS)  # limit FPS

    def drawMenu(self):
        self.screen.fill((50, 200, 200))  # background

        # draw buttons
        for button in self.CO.menuButtons:
            button.draw(self.windowWidth, self.windowHeight)

    def drawSettings(self):
        self.screen.fill((200, 200, 100))  # background

        # draw menu Text
        self.drawMenuText("Settings", (255, 255, 255))

        newTextSize = int((50 * self.windowWidth) / 2000)  # scale text size
        font = pygame.font.Font(pygame.font.get_default_font(), newTextSize)

        settingsText = [["Player 1", "drive forward key: ", "drive backward key: ", "steer left key: ", "steer right key: ", "use item key: ", "pause key: ", "FPS: ", "TPS: "],
                        ["Player 2", "drive forward key: ", "drive backward key: ", "steer left key: ", "steer right key: ", "use item key: ", "Debug mode: ", "Show FPS: ", "Show TPS: "]]
        settingsData = [["", str(self.CO.displayTempSettings.playerKeys[0][0]), str(self.CO.displayTempSettings.playerKeys[0][1]),
                        str(self.CO.displayTempSettings.playerKeys[0][2]), str(self.CO.displayTempSettings.playerKeys[0][3]),
                        str(self.CO.displayTempSettings.playerKeys[0][4]), str(self.CO.displayTempSettings.pauseKey),
                        str(self.CO.displayTempSettings.FPS), str(self.CO.displayTempSettings.TPS)],
                        ["", str(self.CO.displayTempSettings.playerKeys[1][0]), str(self.CO.displayTempSettings.playerKeys[1][1]),
                         str(self.CO.displayTempSettings.playerKeys[1][2]), str(self.CO.displayTempSettings.playerKeys[1][3]),
                         str(self.CO.displayTempSettings.playerKeys[1][4]), str(self.CO.displayTempSettings.debugMode),
                         str(self.CO.displayTempSettings.displayFPS), str(self.CO.displayTempSettings.displayTPS)]]

        for i in range(len(settingsData[0])):
            # left row
            # settings Text
            text = font.render(settingsText[0][i], True, (255, 255, 255))
            newRect = text.get_rect()
            newRect.x = newTextSize
            newRect.y = 30 + newTextSize + newTextSize * (i + 1) + newTextSize * i / 2
            self.screen.blit(text, newRect)

            # settings Data
            text = font.render(settingsData[0][i], True, (255, 255, 255))
            newRect = text.get_rect()
            newRect.right = newTextSize * 17
            newRect.y = 30 + newTextSize + newTextSize * (i + 1) + newTextSize * i / 2
            self.screen.blit(text, newRect)

            # placing buttons
            if i != 0:
                self.CO.settingsButtons[i - 1 + 3].y = (newRect.y * 900) / self.windowHeight

            # right row
            if settingsText[1][i] != "":
                # settings Text
                text = font.render(settingsText[1][i], True, (255, 255, 255))
                newRect = text.get_rect()
                newRect.x = newTextSize + (self.windowWidth / 2)
                newRect.y = 30 + newTextSize + newTextSize * (i + 1) + newTextSize * i / 2
                self.screen.blit(text, newRect)

                # settings Data
                text = font.render(settingsData[1][i], True, (255, 255, 255))
                newRect = text.get_rect()
                newRect.right = newTextSize * 17 + (self.windowWidth / 2)
                newRect.y = 30 + newTextSize + newTextSize * (i + 1) + newTextSize * i / 2
                self.screen.blit(text, newRect)

                # placing buttons
                self.CO.settingsButtons[i - 1 + 3 + 8].y = (newRect.y * 900) / self.windowHeight

        # draw buttons
        for button in self.CO.settingsButtons:
            button.draw(self.windowWidth, self.windowHeight)

        if self.CO.waitForKey:
            self.drawSettingsSelectKey()

    def drawMapMaker(self):
        self.screen.fill((50, 50, 50))  # background

        self.drawMenuText("Map Maker", (255, 255, 255))

        # rectangle
        x = (100 * self.windowWidth) / 1600
        y = (100 * self.windowHeight) / 900
        sizeWidth = (1155.5 * self.windowWidth) / 1600
        sizeHeight = (650 * self.windowHeight) / 900
        rectangle = pygame.Rect(x, y, sizeWidth, sizeHeight)

        pygame.draw.rect(self.screen, (100, 200, 150), rectangle)

        # set mapMaker map position
        self.CO.mapMaker.mapPosition = [x, y, x + sizeWidth, y + sizeHeight]
        self.CO.mapMaker.mapRect = rectangle

        # draw Map name
        newTextSize = int((30 * self.windowWidth) / 2000)  # scale text size
        font = pygame.font.Font(pygame.font.get_default_font(), newTextSize)
        text = font.render("MapName: " + self.CO.mapMaker.mapName, True, (255, 255, 255))
        newRect = text.get_rect()
        newRect.centerx = self.windowWidth / 2
        newRect.y = newTextSize * 2.5
        self.screen.blit(text, newRect)

        # draw Map
        self.drawMap(self.CO.mapMaker.myMap, [x, y], [x+sizeWidth, y+sizeHeight])

        # draw grid
        gridColor = (30, 30, 30)
        lineThickness = 1
        lineThicknessScaler = 400
        scaledThickness = int((lineThickness*self.windowWidth)/lineThicknessScaler)
        lenX = len(self.CO.mapMaker.myMap)
        lenY = len(self.CO.mapMaker.myMap[0])
        sizeWidthPiece = sizeWidth/lenX
        sizeHeightPiece = sizeHeight/lenY
        for i in range(lenX + 1):
            pygame.draw.line(self.screen, gridColor, (x + (sizeWidthPiece*i), y), (x + (sizeWidthPiece*i), y + sizeHeight), scaledThickness)
        for j in range(lenY+1):
            pygame.draw.line(self.screen, gridColor, (x, y + (sizeHeightPiece*j)), (x + sizeWidth, y + (sizeHeightPiece*j)), scaledThickness)

        # draw erase mode
        state = "ON" if not self.CO.mapMaker.enablePlace else "OFF"
        eraseModeColor = (50, 150, 50) if not self.CO.mapMaker.enablePlace else (150, 50, 50)
        text = font.render("Erase mode: " + state, True, (255, 255, 255))
        newRect.x = (1300 * self.windowWidth) / 1600
        newRect.y = (700 * self.windowHeight) / 900
        pygame.draw.rect(self.screen, eraseModeColor, newRect)
        self.screen.blit(text, newRect)

        # draw new x and y
        newTextSize = int((40 * self.windowWidth) / 2000)  # scale text size
        font = pygame.font.Font(pygame.font.get_default_font(), newTextSize)
        text = font.render("x: " + str(self.CO.mapMaker.x), True, (255, 255, 255))
        newRect.x = (850 * self.windowWidth) / 1600
        newRect.y = (785 * self.windowHeight) / 900
        self.screen.blit(text, newRect)
        text = font.render("y: " + str(self.CO.mapMaker.y), True, (255, 255, 255))
        newRect.x = (850 * self.windowWidth) / 1600
        newRect.y = (830 * self.windowHeight) / 900
        self.screen.blit(text, newRect)

        # draw start x and y
        text = font.render("start x: " + str(self.CO.mapMaker.startingPiece[0] + 1), True, (255, 255, 255))
        newRect.x = (1000 * self.windowWidth) / 1600
        newRect.y = (785 * self.windowHeight) / 900
        self.screen.blit(text, newRect)
        text = font.render("start y: " + str(self.CO.mapMaker.startingPiece[1] + 1), True, (255, 255, 255))
        newRect.x = (1000 * self.windowWidth) / 1600
        newRect.y = (830 * self.windowHeight) / 900
        self.screen.blit(text, newRect)

        # draw start direction
        direction = ""
        match(self.CO.mapMaker.startingDirection):
            case 0:
                direction = "RIGHT"
            case 90:
                direction = "DOWN"
            case 180:
                direction = "LEFT"
            case 270:
                direction = "UP"
        text = font.render("start direction: " + direction, True, (255, 255, 255))
        newRect.x = (1200 * self.windowWidth) / 1600
        newRect.y = (830 * self.windowHeight) / 900
        self.screen.blit(text, newRect)

        # highlight starting piece
        if self.CO.mapMaker.highlightStartingPiece:
            # rectangle
            x = sizeWidthPiece * self.CO.mapMaker.startingPiece[0] + (100 * self.windowWidth) / 1600
            y = sizeHeightPiece * self.CO.mapMaker.startingPiece[1] + (100 * self.windowHeight) / 900

            highlight = pygame.Surface((sizeWidthPiece, sizeHeightPiece))
            highlight.fill((70, 70, 70))
            self.screen.blit(highlight, (x, y), special_flags=pygame.BLEND_RGBA_ADD)

        # dictionary for selected button
        dictionary = {
            0: "mapPiece-empty",
            1: "mapPiece-topLeft",
            2: "mapPiece-topRight",
            3: "mapPiece-bottomLeft",
            4: "mapPiece-bottomRight",
            5: "mapPiece-verticalLine",
            6: "mapPiece-horizontalLine",
        }
        dictionary2 = {
            "mapPiece-empty": 1,
            "mapPiece-topLeft": 2,
            "mapPiece-topRight": 3,
            "mapPiece-bottomLeft": 4,
            "mapPiece-bottomRight": 5,
            "mapPiece-verticalLine": 6,
            "mapPiece-horizontalLine": 7,
        }

        # draw buttons
        for button in self.CO.mapMakerButtons:
            button.draw(self.windowWidth, self.windowHeight, (button.action == dictionary[self.CO.mapMaker.selectedPiece]))

            # text
            if "mapPiece-" in button.action:
                newX = (button.x * self.windowWidth) / 1600
                newY = (button.y * self.windowHeight) / 900
                newSizeX = (button.size * self.windowWidth) / 1600
                newSizeY = (button.size * self.windowHeight) / 900
                newTextSize = int((50 * self.windowWidth) / 2000)  # scale text size
                font = pygame.font.Font(pygame.font.get_default_font(), newTextSize)
                text = font.render(str(dictionary2[button.action]), True, (255, 255, 255))
                newRect = text.get_rect()
                newRect.centerx = newX + (newSizeX / 2)
                newRect.y = newY + newSizeY
                self.screen.blit(text, newRect)

        if self.CO.mapMaker.enteringName:
            self.drawOverlay((80, 80, 80))
            text = font.render(self.CO.mapMaker.tempName, True, (255, 255, 255))
            newRect = text.get_rect()
            newRect.center = (self.windowWidth / 2, self.windowHeight / 2)
            self.screen.blit(text, newRect)

    def drawModeSelector(self):
        self.screen.fill((100, 150, 200))  # background

        # draw menu Text
        self.drawMenuText("Mode Selector", (255, 255, 255))

        # draw buttons
        for button in self.CO.gameModeButtons:
            button.draw(self.windowWidth, self.windowHeight)

    def drawCarSelector(self):
        self.screen.fill((150, 150, 100))  # background

        # draw menu Text
        self.drawMenuText("Car Selector", (255, 255, 255))

        # draw the 8 cars
        for i in range(8):
            x = 200 + i * 400
            y = 200
            if i >= 4:
                y += 300
                x -= 1600

            newX = int((x * self.windowWidth) / 1600)  # scale x
            newY = int((y * self.windowHeight) / 900)  # scale y
            size = 200
            sizeX = int((size * self.windowWidth) / 1600)
            sizeY = int((size * self.windowHeight) / 900)

            if i == self.CO.players[0].selectedCarId: # border
                pygame.draw.rect(self.screen, (50, 150, 200), (newX - (sizeX / 2), newY - (sizeY / 2), sizeX, sizeY))

            if self.CO.currentMode == "multiplayer":
                if i == self.CO.players[1].selectedCarId: # border
                    pygame.draw.rect(self.screen, (200, 150, 50),(newX - (sizeX / 2), newY - (sizeY / 2), sizeX, sizeY))

            size = 150
            sizeX = int((size * self.windowWidth) / 1600)
            sizeY = int((size * self.windowHeight) / 900)

            pygame.draw.rect(self.screen, self.CO.carSkins[i], (newX - (sizeX / 2), newY - (sizeY / 2), sizeX, sizeY))

        # draw buttons
        for button in self.CO.carSelectorButtons:
            button.draw(self.windowWidth, self.windowHeight)

    def drawMapSelector(self):
        self.screen.fill((100, 150, 250))  # background

        # draw menu Text
        self.drawMenuText("Map Selector", (255, 255, 255))

        index = 1
        if self.CO.officialMaps:
            index = 0

        # draw buttons
        for button in self.CO.mapButtons[index]:
            if button.enable:
                button.draw(self.windowWidth, self.windowHeight)
                # draw name of map on button
                newTextSize = int((self.CO.TextSize * self.windowWidth) / 2000)  # scale text size
                newX = int(((button.x + (button.size / 2)) * self.windowWidth) / 1600)  # scale x
                newY = int(((button.y + (button.size / 2)) * self.windowHeight) / 900)  # scale y
                font = pygame.font.Font(pygame.font.get_default_font(), newTextSize)
                if button.action.isnumeric():
                    text = font.render(str(self.CO.mapController.getMapArray((index == 0))[int(button.action)].name), True, (255, 255, 255))
                else:
                    if button.action == "generateMapWFC":
                        text = font.render("generate new Map", True, (255, 255, 255))
                newRect = text.get_rect()
                newRect.center = newX, newY  # center text
                self.screen.blit(text, newRect)
        for button in self.CO.mapButtons[2]:
            if button.enable:
                button.draw(self.windowWidth, self.windowHeight)
                if button.action != "return":
                    newTextSize = int((self.CO.TextSize * self.windowWidth) / 2000)  # scale text size
                    newX = int(((button.x + (button.size / 2)) * self.windowWidth) / 1600)  # scale x
                    newY = int(((button.y + (button.size*1.3)) * self.windowHeight) / 900)  # scale y
                    font = pygame.font.Font(pygame.font.get_default_font(), newTextSize)
                    text = font.render(button.action, True, (255, 255, 255))
                    newRect = text.get_rect()
                    newRect.center = newX, newY  # center text
                    self.screen.blit(text, newRect)

    def drawRaceSettings(self):
        self.screen.fill((100, 200, 200))  # background

        # display race settings
        newTextSize = int((50 * self.windowWidth) / 2000)  # scale text size
        font = pygame.font.Font(pygame.font.get_default_font(), newTextSize)

        # map name
        self.drawMenuText(self.CO.mapController.getCurrentMap(self.CO.officialMaps).name, (255, 255, 255))

        settingsText = ["Rounds: ", "MaxSpeed: ", "MaxAcc: ", "Items: ", "Items spawn cooldown: ", "Amount of Bots: "]
        settingsData = [str(self.CO.raceObject.rounds), str(self.CO.raceObject.maxSpeed), str(self.CO.raceObject.maxAcc), str(self.CO.raceObject.itemsEnabled), str(self.CO.raceObject.itemSpawnCooldown), str(self.CO.raceObject.amountOfBots)]

        for i in range(len(settingsText)):
            # settings Text
            text = font.render(settingsText[i], True, (255, 255, 255))
            newRect = text.get_rect()
            newRect.x = newTextSize
            newRect.y = 30 + newTextSize + newTextSize * (i + 1) + newTextSize * i / 2
            self.screen.blit(text, newRect)

            # settings Data
            text = font.render(settingsData[i], True, (255, 255, 255))
            newRect = text.get_rect()
            newRect.right = newTextSize * 17
            newRect.y = 30 + newTextSize + newTextSize * (i + 1) + newTextSize * i / 2
            self.screen.blit(text, newRect)

            self.CO.raceSettingsButtons[i+2].y = (newRect.y * 900) / self.windowHeight

        # map preview
        topLeft = [(870*self.windowWidth)/1600, (80*self.windowHeight)/900]
        bottomRight = [(1570*self.windowWidth)/1600, (750*self.windowHeight)/900]
        self.drawMap(self.CO.mapController.getCurrentMap(self.CO.officialMaps).myMap, topLeft, bottomRight)

        # border
        pygame.draw.line(self.screen, (0, 0, 0), topLeft, (bottomRight[0], topLeft[1]), int(newTextSize / 15)) # top
        pygame.draw.line(self.screen, (0, 0, 0), (bottomRight[0], topLeft[1]), bottomRight, int(newTextSize / 15)) # right
        pygame.draw.line(self.screen, (0, 0, 0), bottomRight, (topLeft[0], bottomRight[1]), int(newTextSize / 15)) # bottom
        pygame.draw.line(self.screen, (0, 0, 0), (topLeft[0], bottomRight[1]), topLeft, int(newTextSize / 15)) # left

        # draw buttons
        for button in self.CO.raceSettingsButtons:
            button.draw(self.windowWidth, self.windowHeight)

    def drawRace(self):
        self.screen.fill((100, 100, 250))  # background

        # draw map
        self.drawMap()

        # draw bounds (for testing)
        if self.CO.settings.debugMode:
            self.drawBoundsMap()

        # draw checkpoints (for testing)
        if self.CO.settings.debugMode:
            self.drawCheckpoints()

        # draw the finish Line
        self.drawFinishLine(15)

        # draw player stats text
        self.drawPlayerStatsText()

        # draw player items and item boxes
        if self.CO.raceObject.itemsEnabled:
            self.drawPlayerItems()
            # draw summoned items
            for item in self.CO.summonedItems:
                item.draw(self.screen)
            # draw item boxes
            for box in self.CO.itemBoxes:
                box.draw(self.screen)

        # draw player
        self.drawPlayers()

        # draw rays
        if self.CO.settings.debugMode:
            self.drawPlayerRays()

        # draw bots and bots rays
        if self.CO.raceObject.amountOfBots > 0:
            self.drawBots()
            if self.CO.settings.debugMode:
                self.drawBotRays()

        # draw starting sequenz
        if self.CO.raceObject.raceStatus == "startRace" or (
                self.CO.raceObject.raceStatus == "race" and self.CO.raceObject.drawCounter):
            self.drawStartingSequenz()

        # draw leaderboard
        if self.CO.raceObject.raceStatus == "raceOver":
            self.drawLeaderboard()
            # draw buttons
            for button in self.CO.leaderboardButtons:
                if button.action == "saveMap":
                    if self.CO.mapController.getCurrentMap(self.CO.officialMaps).name == "generatedWFC":
                        button.draw(self.windowWidth, self.windowHeight)
                else:
                    button.draw(self.windowWidth, self.windowHeight)

        # draw paused screen
        if self.CO.raceObject.raceStatus == "paused":
            self.drawPaused()
            # draw buttons
            for button in self.CO.pauseButtons:
                button.draw(self.windowWidth, self.windowHeight)

    def drawMap(self, myMap=None, topLeft=None, bottomRight=None):
        if myMap is None:
            myMap = self.CO.mapController.getCurrentMap(self.CO.officialMaps).myMap

        if topLeft is None:
            topLeft = [0, 0]
        if bottomRight is None:
            bottomRight = [self.windowWidth, self.windowHeight]
        mapWidth = bottomRight[0] - topLeft[0]
        mapHeight = bottomRight[1] - topLeft[1]

        # draw Map
        if myMap != "":
            for i in range(len(myMap)):
                for j in range(len(myMap[i])):
                    if myMap[i][j] != -1:
                        self.screen.blit(pygame.transform.scale(self.CO.imageArray[myMap[i][j]],
                                                                ((mapWidth / len(myMap)) + 1,
                                                                 (mapHeight / len(myMap[i])) + 1)),
                                         ((mapWidth / len(myMap) * i) + topLeft[0],
                                          (mapHeight / len(myMap[i]) * j) + topLeft[1]))
        else:
            self.screen.fill((50, 200, 200))

    def drawBoundsMap(self):
        boundsMap = self.CO.mapController.getCurrentMap(self.CO.officialMaps).boundsMap
        for bound in boundsMap:
            start = ((bound[0] * self.windowWidth) / 1600, (bound[1] * self.windowHeight) / 900)
            end = ((bound[2] * self.windowWidth) / 1600, (bound[3] * self.windowHeight) / 900)
            pygame.draw.line(self.screen, (255, 255, 255), start, end, 4)

    def drawCheckpoints(self):
        i = 255
        checkpoints = self.CO.mapController.getCurrentMap(self.CO.officialMaps).checkpoints
        for checkpoint in checkpoints:
            start = ((checkpoint[0] * self.windowWidth) / 1600, (checkpoint[1] * self.windowHeight) / 900)
            end = ((checkpoint[2] * self.windowWidth) / 1600, (checkpoint[3] * self.windowHeight) / 900)
            pygame.draw.line(self.screen, (i, 150, 255), start, end, 4)
            i -= 255 / len(checkpoints)

    def drawFinishLine(self, segAmount):
        finishLine = self.CO.raceObject.finishLine
        if not finishLine:
            return
        start = ((finishLine[0] * self.windowWidth) / 1600, (finishLine[1] * self.windowHeight) / 900)
        end = ((finishLine[2] * self.windowWidth) / 1600, (finishLine[3] * self.windowHeight) / 900)

        isHorizontal = (start[0] != end[0] and start[1] == end[1])

        if isHorizontal:
            length = end[0] - start[0]

            for i in range(segAmount):
                color1 = (255, 255, 255)
                color2 = (0, 0, 0)

                if i % 2 == 0:
                    color1 = (0, 0, 0)
                    color2 = (255, 255, 255)

                x = start[0] + ((length / segAmount) * i)
                y = start[1] - (length / segAmount)
                pygame.draw.rect(self.screen, color1,
                                 pygame.Rect(x, y, (length / segAmount) + 1, (length / segAmount) + 1))
                pygame.draw.rect(self.screen, color2,
                                 pygame.Rect(x, start[1], (length / segAmount) + 1, (length / segAmount) + 1))

        else:
            length = end[1] - start[1]

            for i in range(segAmount):
                color1 = (255, 255, 255)
                color2 = (0, 0, 0)

                if i % 2 == 0:
                    color1 = (0, 0, 0)
                    color2 = (255, 255, 255)

                x = start[0] - (length / segAmount)
                y = start[1] + ((length / segAmount) * i)
                pygame.draw.rect(self.screen, color1,
                                 pygame.Rect(x, y, (length / segAmount) + 1, (length / segAmount) + 1))
                pygame.draw.rect(self.screen, color2,
                                 pygame.Rect(start[0], y, (length / segAmount) + 1, (length / segAmount) + 1))

    def generateText(self):
        displayText = []
        displayTextColor = []

        # FPS Display
        if self.CO.settings.displayFPS:
            currentFPS = round(self.CO.FPSClock.get_fps(), 1)
            diffFPS = self.CO.settings.FPS - currentFPS
            if diffFPS < 0:
                diffFPS = 0
            elif diffFPS > 255 / 2:
                diffFPS = 255 / 2
            displayText.append("FPS: " + str(currentFPS))
            displayTextColor.append((diffFPS * 2, 255 - diffFPS * 2, 0))

        # TPS Display
        if self.CO.settings.displayTPS:
            currentTPS = round(self.CO.TPSClock.get_fps(), 1)
            diffTPS = self.CO.settings.TPS - currentTPS
            if diffTPS < 0:
                diffTPS = 0
            elif diffTPS > 255 / 2:
                diffTPS = 255 / 2
            displayText.append("Ticks: " + str(currentTPS))
            displayTextColor.append((diffTPS * 2, 255 - diffTPS * 2, 0))

        # status Display
        if self.CO.settings.debugMode:
            displayText.append("Status: " + self.CO.gameStatus)
            displayTextColor.append((255, 255, 0))

        # stopwatch Display
        if self.CO.gameStatus == "race":
            nanoSeconds = self.CO.raceObject.stopwatch
            seconds = int((nanoSeconds / 1000000000))
            minutes = int(seconds / 60)
            displayText.append("Time: " + str(minutes).zfill(2) + ":" + str(seconds % 60).zfill(2) + ":" + str(
                int((nanoSeconds / 1000000) % 1000)).zfill(3))
            displayTextColor.append((255, 255, 0))

        return displayText, displayTextColor

    def drawText(self):
        newTextSize = int((self.CO.TextSize * self.windowWidth) / 2000)
        displayText, displayTextColor = self.generateText()
        font = pygame.font.Font(pygame.font.get_default_font(), newTextSize)
        for line in range(len(displayText)):
            text = font.render(displayText[line], True, displayTextColor[line])
            self.screen.blit(text, (self.textPosition[0], self.textPosition[1] + (line * newTextSize)))

    def drawMenuText(self, menuText, color = (255, 255, 255)):
        newTextSize = int((50 * self.windowWidth) / 2000)  # scale text size
        font = pygame.font.Font(pygame.font.get_default_font(), newTextSize)
        text = font.render(menuText, True, color)
        newRect = text.get_rect()
        newRect.centerx = self.windowWidth / 2
        newRect.y = newTextSize * 0.5
        self.screen.blit(text, newRect)

    def drawPlayerStatsText(self):
        newTextSize = int((40 * self.windowWidth) / 2000)

        # rounds
        text = str(self.CO.raceObject.playerRoundsList[0]) + " / " + str(self.CO.raceObject.rounds)
        font = pygame.font.Font(pygame.font.get_default_font(), newTextSize)
        text = font.render(text, True, (255, 255, 255))
        newRect = text.get_rect()
        newRect.bottomleft = (newTextSize / 5, self.windowHeight)
        self.screen.blit(text, newRect)  # rounds

        # speed
        text = str(round(self.CO.players[0].speed, 1)) + " / " + str(round(self.CO.players[0].currentMaxSpeed, 1))
        text = font.render(text, True, (255, 255, 255))
        newRect = text.get_rect()
        newRect.bottomleft = (newTextSize / 5, self.windowHeight - newTextSize)
        self.screen.blit(text, newRect)  # speed

        if self.CO.raceObject.mode == "multiplayer":
            # rounds
            text = str(self.CO.raceObject.playerRoundsList[1]) + " / " + str(self.CO.raceObject.rounds)
            font = pygame.font.Font(pygame.font.get_default_font(), newTextSize)
            text = font.render(text, True, (255, 255, 255))
            # self.screen.blit(text, (positionX, positionY))
            newRect = text.get_rect()
            newRect.bottomright = (self.windowWidth - (newTextSize / 5), self.windowHeight)
            self.screen.blit(text, newRect)  # rounds

            # speed
            text = str(round(self.CO.players[1].speed, 1)) + " / " + str(round(self.CO.players[1].currentMaxSpeed, 1))
            text = font.render(text, True, (255, 255, 255))
            newRect = text.get_rect()
            newRect.bottomright = (self.windowWidth - (newTextSize / 5), self.windowHeight - newTextSize)
            self.screen.blit(text, newRect)  # speed

    def drawPlayerItems(self):
        newTextSize = int((40 * self.windowWidth) / 2000)
        x = newTextSize / 5
        y = self.windowHeight - (newTextSize * 5)
        sizeWidth = newTextSize * 2.5
        sizeHeight = sizeWidth
        rectangle = pygame.Rect(x, y, sizeWidth, sizeHeight)
        pygame.draw.rect(self.screen, (128, 128, 128), rectangle)
        # draw Item image
        if self.CO.players[0].currentItem != -1:
            self.screen.blit(pygame.transform.scale(self.CO.itemImageDictionary[self.CO.players[0].currentItem],
                                                    (sizeHeight-(newTextSize/3), sizeWidth-(newTextSize/3))),
                             (x+(newTextSize/6), y+(newTextSize/6)))
        #else:
        #    self.screen.blit(pygame.transform.scale(self.CO.itemImageDictionary[0],
        #                                            (sizeHeight-(newTextSize/3), sizeWidth-(newTextSize/3))),
        #                     (x+(newTextSize/6), y+(newTextSize/6)))

        if self.CO.raceObject.mode == "multiplayer":
            x = (self.windowWidth - (newTextSize / 5)) - newTextSize * 2.5
            y = self.windowHeight - (newTextSize * 5)
            sizeWidth = newTextSize * 2.5
            sizeHeight = sizeWidth
            rectangle = pygame.Rect(x, y, sizeWidth, sizeHeight)
            pygame.draw.rect(self.screen, (128, 128, 128), rectangle)
            # draw Item image
            if self.CO.players[1].currentItem != -1:
                self.screen.blit(pygame.transform.scale(self.CO.itemImageDictionary[self.CO.players[1].currentItem],
                                                        (sizeHeight - (newTextSize / 3), sizeWidth - (newTextSize / 3))),
                                 (x + (newTextSize / 6), y + (newTextSize / 6)))
            #else:
            #    self.screen.blit(pygame.transform.scale(self.CO.itemImageDictionary[0],
            #                                            (sizeHeight - (newTextSize / 3), sizeWidth - (newTextSize / 3))),
            #                     (x + (newTextSize / 6), y + (newTextSize / 6)))

    def drawLeaderboard(self):
        # dark overlay
        self.drawOverlay((70, 70, 70))

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

        # map name
        text = font.render(self.CO.mapController.getCurrentMap(self.CO.officialMaps).name, True, (255, 255, 255))
        newRect = text.get_rect()
        newRect.centerx = rectangle.centerx
        newRect.y = rectangle.y + (newTextSize / 2) + newTextSize
        self.screen.blit(text, newRect)

        i = 0
        for entry in self.CO.raceObject.leaderboard:
            color = (255, 255, 255)
            if entry[0] < 100:
                for player in self.CO.players:
                    if player.id == entry[0]:
                        color = player.color
                text = font.render("Player " + str(entry[0]), True, color)
            else:
                for bot in self.CO.bots:
                    if bot.player.id == entry[0]:
                        color = bot.player.color
                text = font.render("Bot " + str(entry[0] - 100), True, color)
            newRect = text.get_rect()
            newRect.x = rectangle.x + (newTextSize / 2)
            newRect.y = rectangle.y + (newTextSize * (3 + i))
            self.screen.blit(text, newRect)

            nanoSec = entry[1]
            seconds = int((nanoSec / 1000000000))
            minutes = int(seconds / 60)

            timeText = str(minutes).zfill(2) + ":" + str(seconds % 60).zfill(2) + ":" + str(
                int((nanoSec / 1000000) % 1000)).zfill(3)

            text = font.render(timeText, True, color)
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
        # dark overlay
        self.drawOverlay((100, 100, 100))

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

        # map name
        text = font.render(self.CO.mapController.getCurrentMap(self.CO.officialMaps).name, True, (255, 255, 255))
        newRect = text.get_rect()
        newRect.centerx = rectangle.centerx
        newRect.y = rectangle.y + (newTextSize / 2) + newTextSize
        self.screen.blit(text, newRect)

        # race settings
        settingsText = ["Rounds: ", "MaxSpeed: ", "MaxAcc: ", "Items: ", "Items spawn cooldown: ", "Amount of Bots: "]
        settingsData = [str(self.CO.raceObject.rounds), str(self.CO.raceObject.maxSpeed),
                        str(self.CO.raceObject.maxAcc), str(self.CO.raceObject.itemsEnabled),
                        str(self.CO.raceObject.itemSpawnCooldown), str(self.CO.raceObject.amountOfBots)]
        newTextSize = int((30 * self.windowWidth) / 2000)
        font = pygame.font.Font(pygame.font.get_default_font(), newTextSize)
        x = (430 * self.windowWidth) / 1600
        y = (300 * self.windowHeight) / 900
        for i in range(len(settingsText)):
            # settings Text
            text = font.render(settingsText[i], True, (255, 255, 255))
            newRect = text.get_rect()
            newRect.x = x
            newRect.y = y + newTextSize + newTextSize * (i + 1) + newTextSize * i / 2
            self.screen.blit(text, newRect)

            # settings Data
            text = font.render(settingsData[i], True, (255, 255, 255))
            newRect = text.get_rect()
            newRect.right = x + newTextSize * 16
            newRect.y = y + newTextSize + newTextSize * (i + 1) + newTextSize * i / 2
            self.screen.blit(text, newRect)

    def drawSettingsSelectKey(self):
        # dark overlay
        self.drawOverlay((100, 100, 100))

        # rectangle
        x = (580 * self.windowWidth) / 1600
        y = (410 * self.windowHeight) / 900
        sizeWidth = (440 * self.windowWidth) / 1600
        sizeHeight = (80 * self.windowHeight) / 900
        rectangle = pygame.Rect(x, y, sizeWidth, sizeHeight)

        pygame.draw.rect(self.screen, (128, 128, 128), rectangle)

        # text
        newTextSize = int((50 * self.windowWidth) / 2000)
        font = pygame.font.Font(pygame.font.get_default_font(), newTextSize)

        # map name
        text = font.render("Press a key to select!", True, (255, 255, 255))
        newRect = text.get_rect()
        newRect.centerx = rectangle.centerx
        newRect.centery = rectangle.centery
        self.screen.blit(text, newRect)

    def drawOverlay(self, color):
        # dark overlay
        dark = pygame.Surface((self.windowWidth, self.windowHeight))
        dark.fill(color)
        self.screen.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

    def drawPlayers(self):
        i = 0
        for player in self.CO.players:
            if (self.CO.currentMode == "singleplayer" and i == 0) or self.CO.currentMode == "multiplayer":
                x = (player.x * self.windowWidth) / player.scaleWidth
                y = (player.y * self.windowHeight) / player.scaleHeight
                playerSizeWidth = (20 * self.windowWidth) / player.scaleSizeWidth
                playerSizeHeight = (20 * self.windowHeight) / player.scaleSizeHeight

                # shield item
                if self.CO.raceObject.itemsEnabled and player.shieldTime > 0:
                    pygame.draw.circle(self.screen, (10, 150, 200), (x, y), playerSizeWidth, 0)

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

    def drawBots(self):
        for bot in self.CO.bots:
            x = (bot.player.x * self.windowWidth) / bot.player.scaleWidth
            y = (bot.player.y * self.windowHeight) / bot.player.scaleHeight
            playerSizeWidth = (20 * self.windowWidth) / bot.player.scaleSizeWidth
            playerSizeHeight = (20 * self.windowHeight) / bot.player.scaleSizeHeight

            # shield item
            if self.CO.raceObject.itemsEnabled and bot.player.shieldTime > 0:
                pygame.draw.circle(self.screen, (10, 150, 200), (x, y), playerSizeWidth, 0)

            pygame.draw.rect(self.screen, bot.player.color,
                             pygame.Rect(x - (playerSizeWidth / 2), y - (playerSizeHeight / 2),
                                         playerSizeWidth, playerSizeHeight))

    def drawBotRays(self):
        for bot in self.CO.bots:
            for ray in bot.player.frontRays:
                rayLengthX = (ray.length * self.windowWidth) / 1600
                rayLengthY = (ray.length * self.windowHeight) / 900
                x1 = (bot.player.x * self.windowWidth) / bot.player.scaleWidth
                y1 = (bot.player.y * self.windowHeight) / bot.player.scaleHeight
                x2 = x1 + rayLengthX * np.cos(np.deg2rad(ray.direction))
                y2 = y1 + rayLengthY * np.sin(np.deg2rad(ray.direction))
                pygame.draw.line(self.screen, bot.player.color, (x1, y1), (x2, y2), 4)
