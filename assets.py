import pygame
from settings import *
import random
# Types: B = Bomb, E = Empty, N = Number
class Cell:
    def __init__(self, x, y, image, type = "E", revealed=False, flagged=False):
        self.x = x * CELLSIZE
        self.y = y * CELLSIZE
        self.image = image
        self.type = type
        self.revealed = revealed
        self.flagged = flagged

    def draw(self, grid_surface):
        if self.revealed:
            if not self.flagged: #Draw numbered cells
                grid_surface.blit(self.image, (self.x, self.y))
        else: 
            if self.flagged: #Draw Flag
                pass
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
                "E"
            )
            for col in range(COLUMNS)
        ]
        for row in range(ROWS)
    ]

        self.generate_bombs()
        self.generate_numbers()

    def display_board(self):
        for row in self.grid_list:
           print(row)

    def generate_numbers(self):
        for x in range(ROWS):
            for y in range(COLUMNS):
                if self.grid_list[x][y].type != "B":
                    total_bombs = self.check_adj_cells(x, y)
                    if total_bombs > 0:
                        self.grid_list[x][y].image = cell_num_1[total_bombs - 1] if (x + y) % 2 == 0 else cell_num_2[total_bombs - 1]
                        self.grid_list[x][y].type = "N"

    @staticmethod
    def is_inside_grid(x, y):
        '''
        Static function that checks if a cell at (x, y) is within the game grid.
        Returns true if cell is inside board, false otherwise.
        '''
        return 0 <= x < ROWS and 0 <= y < COLUMNS

    def check_adj_cells(self, x, y):
        '''
        Checks the adjacent 8 cells around a given cell and calculates the cell number.
        '''
        total_bombs = 0
        #Checks adjacent cells starting from the top left corner (-1, -1).
        for x_offset in range(-1, 2):
            for y_offset in range(-1, 2):
                adj_x = x + x_offset
                adj_y = y + y_offset

                if self.is_inside_grid(adj_x, adj_y) and self.grid_list[adj_x][adj_y].type == "B":
                    total_bombs += 1

        return total_bombs

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
                if self.grid_list[bomb_x_coord][bomb_y_coord].type == "E":
                    self.grid_list[bomb_x_coord][bomb_y_coord].type = "B"
                    self.grid_list[bomb_x_coord][bomb_y_coord].image = bomb_cell_1 if (bomb_x_coord + bomb_y_coord) % 2 == 0 else bomb_cell_2
                    break