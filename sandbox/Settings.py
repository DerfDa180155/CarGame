import pygame
import os
import xml.etree.cElementTree as ET


class Settings:
    def __init__(self, path: str, filename: str = "settings"):
        self.path = path
        self.filename = filename

        # default keys
        self.driveForwardKey = "w"
        self.driveBackwardKey = "s"
        self.steerLeftKey = "a"
        self.steerRightKey = "d"
        self.pauseKey = "escape"

        self.playerSteering = [["w", "s", "a", "d"], ["up", "down", "left", "right"]]

        # game settings
        self.FPS = 60
        self.TPS = 120

        self.loadSettings()

    def loadSettings(self):
        currentPath = os.getcwd()
        settingsPath = os.path.join(currentPath, self.path)

        for root, dirs, files in os.walk(settingsPath):
            for file in files:
                if self.filename + ".xml" == file:
                    docRoot = ET.parse(os.path.join(root, file)).getroot()
                    self.driveForwardKey = pygame.key.name(int(docRoot[0].text))
                    self.driveBackwardKey = pygame.key.name(int(docRoot[1].text))
                    self.steerLeftKey = pygame.key.name(int(docRoot[2].text))
                    self.steerRightKey = pygame.key.name(int(docRoot[3].text))
                    self.pauseKey = pygame.key.name(int(docRoot[4].text))
                    self.FPS = int(docRoot[5].text)
                    self.TPS = int(docRoot[6].text)

    def saveSettings(self):
        root = ET.Element("settings")
        ET.SubElement(root, "driveForwardKey").text = str(pygame.key.key_code(self.driveForwardKey))
        ET.SubElement(root, "driveBackwardKey").text = str(pygame.key.key_code(self.driveBackwardKey))
        ET.SubElement(root, "steerLeftKey").text = str(pygame.key.key_code(self.steerLeftKey))
        ET.SubElement(root, "steerRightKey").text = str(pygame.key.key_code(self.steerRightKey))
        ET.SubElement(root, "pauseKey").text = str(pygame.key.key_code(self.pauseKey))
        ET.SubElement(root, "FPS").text = str(self.FPS)
        ET.SubElement(root, "TPS").text = str(self.TPS)

        print(self.path + self.filename + ".xml")
        ET.ElementTree(root).write(self.path + self.filename + ".xml")

    def copyFrom(self, newSetting):
        self.driveForwardKey = newSetting.driveForwardKey
        self.driveBackwardKey = newSetting.driveBackwardKey
        self.steerLeftKey = newSetting.steerLeftKey
        self.steerRightKey = newSetting.steerRightKey

        #self.playerSteering = newSetting.playerSteering

        self.pauseKey = newSetting.pauseKey

        self.FPS = newSetting.FPS
        self.TPS = newSetting.TPS
