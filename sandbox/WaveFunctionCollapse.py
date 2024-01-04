import pygame
import random
import os
import time
import numpy

class WaveFunctionCollapse:
    def __init__(self, images):
        self.images = images

    def generate(self, x, y):
        map = []
        a = 0
        while a < x:
            temp = []
            b = 0
            while b < y:
                temp.append(0)
                b += 1
            map.append(temp)
            a += 1

        a = random.randint(0, x-1)
        b = random.randint(0, y-1)

        map[a][b] = random.randint(1, 4)


        return map
