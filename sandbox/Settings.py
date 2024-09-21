import pygame
import os
import xml.etree.cElementTree as ET


class Settings:
    def __init__(self, path: str, filename: str = "settings"):
        self.path = path
        self.filename = filename

        # default keys
        #self.driveForwardKey = "w"
        #self.driveBackwardKey = "s"
        #self.steerLeftKey = "a"
        #self.steerRightKey = "d"

        # player steering keys with default values
        self.playerKeys = [["w", "s", "a", "d", "space"], ["up", "down", "left", "right", "0"]]
        self.pauseKey = "escape"

        # game settings
        self.FPS = 60
        self.TPS = 120
        self.displayFPS = False
        self.displayTPS = False

        self.debugMode = False

        self.loadSettings()

    def loadSettings(self):
        currentPath = os.getcwd()
        settingsPath = os.path.join(currentPath, self.path)

        for root, dirs, files in os.walk(settingsPath):
            for file in files:
                if self.filename + ".xml" == file:
                    docRoot = ET.parse(os.path.join(root, file)).getroot()
                    self.FPS = int(docRoot[0].text)
                    self.TPS = int(docRoot[1].text)
                    self.pauseKey = pygame.key.name(int(docRoot[2].text))

                    self.displayFPS = (int(docRoot[3].text) == 1)
                    self.displayTPS = (int(docRoot[4].text) == 1)
                    self.debugMode = (int(docRoot[5].text) == 1)

                    # load the keys of the players
                    self.playerKeys = []
                    for player in docRoot[6]:
                        temp = []
                        for i in player:
                            temp.append(pygame.key.name(int(i.text)))
                        self.playerKeys.append(temp)

    def saveSettings(self):
        root = ET.Element("settings")
        ET.SubElement(root, "FPS").text = str(self.FPS)
        ET.SubElement(root, "TPS").text = str(self.TPS)
        ET.SubElement(root, "pauseKey").text = str(pygame.key.key_code(self.pauseKey))
        ET.SubElement(root, "displayFPS").text = str(int(self.displayFPS))
        ET.SubElement(root, "displayTPS").text = str(int(self.displayTPS))
        ET.SubElement(root, "debugMode").text = str(int(self.debugMode))

        # save the keys of the players
        playerKeys = ET.SubElement(root, "PlayerKeys", type="array")
        for player in self.playerKeys:
            playerTag = ET.SubElement(playerKeys, "player")
            ET.SubElement(playerTag, "driveForwardKey").text = str(pygame.key.key_code(player[0]))
            ET.SubElement(playerTag, "driveBackwardKey").text = str(pygame.key.key_code(player[1]))
            ET.SubElement(playerTag, "steerLeftKey").text = str(pygame.key.key_code(player[2]))
            ET.SubElement(playerTag, "steerRightKey").text = str(pygame.key.key_code(player[3]))
            ET.SubElement(playerTag, "useItem").text = str(pygame.key.key_code(player[4]))

        print(self.path + self.filename + ".xml")
        ET.ElementTree(root).write(self.path + self.filename + ".xml")

    def copyFrom(self, newSetting):
        self.playerKeys = newSetting.playerKeys

        self.pauseKey = newSetting.pauseKey

        self.FPS = newSetting.FPS
        self.TPS = newSetting.TPS
        self.displayFPS = newSetting.displayFPS
        self.displayTPS = newSetting.displayTPS

        self.debugMode = newSetting.debugMode
