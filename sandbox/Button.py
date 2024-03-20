import time

import pygame
import random
import os
import numpy
import array


class Button:
    def __init__(self, surface, x: int, y: int, size: int, img: pygame.image, action: str):
        self.surface = surface
        self.x = x
        self.y = y
        self.size = size
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.topleft = (x, y)
        self.scaledImg = img
        self.isClicked = False
        self.hadAction = False
        self.action = action
        self.enable = True

    def draw(self, currentWidth: int, currentHeight: int):
        if self.enable:
            newX = (self.x * currentWidth) / 1600
            newY = (self.y * currentHeight) / 900
            newSizeX = (self.size * currentWidth) / 1600
            newSizeY = (self.size * currentHeight) / 900
            self.scaledImg = pygame.transform.scale(self.img, (newSizeX, newSizeY))
            self.rect = self.scaledImg.get_rect()
            self.rect.topleft = (newX, newY)
            self.surface.blit(self.scaledImg, (newX, newY))

    def clicked(self, mx: int, my: int, mouseClick: array):
        if self.enable:
            if self.rect.collidepoint((mx, my)) and mouseClick[0]:
                self.isClicked = True
                time.sleep(0.3) # delay for multiple button presses
            else:
                self.hadAction = False
                self.isClicked = False

            return self.isClicked
        return False

    def hover(self, mx: int, my: int):
        return self.rect.collidepoint((mx, my)) and self.enable

