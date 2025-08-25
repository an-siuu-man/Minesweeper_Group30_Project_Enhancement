import pygame
from settings import *
from assets import *


class Game:
    def __init__(self):
        pygame.init()

        self.layout = pygame.display.set_mode((COLUMNS * CELLSIZE, ROWS * CELLSIZE))

        pygame.display.set_caption("Minesweeper")

        self.timer = pygame.time.Clock()

        self.isGameActive = True

        self.grid = Grid()

    def empty_game_board_generation(self):
        grid_Structure = [[0 for i in range(COLUMNS)] for i in range(ROWS)]
        return grid_Structure
    
    def grid_Cells(self):
        for i in range(10):
            for j in range(10):
                cell = pygame.Rect(j*CELLSIZE, i*CELLSIZE, CELLSIZE, CELLSIZE)
                if self.grid[i][j] == 1:
                    cell_color = DARKGREEN
                else:
                    cell_color = GREEN
                pygame.draw.rect(self.layout, cell_color, cell)
    
    def grid_Lines(self):
        for width in range(0, (COLUMNS * CELLSIZE) + 1, CELLSIZE):
            pygame.draw.line(self.layout, BLACK, (width,0), (width, ROWS * CELLSIZE), 2)

        for height in range(0, (ROWS * CELLSIZE) + 1, CELLSIZE):
            pygame.draw.line(self.layout, BLACK, (0, height), (COLUMNS * CELLSIZE, height), 2)

    def play_Game(self):
        while (self.isGameActive == True):
            self.timer.tick(60)
            for action in pygame.event.get():
                if action.type == pygame.QUIT:
                    self.isGameActive = False

                if action.type == pygame.MOUSEBUTTONDOWN:
                    row,col = (pygame.mouse.get_pos()[1] // CELLSIZE, pygame.mouse.get_pos()[0] // CELLSIZE)
                    cell = self.grid.grid_list[row][col]
                    cell.revealed = True

                    if cell.type == "B":
                        print("Game Over!")
                    else:
                        cell.revealed = True

            self.layout.fill(DARKGREEN)
            self.grid.draw(self.layout)
            self.grid_Lines()
            pygame.display.update()
        
        pygame.quit()
