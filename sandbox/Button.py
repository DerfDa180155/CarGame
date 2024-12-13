import time
import pygame
import random
import os
import numpy
import array


class Button:
    def __init__(self, surface, x: int, y: int, size: int, img: pygame.image, action: str, displayText: str = "", displayTextColor = (255, 255, 255), displayTextSize: int = 20, useTopLeft: bool = True):
        self.surface = surface
        self.x = x
        self.y = y
        self.size = size
        self.displayText = displayText
        self.displayTextColor = displayTextColor
        self.displayTextSize = displayTextSize
        self.img = img
        self.rect = self.img.get_rect()
        self.useTopLeft = useTopLeft
        if self.useTopLeft:
            self.rect.topleft = (x, y)
        else:
            self.rect.center = (x, y)
        self.scaledImg = img
        self.isClicked = False
        self.hadAction = False
        self.action = action
        self.enable = True
        self.getsHovered = False

    def draw(self, currentWidth: int, currentHeight: int, highlight: bool = False):
        if self.enable:
            newTextSize = int((self.displayTextSize * currentWidth) / 2000)  # scale text size
            font = pygame.font.Font(pygame.font.get_default_font(), newTextSize)


            newX = (self.x * currentWidth) / 1600
            newY = (self.y * currentHeight) / 900
            newSizeX = ((self.img.get_width() / self.img.get_height())  * self.size * currentWidth) / 1600
            newSizeY = (self.size * currentHeight) / 900
            self.scaledImg = pygame.transform.scale(self.img, (newSizeX, newSizeY))
            self.rect = self.scaledImg.get_rect()
            if self.useTopLeft:
                self.rect.topleft = (newX, newY)
                self.surface.blit(self.scaledImg, (newX, newY))
            else:
                self.rect.center = (newX, newY)
                self.surface.blit(self.scaledImg, (newX-(newSizeX/2), newY-(newSizeY/2)))

            text = font.render(self.displayText, True, self.displayTextColor)
            newRect = text.get_rect()
            newRect.center = self.rect.center
            self.surface.blit(text, newRect)

            if self.getsHovered:
                darkenFaktor = 100
                newImg = self.scaledImg.copy().convert_alpha()
                #newImg.fill((darkenFaktor, darkenFaktor, darkenFaktor))

                darkOverlay = pygame.Surface(newImg.get_size(), flags=pygame.SRCALPHA)
                darkOverlay.fill((0, 0, 0, darkenFaktor))
                newImg.blit(darkOverlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

                if self.useTopLeft:
                    self.surface.blit(newImg, (newX, newY))
                else:
                    self.surface.blit(newImg, (newX-(newSizeX/2), newY-(newSizeY/2)), special_flags=pygame.BLEND_RGBA_SUB)

            if highlight:
                darkenFaktor = 50
                newImg = self.scaledImg.copy()
                newImg.fill((darkenFaktor, darkenFaktor, darkenFaktor))
                if self.useTopLeft:
                    self.surface.blit(newImg, (newX, newY), special_flags=pygame.BLEND_RGBA_ADD)
                else:
                    self.surface.blit(newImg, (newX - (newSizeX / 2), newY - (newSizeY / 2)),
                                      special_flags=pygame.BLEND_RGBA_ADD)

    def clicked(self, mx: int, my: int, mouseClick: array):
        if self.enable:
            if self.hover(mx, my):
                if self.rect.collidepoint((mx, my)) and mouseClick[0]:
                    self.isClicked = True
                    #time.sleep(0.3) # delay for multiple button presses
                else:
                    self.hadAction = False
                    self.isClicked = False

                return self.isClicked
        return False

    def hover(self, mx: int, my: int):
        self.getsHovered = self.rect.collidepoint((mx, my)) and self.enable
        return self.getsHovered

