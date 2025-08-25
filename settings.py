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
WIDTH = CELLSIZE * ROWS
HEIGHT = CELLSIZE * COLUMNS
FPS = 60
TITLE = "Minesweeper"

#Import assets 
cell_num = []
for i in range(1,9): 
    cell_num.append(pygame.transform.scale(pygame.image.load(os.path.join(f"Cell{i}.png")), (CELLSIZE, CELLSIZE)))

empty_cell = pygame.transform.scale(pygame.image.load(os.path.join(f"CellEmpty.png")), (CELLSIZE, CELLSIZE)) #Update asset names accordingly 
exploded_cell = pygame.transform.scale(pygame.image.load(os.path.join(f"CellExploded.png")), (CELLSIZE, CELLSIZE))
flag_cell = pygame.transform.scale(pygame.image.load(os.path.join("CellFlag.png")), (CELLSIZE, CELLSIZE))
bomb_cell = pygame.transform.scale(pygame.image.load(os.path.join(f"CellBomb.png")), (CELLSIZE, CELLSIZE))
unknown_cell = pygame.transform.scale(pygame.image.load(os.path.join(f"CellUnknown.png")), (CELLSIZE, CELLSIZE))
nobomb_cell = pygame.transform.scale(pygame.image.load(os.path.join(f"CellNoBomb.png")), (CELLSIZE, CELLSIZE))