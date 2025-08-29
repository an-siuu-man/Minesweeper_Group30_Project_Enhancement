import pygame
from settings import *
import random
# Types: ~ = Unknown, B = Bomb, E = Empty, test
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
            if self.type == "~": #Draw Number
                darkgreen_layer = pygame.Surface((CELLSIZE, CELLSIZE))
                darkgreen_layer.fill(DARKGREEN) #TODO: Draw cell with number instead
                grid_surface.blit(darkgreen_layer, (self.x, self.y))
            else: #Draw Bomb
                grid_surface.blit(self.image, (self.x, self.y))
        else: #Draw Unknown
            if ((self.x + self.y) / CELLSIZE) % 2 == 0:
                grid_surface.blit(unknown_cell_1, (self.x, self.y))
            else:
                grid_surface.blit(unknown_cell_2, (self.x, self.y))

    def __repr__(self):
        return self.type

class Grid:
    def __init__(self, bomb_amount = 10):
        self.bomb_amount = bomb_amount
        self.grid_surface = pygame.Surface((WIDTH, HEIGHT))
        self.grid_list = self.grid_list = [
        [
            Cell(
                col,
                row,
                empty_cell_1 if (row + col) % 2 == 0 else empty_cell_2,
                "~"
            )
            for col in range(COLUMNS)
        ]
        for row in range(ROWS)
    ]

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
        for i in range(self.bomb_amount):
            while True:
                bomb_x_coord = random.randint(0, ROWS-1)
                bomb_y_coord = random.randint(0, COLUMNS - 1)
                if self.grid_list[bomb_x_coord][bomb_y_coord].type == "~":
                    self.grid_list[bomb_x_coord][bomb_y_coord].type = "B"
                    if (bomb_x_coord + bomb_y_coord) % 2 == 0:
                        self.grid_list[bomb_x_coord][bomb_y_coord].image = bomb_cell_1
                    else:
                        self.grid_list[bomb_x_coord][bomb_y_coord].image = bomb_cell_2
                    break