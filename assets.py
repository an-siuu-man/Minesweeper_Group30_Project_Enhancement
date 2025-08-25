import pygame
from settings import *
import random
# Types: ~ = Unkown, B = Bomb, E = Empty, test
class Cell:
    def __init__(self, x, y, image, type = "~", revealed=False, flagged=False):
        self.x = x * CELLSIZE
        self.y = y * CELLSIZE
        self.image = image
        self.type = type
        self.revealed = revealed
        self.flagged = flagged

    def draw(self, grid_surface):
        if self.revealed == True:
            if self.type == "~":
                darkgreen_layer = pygame.Surface((CELLSIZE, CELLSIZE))
                darkgreen_layer.fill(DARKGREEN)
                grid_surface.blit(darkgreen_layer, (self.x, self.y))
            else:
                grid_surface.blit(self.image, (self.x, self.y))
        else:
            grid_surface.blit(unknown_cell, (self.x, self.y))

    def __repr__(self):
        return self.type

class Grid:
    def __init__(self):
       self.grid_surface = pygame.Surface((WIDTH, HEIGHT))
       self.grid_list = [[Cell(col, row, unknown_cell, "~") for col in range(COLUMNS)] for row in range(ROWS)]
       self.generate_bombs()

    def display_board(self):
       for row in self.grid_list:
           print(row)

    def draw(self, screen):
        for row in self.grid_list:
            for cell in row:
                cell.draw(self.grid_surface)
        screen.blit(self.grid_surface, (0, 0))

    def generate_bombs(self):
        for i in range(BOMB_AMT):
            while True:
                bomb_x_coord = random.randint(0, ROWS-1)
                bomb_y_coord = random.randint(0, COLUMNS - 1)
                if self.grid_list[bomb_x_coord][bomb_y_coord].type == "~":
                    self.grid_list[bomb_x_coord][bomb_y_coord].type = "B"
                    self.grid_list[bomb_x_coord][bomb_y_coord].image = bomb_cell
                    break