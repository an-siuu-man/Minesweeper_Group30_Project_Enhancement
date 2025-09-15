"""
    Program Name: settings.py
    Authors: Nikka Vuong, Anna Lin, Sophia Jacob, Kusuma Murthy, Nimra Syed
    Creation Date: 8/29/2025
    Last modified: 9/15/2025
    Purpose: To include all the game settings, including color scheme and sizing.
    Inputs: N/A
    Outputs: N/A
    Collaborators: N/A
    Sources: N/A
"""
import pygame
import os

# Colors 
BLACK = (0,0,0)
WHITE = (255,255,255)
LIGHTGREEN = (155, 210, 66)
DARKGREEN = (74, 117, 44)

# Game settings
CELLSIZE = 50
ROWS = 10
COLUMNS = 10
PADDING = 50
GRID_WIDTH = CELLSIZE * ROWS
GRID_HEIGHT = CELLSIZE * COLUMNS
FULL_WIDTH = GRID_WIDTH + (2 * PADDING)
FULL_HEIGHT = GRID_HEIGHT + (2 * PADDING)
TITLE = "Minesweeper"

# Import assets for number cells 1-8 
cell_num_1 = []
cell_num_2 = []
for i in range(1,9):
    cell_num_1.append(pygame.transform.scale(pygame.image.load(os.path.join("Assets", f"Cell{i}_1.png")), (CELLSIZE, CELLSIZE)))
    cell_num_2.append(pygame.transform.scale(pygame.image.load(os.path.join("Assets", f"Cell{i}_2.png")), (CELLSIZE, CELLSIZE)))

# Import assets for other cell types: empty, exploded, flag, bomb, unknown, no bomb
empty_cell_1 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", f"CellEmpty_1.png")), (CELLSIZE, CELLSIZE))
empty_cell_2 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", f"CellEmpty_2.png")), (CELLSIZE, CELLSIZE))
exploded_cell_1 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", f"CellExploded_1.png")), (CELLSIZE, CELLSIZE))
exploded_cell_2 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", f"CellExploded_2.png")), (CELLSIZE, CELLSIZE))
flag_cell_1 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", f"CellFlag_1.png")), (CELLSIZE, CELLSIZE))
flag_cell_2 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", f"CellFlag_2.png")), (CELLSIZE, CELLSIZE))
bomb_cell_1 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", f"CellBomb_1.png")), (CELLSIZE, CELLSIZE))
bomb_cell_2 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", f"CellBomb_2.png")), (CELLSIZE, CELLSIZE))
unknown_cell_1 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", f"CellUnknown_1.png")), (CELLSIZE, CELLSIZE))
unknown_cell_2 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", f"CellUnknown_2.png")), (CELLSIZE, CELLSIZE))
no_bomb_cell_1 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", f"CellNoBomb_1.png")), (CELLSIZE, CELLSIZE))
no_bomb_cell_2 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", f"CellNoBomb_2.png")), (CELLSIZE, CELLSIZE))

# Import background image
background_img = pygame.transform.scale(pygame.image.load("Assets/Background.png"), (FULL_WIDTH, FULL_HEIGHT))