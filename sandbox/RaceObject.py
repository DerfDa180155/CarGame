import numpy as np
import time

class RaceObject:
    def __init__(self):
        self.stopwatch = 0
        self.stopwatchStart = 0
        self.stopwatchRunning = False

    def start(self):
        self.stopwatchStart = time.time_ns()
        self.stopwatchRunning = True

    def stop(self):
        self.stopwatchRunning = False

    def reset(self):
        self.stopwatch = 0
        self.stopwatchStart = 0
        self.stopwatchRunning = False

    def update(self):
        if self.stopwatchRunning:
            self.stopwatch = time.time_ns() - self.stopwatchStart

