import numpy as np
import time
import array
import RaceMap

class RaceObject:
    def __init__(self, players: array, raceMap: RaceMap):
        self.stopwatch = 0
        self.stopwatchCurrentTime = 0
        self.stopwatchStart = 0
        self.stopwatchRunning = False

        self.raceMap = raceMap
        self.raceStatus = "noRace"
        self.mode = "singleplayer"
        self.maxRounds = 0
        self.playerMaxItemCount = 0
        self.checkpointsPerRounds = len(self.raceMap.checkpoints)

        self.players = players
        self.playerCheckpointList = []
        self.playerRoundsList = [0, 0]
        self.leaderboard = []



    def start(self, raceMap: RaceMap):
        if self.maxRounds > 0: # only start wenn the race settings are set
            self.stopwatchStart = time.time_ns()
            self.stopwatchRunning = True
            self.stopwatchCurrentTime = 0

            self.checkpointsPerRounds = len(self.raceMap.checkpoints)

            self.raceStatus = "race"
            self.raceMap = raceMap

            # position players and create checkpoints list
            self.playerCheckpointList = []
            for player in self.players:
                player.reset(self.raceMap.playerStartX, self.raceMap.playerStartY, self.raceMap.playerStartDirection)
                tempList = []
                for i in range(self.maxRounds):
                    tempList += self.raceMap.checkpoints
                self.playerCheckpointList.append(tempList)


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
        self.maxRounds = 0
        self.playerMaxItemCount = 0
        self.playerCheckpointList = []
        self.playerRoundsList = [0, 0]

    def update(self):
        if self.stopwatchRunning:
            self.stopwatch = time.time_ns() + self.stopwatchCurrentTime - self.stopwatchStart

        match self.raceStatus:
            case "noRace":
                pass
            case "race":
                self.checkPlayerPassCheckpoint()
                self.checkPlayerIsDone()
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
        i = 0
        for player in self.players:
            if len(self.playerCheckpointList[i]) != 0:
                length = float('inf')
                for ray in player.frontRays:
                    newLength = ray.calcOneLine(self.playerCheckpointList[i][0])
                    if newLength > 0 and newLength < length:
                        length = newLength

                if length <= 3:
                    self.playerCheckpointList[i].pop(0)
                    print(len(self.playerCheckpointList[i]))

            i += 1

    def updatePlayerRoundList(self):
        i = 0
        for player in self.players:
            currentRound = 0
            for j in range(self.maxRounds+1):
                if (self.maxRounds * self.checkpointsPerRounds) - (self.checkpointsPerRounds * j) >= len(self.playerCheckpointList[i]):
                    currentRound = j
            self.playerRoundsList[i] = currentRound

            i += 1

    def checkPlayerIsDone(self):
        i = 0
        for player in self.players:
            if len(self.playerCheckpointList[i]) == 0:
                player.isDone = True
            i += 1

    def checkRaceOver(self):
        if self.mode == "singleplayer":
            return self.players[0].isDone
        for player in self.players:
            if not player.isDone:
                return False
        return True

    def updateLeaderboard(self):
        i = 1
        for player in self.players:
            if player.isDone:
                exist = False
                for j in self.leaderboard:
                    if j[0] == i:
                        exist = True
                if not exist:
                    temp = []
                    temp.append(i)
                    temp.append(self.stopwatch)
                    self.leaderboard.append(temp)

            i += 1
