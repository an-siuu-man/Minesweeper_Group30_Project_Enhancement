"""
    Program Name: cell.py
    Authors: Anna Lin, Sophia Jacob, Kusuma Murthy, Nikka Voung, Nimra Syed
    Creation Date: 8/29/2025
    Last modified: 9/15/2025
    Purpose: To create a Cell class that will house all the attributes tied to each cell in the board.
    Inputs: Cell position.
    Outputs: N/A
    Collaborators: N/A
    Sources: N/A
"""

from settings import *
class Cell:
    def __init__(self, x, y, image, type = "E", revealed = False, flagged = False):
        """
        Initalizes cell object.
        """
        self.x = x * CELLSIZE
        self.y = y * CELLSIZE
        self.image = image
        self.type = type # Types: B = Bomb, E = Empty, N = Number
        self.revealed = revealed
        self.flagged = flagged

    def draw(self, grid_surface):
        """
        Draws the cell on the grid surface.
        """
        if self.revealed:
            if not self.flagged:
                # Draw numbered, bomb, empty, or exploded cell if revealed
                grid_surface.blit(self.image, (self.x, self.y))
        else:
            # Draw flagged if not revealed
            if self.flagged:
                if ((self.x + self.y) // CELLSIZE) % 2 == 0:
                    grid_surface.blit(flag_cell_1, (self.x, self.y))
                else:
                    grid_surface.blit(flag_cell_2, (self.x, self.y))
                    
            # Draw unknown cell if not revealed
            else:
                if ((self.x + self.y) // CELLSIZE) % 2 == 0:
                    grid_surface.blit(unknown_cell_1, (self.x, self.y))
                else:
                    grid_surface.blit(unknown_cell_2, (self.x, self.y))

    def __repr__(self):
        """
        Printed representation of the cell for debugging.
        """
        return self.type
        