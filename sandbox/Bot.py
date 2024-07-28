import pygame
import random
import numpy as np
import array
import Player


class Bot:
    def __init__(self, player: Player):
        self.player = player

    def reset(self, x: int, y: int, direction: int):
        self.player.reset(x, y, direction)

    def update(self):
        self.player.move(True) # for testing

