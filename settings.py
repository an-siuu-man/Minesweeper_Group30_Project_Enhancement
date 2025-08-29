import pygame
import os

#Colors 
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
LIGHTGREEN = (144)
GREEN = (0,255,0)
DARKGREEN = (0,128,0)
BLUE = (0,0,255)
DARKBLUE = (0,0,139)
LIGHTBLUE = (173,216,230)
YELLOW = (255,255,0)
DARKGREY = (40,40,40)
LIGHTGREY = (100,100,100)
BGCOLOR = DARKGREEN

#Game settings
CELLSIZE = 50
ROWS = 10
COLUMNS = 10
BOMB_AMT = 10 #Need to update so user-sepecifed from 10 to 20 
HUD_HEIGHT = 40
WIDTH = CELLSIZE * ROWS
HEIGHT = CELLSIZE * COLUMNS
FPS = 60
TITLE = "Minesweeper"

#Import assets 
cell_num_1 = []
cell_num_2 = []
for i in range(1,9):
    cell_num_1.append(pygame.transform.scale(pygame.image.load(os.path.join("Assets", f"Cell{i}_1.png")), (CELLSIZE, CELLSIZE)))
    cell_num_2.append(pygame.transform.scale(pygame.image.load(os.path.join("Assets", f"Cell{i}_2.png")), (CELLSIZE, CELLSIZE)))

#Update asset names accordingly 
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
no_bomb_cell_1 = pygame.transform.scale(pygame.image.load(os.path.join("Assets", f"CellNoBomb_2.png")), (CELLSIZE, CELLSIZE))
