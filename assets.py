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
    def __init__(self, bomb_amount = 10):
        self.bomb_amount = bomb_amount
        self.grid_surface = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))
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
        self.bombs_generated = False
        self.numbers_generated = False
        self.mine_count = bomb_amount #total mines/bombs = total flags
        self.flags_placed = 0 #this tracks how many flags are placed
        self.dug = [] #store values that are dug out 

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
        print("")

    def generate_numbers(self):
        for x in range(ROWS):
            for y in range(COLUMNS):
                if self.grid_list[x][y].type != "B":
                    total_bombs = self.check_adj_cells(x, y)
                    if total_bombs > 0:
                        self.grid_list[x][y].image = cell_num_1[total_bombs - 1] if (x + y) % 2 == 0 else cell_num_2[total_bombs - 1]
                        self.grid_list[x][y].type = "N"
        self.numbers_generated = True

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
        # Need a HUD_HEIGHT for the header/menu banner part.
        screen.blit(self.grid_surface, (PADDING, PADDING))

    def generate_bombs(self, safe_row, safe_col):
        planted_bombs = 0
        while planted_bombs < self.bomb_amount:
            bomb_x_coord = random.randint(0, ROWS-1)
            bomb_y_coord = random.randint(0, COLUMNS - 1)

            if bomb_x_coord == safe_row and bomb_y_coord == safe_col:
                continue

            if self.grid_list[bomb_x_coord][bomb_y_coord].type == "E":
                self.grid_list[bomb_x_coord][bomb_y_coord].type = "B"
                self.grid_list[bomb_x_coord][bomb_y_coord].image = bomb_cell_1 if (bomb_x_coord + bomb_y_coord) % 2 == 0 else bomb_cell_2
                planted_bombs += 1
        
        self.bombs_generated = True
    def reveal_bombs(self):
        for row in self.grid_list:
            for cell in row:
                if cell.type == "B":
                    cell.revealed = True
    def check_win(self):
        count_revealed = 0
        for row in self.grid_list:
            for cell in row:
                if cell.revealed == True:
                    if cell.type != "B":
                        count_revealed+=1
        if count_revealed == (100 - self.bomb_amount):
            return True
        else:
            return False
        
    def dig(self, x, y): 
        self.dug.append((x, y))
        if self.grid_list[x][y].type == "B":
            self.grid_list[x][y].revealed = True
            if (x+y) % 2 == 0:  
                self.grid_list[x][y].image = exploded_cell_1 
            else: 
                self.grid_list[x][y].image = exploded_cell_2
            return False
        elif self.grid_list[x][y].type == "N": 
            self.grid_list[x][y].revealed = True
            return True 
        
        self.grid_list[x][y].revealed = True

        for row in range(max(0, x-1), min(ROWS-1, x+1) +1):
            for col in range(max(0, y-1), min(COLUMNS-1, y+1) +1): 
                if (row, col) not in self.dug: 
                    self.dig(row, col) 
        return True 
                


