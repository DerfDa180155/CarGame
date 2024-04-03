import os


class Settings:
    def __init__(self, path):
        self.path = path

        self.driveForwardKey = "w"
        self.driveBackwardKey = "s"
        self.steerLeftKey = "a"
        self.steerRightKey = "d"
        self.pauseKey = "escape"

        self.loadSettings()

    def loadSettings(self):
        pass


    def saveSettings(self):
        pass
