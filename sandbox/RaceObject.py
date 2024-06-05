import random

import numpy as np
import time
import array
import RaceMap

class RaceObject:
    def __init__(self, players: array, raceMap: RaceMap, amountOfItems: int, summonedItems: array):
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
        self.defaultItemSpawnCooldown = 0

        self.rounds = self.defaultRounds
        self.maxSpeed = self.defaultMaxSpeed
        self.maxAcc = self.defaultMaxAcc
        self.itemsEnabled = self.defaultItemsEnabled
        self.itemSpawnCooldown = self.defaultItemSpawnCooldown
        self.amountOfItems = amountOfItems
        self.summonedItems = summonedItems

        self.checkpointsPerRounds = len(self.raceMap.checkpoints)

        self.players = players
        self.playerCheckpointList = []
        self.playerRoundsList = [0, 0]
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

            # position players and create checkpoints list
            self.playerCheckpointList = []
            for player in self.players:
                player.reset(self.raceMap.playerStartX, self.raceMap.playerStartY, self.raceMap.playerStartDirection)
                player.maxSpeed = self.maxSpeed
                player.maxAcc = self.maxAcc
                tempList = []
                for i in range(self.rounds):
                    tempList += self.raceMap.checkpoints
                tempList.append(self.raceMap.checkpoints[0])
                self.playerCheckpointList.append(tempList)

            self.finishLine = self.playerCheckpointList[0][len(self.playerCheckpointList[0])-1]

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

    def reset(self):
        self.stopwatch = 0
        self.stopwatchCurrentTime = 0
        self.stopwatchStart = 0
        self.stopwatchRunning = False

        self.raceStatus = "noRace"

        self.rounds = self.defaultRounds
        self.maxSpeed = self.defaultMaxSpeed
        self.maxAcc = self.defaultMaxAcc
        self.itemsEnabled = self.defaultItemsEnabled
        self.itemSpawnCooldown = self.defaultItemSpawnCooldown

        self.playerCheckpointList = []
        self.playerRoundsList = [0, 0]
        self.leaderboard = []
        self.finishLine = []

        self.countDown = "-"
        self.drawCounter = False

        # position players
        for player in self.players:
            player.reset(self.raceMap.playerStartX, self.raceMap.playerStartY, self.raceMap.playerStartDirection)

        # deleting all summoned items
        i = len(self.summonedItems) - 1
        while i >= 0:
            del self.summonedItems[i]
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
                self.checkPlayerPassCheckpoint()
                self.checkPlayerIsDone()
                self.checkSummonedItems()
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

    def checkPlayerPassCheckpoint(self):
        for player in self.players:
            if len(self.playerCheckpointList[player.id]) != 0:
                length = float('inf')
                for ray in player.frontRays:
                    newLength = ray.calcOneLine(self.playerCheckpointList[player.id][0])
                    if newLength > 0 and newLength < length:
                        length = newLength

                if length <= 3:
                    self.playerCheckpointList[player.id].pop(0)
                    self.givePlayerItem(player)
                    print(len(self.playerCheckpointList[player.id]))

    def updatePlayerRoundList(self):
        for player in self.players:
            currentRound = 0
            for j in range(self.rounds + 1):
                if (self.rounds * self.checkpointsPerRounds) - (self.checkpointsPerRounds * j) >= len(self.playerCheckpointList[player.id]):
                    currentRound = j
            self.playerRoundsList[player.id] = currentRound

    def checkPlayerIsDone(self):
        for player in self.players:
            if len(self.playerCheckpointList[player.id]) == 0:
                player.isDone = True

    def checkRaceOver(self):
        if self.mode == "singleplayer":
            return self.players[0].isDone
        for player in self.players:
            if not player.isDone:
                return False
        return True

    def updateLeaderboard(self):
        for player in self.players:
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

    def givePlayerItem(self, player):
        if self.itemsEnabled and player.currentItem == -1:
            player.currentItem = random.randint(0, self.amountOfItems-1)
            player.currentItem = 1 # for item testing

    def checkSummonedItems(self):
        i = len(self.summonedItems) - 1
        while i >= 0:
            if not self.summonedItems[i].living:
                del self.summonedItems[i]
            i -= 1
