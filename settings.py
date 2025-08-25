#Colors 
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
LIGHTGREEN = (144)
GREEN = (0,255,0)
DARKGREEN = (0,255,0)
BLUE = (0,0,255)
DARKBLUE = (0,0,139)
LIGHTBLUE = (173,216,230)
YELLOW = (255,255,0)
DARKGREY = (40,40,40)
LIGHTGREY = (100,100,100)
BGCOLOR = DARKGREEN

#Game settings
TILESIZE = 32
ROWS = 10
COLUMNS = 10
BOMB_AMT = 10 #Need to update so user-sepecifed from 10 to 20 
WIDTH = TILESIZE * ROWS
HEIGHT = TILESIZE * COLUMNS
FPS = 60
TITLE = "Minesweeper"

#Import assets 
tile_num = []
for i in range(1,9): 
    tile_num.append(pygame.transform.scale(pygame.image.load(os.path.join("assets", f"Cell{i}.png")), (TILESIZE, TILESIZE)))

empty_tile = pygame.transform.scale(pygame.image.load(os.path.join("assets", f"CellEmpty.png")), (TILESIZE, TILESIZE)) #Update asset names accordingly 
exploded_tile = pygame.transform.scale(pygame.image.load(os.path.join("assets", f"CellExploded.png")), (TILESIZE, TILESIZE))
flag_tile = pygame.transform.scale(pygame.image.load(os.path.join("assets", f"CeilFlag.png")), (TILESIZE, TILESIZE))
bomb_tile = pygame.transform.scale(pygame.image.load(os.path.join("assets", f"CeilBomb.png")), (TILESIZE, TILESIZE))
unknown_tile = pygame.transform.scale(pygame.image.load(os.path.join("assets", f"CellUnknown.png")), (TILESIZE, TILESIZE))
nobomb_tile = pygame.transform.scale(pygame.image.load(os.path.join("assets", f"CellNoBomb.png")), (TILESIZE, TILESIZE))
