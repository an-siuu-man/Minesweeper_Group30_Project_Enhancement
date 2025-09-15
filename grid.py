"""
    Program Name: grid.py
    Authors:
    Creation Date:
    Last modified:
    Purpose:
    Inputs:
    Outputs:
    Collaborators:
    Sources:
"""
import pygame
from settings import *
from cell import *
import random

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
        self.mine_count = bomb_amount # Total mines/bombs = total flags
        self.flags_placed = 0 # This tracks how many flags are placed
        self.dug = [] # Store values that are dug out 

    def flags_remaining(self): # Compute remaining flags as total mines minus how many flags are on the board
        return self.mine_count - self.flags_placed
    
    def toggle_flag(self, r, c): 
        cell = self.grid_list[r][c] # Add or remove a flag on cell (r,c) if allowed
        if cell.revealed: # You can't flag a cell that is already revealed
            return
        if cell.flagged: # Unflag - flip the flag off and then decrement the flags_placed
            cell.flagged = False
            self.flags_placed = max(0, self.flags_placed - 1) # We use max here to ensure the flags_placed never goes negative due to edge cases
        else:
            if self.flags_remaining() > 0: # Only place a new flag if we still have flags available
                cell.flagged = True
                self.flags_placed += 1
    
    def display_board(self):
        for row in self.grid_list: # Each row in the grid_list should have a printable format for cells
           print(row)
        print("") # Added a blank line for readability between prints

    def generate_numbers(self):
        '''
        Generates numbers for all cells that are not bombs based on adjacent bombs.
        These act as clues for the player.
        '''
        for x in range(ROWS):
            for y in range(COLUMNS):
                if self.grid_list[x][y].type != "B":
                    # If cell is not a bomb, check adjacent cells for bombs
                    total_bombs = self.check_adj_cells(x, y)

                    if total_bombs > 0:
                        # If there are adjacent bombs, set the cell image to the corresponding number image and change type to "N"
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
        Returns the total number of bombs in adjacent cells.
        '''
        total_bombs = 0
        # Checks adjacent cells starting from the top left corner (-1, -1).
        for x_offset in range(-1, 2):

            for y_offset in range(-1, 2):
                adj_x = x + x_offset
                adj_y = y + y_offset

                if self.is_inside_grid(adj_x, adj_y) and self.grid_list[adj_x][adj_y].type == "B":
                    total_bombs += 1

        return total_bombs

    def draw(self, screen):
        """
        Terminal grid output to show all the cells placed on the board
        """
        # Draw each cell onto the off-screen grid surface first
        for row in self.grid_list:
            for cell in row:
                cell.draw(self.grid_surface) #each cell knows how to draw itself

        screen.blit(self.grid_surface, (PADDING, PADDING)) #Blit the composed grid surface onto the main window at a padded offset

    def generate_bombs(self, safe_row, safe_col):
        """
        Randomly generates the positions of the bombs based on how many bombs the user wants.
        Ensure that there isn't a bomb in the user's first click by generating bombs afterwards.
        """
        planted_bombs = 0 # Count of bombs placed on board
        while planted_bombs < self.bomb_amount:
            bomb_x_coord = random.randint(0, ROWS-1) # Randomly find a row on the board
            bomb_y_coord = random.randint(0, COLUMNS - 1) # Randomly find a column on the board

            if bomb_x_coord == safe_row and bomb_y_coord == safe_col: # Do not place a bomb where the user's first click is
                continue

            if self.grid_list[bomb_x_coord][bomb_y_coord].type == "E": # Change the type of the Cell from empty to B
                self.grid_list[bomb_x_coord][bomb_y_coord].type = "B"
                self.grid_list[bomb_x_coord][bomb_y_coord].image = bomb_cell_1 if (bomb_x_coord + bomb_y_coord) % 2 == 0 else bomb_cell_2 # Make the Cell's image one of the two bombs
                planted_bombs += 1
        
        self.bombs_generated = True

    def reveal_bombs(self, clicked_row, clicked_col):
        """
        Function called once game over and user clicked on bomb.
        Reveal all the bombs that were on the grid.
        """
        for row in self.grid_list:
            for cell in row:
                if cell.flagged and cell.type != "B": # If the user flagged a cell that wasn't a bomb, then show that they made a mistake
                    if ((cell.x + cell.y) / CELLSIZE) % 2 == 0:
                        cell.image = no_bomb_cell_1 # First type of no bomb image
                    else:
                        cell.image = no_bomb_cell_2 # Second type of no bomb image

                    cell.flagged = False # Unflag it to show the cell
                    cell.revealed = True # Reveal the cell

                elif cell.type == "B": # If the cell was a bomb, then reveal it
                    if cell.x // CELLSIZE == clicked_col and cell.y // CELLSIZE == clicked_row: # If the cell was the bomb the user clicked on, show the exploding bomb image
                        if (clicked_row+clicked_col) % 2 == 0:
                            self.grid_list[clicked_row][clicked_col].image = exploded_cell_1 # First type of exploding bomb image
                        else:
                            self.grid_list[clicked_row][clicked_col].image = exploded_cell_2 # Second type of exploding bomb image

                    cell.revealed = True # Reveal the bomb cell
                    
    def check_win(self):
        """
        After every user click, check if it was a winning move.
        If all the cells are uncovered that aren't bombs, then they win.
        """
        count_revealed = 0 # Count the amount of revealed cells
        for row in self.grid_list:
            for cell in row:
                if cell.revealed == True:
                    if cell.type != "B": # If the cell isn't a bomb and it is revealed, then count it
                        count_revealed += 1

        if count_revealed == (100 - self.bomb_amount): # The total amount of cells that aren't bombs are (10*10) - amount of bombs. There are 100 cells total
            return True # If they have uncovered all non-bomb cells, then it was a winning move
        else:
            return False # Otherwise, they haven't won yet
        
    def dig(self, x, y): 
        """
        Dig function reveals numbered cells and recursively reveals neighboring cells of an empty cell.  
        """
        self.dug.append((x, y)) # Add cell to dug list once clicked on

        if self.grid_list[x][y].type == "N": # If the cell is numbered, reveal only the cell and return 
            self.grid_list[x][y].revealed = True 
            return True
        
        self.grid_list[x][y].revealed = True # If the cell is empty, reveal it 

        for row in range(max(0, x - 1), min(ROWS - 1, x + 1) + 1): # Check all neighboring cells to see if they need to be dug
            for col in range(max(0, y - 1), min(COLUMNS - 1, y + 1) + 1): 
                if (row, col) not in self.dug: # If neighbor cell hasn't been dug, recursively dig it
                    self.dig(row, col) 
                    
        return True
    