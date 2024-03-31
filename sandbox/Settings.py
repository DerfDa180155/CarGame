import os


class Settings:
    def __init__(self, path):
        self.path = path

        self.driveForwardKey = "1"
        self.driveBackwardKey = "2"
        self.steerLeftKey = "3"
        self.steerRightKey = "4"
        self.pauseKey = "5"

        self.loadSettings()

    def loadSettings(self):
        pass


    def saveSettings(self):
        pass
