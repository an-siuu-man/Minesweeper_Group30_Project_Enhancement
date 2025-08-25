import pygame
from settings import *
import random
# Types: ~ = Unkown, B = Bomb, E = Empty
class Cell:
    def __init__(self, x, y, image, type, revealed=False, flagged=False):
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.image = image
        self.type = type
        self.revealed = revealed
        self.flagged = flagged

    def __type__(self):
        return self.type

class Grid:
    def generate_bombs(self, total_bombs):
        for i in range(total_bombs):
            while True:
                bomb_x_coord = random.randint(0, ROWS-1)
                bomb_y_coord = random.randint(0, COLUMNS - 1)
                if self.grid_list[bomb_x_coord][bomb_y_coord].type == "~":
                    self.grid_list[bomb_x_coord][bomb_y_coord].type = "B"
                    self.grid_list[bomb_x_coord][bomb_y_coord].image = bomb_tile
                    break