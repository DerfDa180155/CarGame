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

        self.loadSettings()

    def loadSettings(self):
        pass

    def saveSettings(self):
        root = ET.Element("settings")
        ET.SubElement(root, "driveForwardKey").text = str(pygame.key.key_code(self.driveForwardKey))
        ET.SubElement(root, "driveBackwardKey").text = str(pygame.key.key_code(self.driveBackwardKey))
        ET.SubElement(root, "steerLeftKey").text = str(pygame.key.key_code(self.steerLeftKey))
        ET.SubElement(root, "steerRightKey").text = str(pygame.key.key_code(self.steerRightKey))
        ET.SubElement(root, "pauseKey").text = str(pygame.key.key_code(self.pauseKey))

        print(self.path + self.filename + ".xml")
        ET.ElementTree(root).write(self.path + self.filename + ".xml")
