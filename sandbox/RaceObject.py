import random

import numpy as np
import time
import array
import RaceMap
import ItemBox
import Bot
import Player


class RaceObject:
    def __init__(self, players: array, bots: array, raceMap: RaceMap, amountOfItems: int, summonedItems: array, itemBoxes: array):
        self.stopwatch = 0
        self.stopwatchCurrentTime = 0
        self.stopwatchStart = 0
        self.stopwatchRunning = False

        self.raceMap = raceMap
        self.raceStatus = "noRace"
        self.mode = "singleplayer"

        self.defaultRounds = 0
        self.defaultMaxSpeed = 150
        self.defaultMaxAcc = 30
        self.defaultItemsEnabled = False
        self.defaultItemSpawnCooldown = 240
        self.defaultAmountOfBots = 0

        self.rounds = self.defaultRounds
        self.maxSpeed = self.defaultMaxSpeed
        self.maxAcc = self.defaultMaxAcc
        self.itemsEnabled = self.defaultItemsEnabled
        self.itemSpawnCooldown = self.defaultItemSpawnCooldown
        self.amountOfBots = self.defaultAmountOfBots
        self.amountOfItems = amountOfItems
        self.summonedItems = summonedItems
        self.itemBoxes = itemBoxes

        self.checkpointsPerRounds = len(self.raceMap.checkpoints)

        self.players = players
        self.bots = bots
        self.allPlayers = []
        self.generateAllPlayers()

        self.playerCheckpointList = {}
        self.playerRoundsList = {}
        for player in self.allPlayers:
            self.playerRoundsList[player.id] = 0

        self.leaderboard = []
        self.finishLine = []

        self.countDown = "-"
        self.drawCounter = False

    def togglePause(self):
        if self.raceStatus == "race":
            self.stop()
        elif self.raceStatus == "paused":
            self.resume()

    def start(self, raceMap: RaceMap):
        if self.rounds > 0: # only start wenn the race settings are set
            self.raceMap = raceMap
            self.raceStatus = "startRace"
            self.startingSequenzTimer = time.time_ns()

            self.drawCounter = True

            self.generateAllPlayers()
            self.playerRoundsList = {}
            for player in self.allPlayers:
                self.playerRoundsList[player.id] = 0

            # position players and create checkpoints list
            self.playerCheckpointList = {}
            playerCounter = 0
            for player in self.allPlayers:
                player.reset(self.raceMap.startPositions[playerCounter][0], self.raceMap.startPositions[playerCounter][1], self.raceMap.playerStartDirection)
                player.maxSpeed = self.maxSpeed
                player.maxAcc = self.maxAcc
                tempList = []
                for i in range(self.rounds):
                    tempList += self.raceMap.checkpoints
                tempList.append(self.raceMap.checkpoints[0])
                #self.playerCheckpointList.append(tempList)
                self.playerCheckpointList[player.id] = tempList
                playerCounter += 1

            # position bots
            #for bot in self.bots:
            #    bot.reset(self.raceMap.playerStartX, self.raceMap.playerStartY, self.raceMap.playerStartDirection)
            #    bot.player.maxSpeed = self.maxSpeed
            #    bot.player.maxAcc = self.maxAcc

            # create item boxes
            for i in range(len(self.raceMap.itemBoxes)):
                self.itemBoxes.append(self.raceMap.itemBoxes[i])
                self.itemBoxes[i].cooldown = self.itemSpawnCooldown
                self.itemBoxes[i].amountOfItems = self.amountOfItems

            self.finishLine = self.raceMap.checkpoints[0]

            # reset the old leaderboard
            self.leaderboard = []

    def startRace(self):
        self.stopwatch = 0
        self.stopwatchStart = time.time_ns()
        self.stopwatchRunning = True
        self.stopwatchCurrentTime = 0

        self.checkpointsPerRounds = len(self.raceMap.checkpoints)

        self.raceStatus = "race"

    def stop(self):
        if self.raceStatus == "race":
            if self.stopwatchRunning:
                self.stopwatchCurrentTime += time.time_ns() - self.stopwatchStart
            self.stopwatchRunning = False

            self.raceStatus = "paused"

    def resume(self):
        if self.raceStatus == "paused":
            self.stopwatchStart = time.time_ns()
            self.stopwatchRunning = True

            self.raceStatus = "race"

    def reset(self, fullReset=False):
        self.stopwatch = 0
        self.stopwatchCurrentTime = 0
        self.stopwatchStart = 0
        self.stopwatchRunning = False

        self.raceStatus = "noRace"

        if fullReset:
            self.rounds = self.defaultRounds
            self.maxSpeed = self.defaultMaxSpeed
            self.maxAcc = self.defaultMaxAcc
            self.itemsEnabled = self.defaultItemsEnabled
            self.itemSpawnCooldown = self.defaultItemSpawnCooldown
            self.amountOfBots = self.defaultAmountOfBots

        self.generateAllPlayers()
        self.playerCheckpointList = {}
        self.playerRoundsList = {}
        for player in self.allPlayers:
            self.playerRoundsList[player.id] = 0
        self.leaderboard = []
        self.finishLine = []

        self.countDown = "-"
        self.drawCounter = False

        # position players
        for player in self.allPlayers:
            player.reset(self.raceMap.playerStartX, self.raceMap.playerStartY, self.raceMap.playerStartDirection)

        # position bots
        #for bot in self.bots:
        #    bot.reset(self.raceMap.playerStartX, self.raceMap.playerStartY, self.raceMap.playerStartDirection)

        # deleting all summoned items
        i = len(self.summonedItems) - 1
        while i >= 0:
            del self.summonedItems[i]
            i -= 1

        # deleting and resetting all item boxes
        i = len(self.itemBoxes) - 1
        while i >= 0:
            self.itemBoxes[i].reset()
            del self.itemBoxes[i]
            i -= 1

    def update(self):
        if self.stopwatchRunning:
            self.stopwatch = time.time_ns() + self.stopwatchCurrentTime - self.stopwatchStart

        if self.drawCounter:
            self.startingSequenz()

        match self.raceStatus:
            case "noRace":
                pass
            case "startRace": # starting sequenz
                self.startingSequenz()
            case "race":
                self.updateBots()
                self.checkPlayerPassCheckpoint()
                self.checkPlayerIsDone()
                self.checkPlayerItemHit()
                self.checkSummonedItems()
                if self.itemsEnabled:
                    self.updateItemBoxes()
                    self.checkPlayerItemBoxCollected()
                self.updatePlayerRoundList()
                self.updateLeaderboard()
                if self.checkRaceOver():
                    self.raceStatus = "raceOver"
                    print(self.raceStatus)
                    print(self.leaderboard)
                    if self.stopwatchRunning:
                        self.stopwatchCurrentTime += time.time_ns() - self.stopwatchStart
                    self.stopwatchRunning = False
            case "raceOver":
                pass
            case "paused":
                pass

    def generateAllPlayers(self):
        if len(self.allPlayers) == len(self.players) + self.amountOfBots:
            return
        # deleting all bots
        while len(self.bots) > 0:
            self.bots.pop(0)

        for i in range(self.amountOfBots):
            self.bots.append(Bot.Bot(Player.Player(100, 100, 0, 100 + i, self.summonedItems)))

        availableCarSkins = [0, 1, 2, 3, 4, 5, 6, 7]
        self.allPlayers = []
        for player in self.players:
            print("tset")
            print(len(self.players))
            deleted = False
            for i in range(len(availableCarSkins)):
                print(i)
                if not deleted:
                    if availableCarSkins[i] == player.selectedCarId:
                        availableCarSkins.pop(i)
                        deleted = True
            self.allPlayers.append(player)
        for bot in self.bots:
            temp = random.randint(0,len(availableCarSkins)-1)
            bot.player.selectedCarId = availableCarSkins[temp]
            availableCarSkins.pop(temp)
            self.allPlayers.append(bot.player)

    def updateBots(self):
        for bot in self.bots:
            bot.update()

    def checkPlayerPassCheckpoint(self):
        for player in self.allPlayers:
            if len(self.playerCheckpointList[player.id]) != 0:
                length = float('inf')
                for ray in player.frontRays:
                    newLength = ray.calcOneLine(self.playerCheckpointList[player.id][0])
                    if newLength > 0 and newLength < length:
                        length = newLength

                if length <= 3:
                    self.playerCheckpointList[player.id].pop(0)
                    #self.givePlayerItem(player)
                    print(len(self.playerCheckpointList[player.id]))

    def updatePlayerRoundList(self):
        for player in self.allPlayers:
            currentRound = 0
            for j in range(self.rounds + 1):
                if (self.rounds * self.checkpointsPerRounds) - (self.checkpointsPerRounds * j) >= len(self.playerCheckpointList[player.id]):
                    currentRound = j
            self.playerRoundsList[player.id] = currentRound

    def checkPlayerIsDone(self):
        for player in self.allPlayers:
            if len(self.playerCheckpointList[player.id]) == 0:
                player.isDone = True

    def checkRaceOver(self):
        for player in self.allPlayers:
            if not player.isDone:
                return False
        return True

    def updateLeaderboard(self):
        for player in self.allPlayers:
            if player.isDone:
                exist = False
                for j in self.leaderboard:
                    if j[0] == player.id:
                        exist = True
                if not exist:
                    temp = []
                    temp.append(player.id)
                    temp.append(self.stopwatch)
                    self.leaderboard.append(temp)

    def startingSequenz(self):
        #print((time.time_ns() - self.startingSequenzTimer))
        if (time.time_ns() - self.startingSequenzTimer) < 1000000000:
            self.countDown = "3"
        elif (time.time_ns() - self.startingSequenzTimer) < 2000000000:
            self.countDown = "2"
        elif (time.time_ns() - self.startingSequenzTimer) < 3000000000:
            self.countDown = "1"
        elif (time.time_ns() - self.startingSequenzTimer) < 4000000000:
            self.countDown = "GO"
            self.startRace()
        elif (time.time_ns() - self.startingSequenzTimer) < 5000000000:
            self.countDown = "-"
            self.drawCounter = False

    #def givePlayerItem(self, player):
    #    if self.itemsEnabled and player.currentItem == -1:
    #        player.currentItem = random.randint(0, self.amountOfItems-1)
    #        #player.currentItem = 5 # for item testing

    def checkSummonedItems(self):
        i = len(self.summonedItems) - 1
        while i >= 0:
            if not self.summonedItems[i].living:
                del self.summonedItems[i]
            i -= 1

    def updateItemBoxes(self):
        for box in self.itemBoxes:
            box.update()

    def checkPlayerItemBoxCollected(self):
        for box in self.itemBoxes:
            box.checkCollected(self.allPlayers)

    def checkPlayerItemHit(self):
        for item in self.summonedItems:
            for player in self.allPlayers:
                if player.stunTime == 0:
                    match (item.itemName):
                        case "Rocket" | "MultiRocket":
                            if player.id not in item.hitPlayers:
                                x = player.x - item.x
                                y = player.y - item.y
                                distance1 = np.sqrt(np.power(x, 2) + np.power(y, 2))
                                if item.explode:
                                    distance2 = 0

                                    angle = 90
                                    if x != 0:
                                        angle = np.rad2deg(np.arctan(y/x))
                                    if angle < 0:
                                        angle *= -1
                                    while angle > 90:
                                        angle -= 90

                                    if angle == 45:
                                        distance2 = 14.142135624 # np.sqrt(np.power(x, 10) + np.power(y, 10))
                                    elif angle < 45:
                                        distance2 = 10 / np.sin(np.deg2rad(90 - angle))
                                    elif angle > 45:
                                        distance2 = 10 / np.sin(np.deg2rad(angle))

                                    if distance1 - distance2 <= item.explodeRadius:
                                        item.hitPlayers.append(player.id)
                                        player.itemHit(item.itemName)
                                else:
                                    if distance1 <= 10 and player.id != item.summonedPlayer.id:
                                        item.explode = True
                        case "OilPuddle":
                            if player.id not in item.hitPlayers and not (player.id == item.summonedPlayer.id and item.liveTime >= item.maxLiveTime - 120):
                                x = player.x - item.x
                                y = player.y - item.y
                                distance = np.sqrt(np.power(x, 2) + np.power(y, 2))

                                if distance <= item.size:
                                    item.hitPlayers.append(player.id)
                                    player.itemHit(item.itemName)

                        case "GodMode":
                            if player.id != item.summonedPlayer.id:
                                x = player.x - item.summonedPlayer.x
                                y = player.y - item.summonedPlayer.y
                                distance = np.sqrt(np.power(x, 2) + np.power(y, 2))
                                if distance <= item.radius:
                                    player.itemHit(item.itemName)
