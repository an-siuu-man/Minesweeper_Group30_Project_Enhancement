import pygame
from settings import *
import random
# Types: ~ = Unkown, B = Bomb, E = Empty, test
class Cell:
    def __init__(self, x, y, image, type, revealed=False, flagged=False):
        self.x = x * CELLSIZE
        self.y = y * CELLSIZE
        self.image = image
        self.type = type
        self.revealed = revealed
        self.flagged = flagged

    def __type__(self):
        return self.type

class Grid:
    def __init__(self):
       self.grid_surface = pygame.Surface((WIDTH, HEIGHT))
       self.grid_list = [[Cell(col, row, empty_cell, ".") for row in range(ROWS)] for col in range(COLUMNS)]
       self.generate_bombs()
  
    def display_board(self):
       for row in self.grid_list:
           print(row)
    
    def generate_bombs(self):
        for i in range(BOMB_AMT):
            while True:
                bomb_x_coord = random.randint(0, ROWS-1)
                bomb_y_coord = random.randint(0, COLUMNS - 1)
                if self.grid_list[bomb_x_coord][bomb_y_coord].type == "~":
                    self.grid_list[bomb_x_coord][bomb_y_coord].type = "B"
                    self.grid_list[bomb_x_coord][bomb_y_coord].image = bomb_cell
                    break
