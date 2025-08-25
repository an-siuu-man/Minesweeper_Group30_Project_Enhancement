import pygame
from settings import *
import random
# Types: ~ = Unkown, B = Bomb, E = Empty, test
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
    def __init__(self):
       self.grid_surface = pygame.Surface((WIDTH, HEIGHT))
       self.grid_list = [[Tile(col, row, tile_empty, ".") for row in range(ROWS)] for col in range(COLS)]
  
   def display_board(self):
       for row in self.grid_list:
           print(row)
    
    def generate_bombs(self, total_bombs):
        for i in range(total_bombs):
            while True:
                bomb_x_coord = random.randint(0, ROWS-1)
                bomb_y_coord = random.randint(0, COLUMNS - 1)
                if self.grid_list[bomb_x_coord][bomb_y_coord].type == "~":
                    self.grid_list[bomb_x_coord][bomb_y_coord].type = "B"
                    self.grid_list[bomb_x_coord][bomb_y_coord].image = bomb_tile
                    break
