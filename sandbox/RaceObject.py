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

        self.raceStatus = "noRace"
        self.mode = "singleplayer"
        self.maxRounds = 0
        self.playerMaxItemCount = 0

        self.players = players

        self.raceMap = raceMap

    def start(self, raceMap: RaceMap):
        if self.maxRounds > 0: # only start wenn the race settings are set
            self.stopwatchStart = time.time_ns()
            self.stopwatchRunning = True
            self.stopwatchCurrentTime = 0

            self.raceStatus = "race"
            self.raceMap = raceMap

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

    def update(self):
        if self.stopwatchRunning:
            self.stopwatch = time.time_ns() + self.stopwatchCurrentTime - self.stopwatchStart

        match self.raceStatus:
            case "noRace":
                pass
            case "race":
                pass
            case "paused":
                pass
