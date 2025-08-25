import pygame
from settings import *

class Ceil:
    def __init__(self, x, y, image, type, revealed=False, flagged=False):
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.image = image
        self.type = type
        self.revealed = revealed
        self.flagged = flagged

    def __type__(self):
        return self.type