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
        else:
        # COVERED: this will show a flag if flagged, otherwise the unknown tile
            if self.flagged:
                if ((self.x + self.y) // CELLSIZE) % 2 == 0:
                    grid_surface.blit(flag_cell_1, (self.x, self.y))
                else:
                    grid_surface.blit(flag_cell_2, (self.x, self.y))
            else:
                if ((self.x + self.y) // CELLSIZE) % 2 == 0:
                    grid_surface.blit(unknown_cell_1, (self.x, self.y))
                else:
                    grid_surface.blit(unknown_cell_2, (self.x, self.y))

    def __repr__(self):
        return self.type

class Grid:
    def __init__(self, bomb_amount = BOMB_AMT):
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

        self.mine_count = bomb_amount #total mines/bombs = total flags
        self.flags_placed = 0 #this tracks how many flags are placed
        self.generate_bombs()

    def flags_remaining(self):
        return self.mine_count - self.flags_placed
    
    def toggle_flag(self, r, c):
        cell = self.grid_list[r][c]
        if cell.revealed:
            return
        if cell.flagged:
            cell.flagged = False
            self.flags_placed = max(0, self.flags_placed - 1)
        else:
            if self.flags_remaining() > 0:
                cell.flagged = True
                self.flags_placed += 1
    
    def display_board(self):
        for row in self.grid_list:
           print(row)

    def draw(self, screen):
        for row in self.grid_list:
            for cell in row:
                cell.draw(self.grid_surface)
        screen.blit(self.grid_surface, (0, 0))

    def generate_bombs(self):
        for i in range(self.mine_count):
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