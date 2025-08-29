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
        self.grid.display_board()
        self.state = "front-page"

    def empty_game_board_generation(self):
        grid_Structure = [[0 for i in range(COLUMNS)] for i in range(ROWS)]
        return grid_Structure
    
    def grid_cells(self):
        for i in range(10):
            for j in range(10):
                cell = pygame.Rect(j*CELLSIZE, i*CELLSIZE, CELLSIZE, CELLSIZE)
                if self.grid[i][j] == 1:
                    cell_color = DARKGREEN
                else:
                    cell_color = GREEN
                pygame.draw.rect(self.layout, cell_color, cell)

    def front_page(self):
        self.layout.fill(DARKGREEN)
        title_font = pygame.font.SysFont("Times New Roman", 72, bold=True)
        front_page_title = title_font.render(TITLE, True, BLUE)
        title_pos = front_page_title.get_rect(center=(COLUMNS * CELLSIZE // 2, ROWS * CELLSIZE // 3))
        self.layout.blit(front_page_title, title_pos)
        button_font = pygame.font.SysFont("Times New Roman", 40, bold=True)
        button_title = button_font.render("Generate", True, BLUE)
        button_pos = pygame.Rect(0,0,200,60)
        button_pos.center = (COLUMNS * CELLSIZE // 2, ROWS * CELLSIZE // 1.5)
        pygame.draw.rect(self.layout, LIGHTBLUE, button_pos)
        self.layout.blit(button_title, button_title.get_rect(center=button_pos.center))
        return button_pos

    def play_game(self):
        while (self.isGameActive == True):
            self.timer.tick(60)
            for action in pygame.event.get():
                if action.type == pygame.QUIT:
                    self.isGameActive = False
                if self.state == "front-page":
                    if action.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.front_page().collidepoint(mouse_pos):
                            self.state = "play"
                elif self.state == "play":
                    if action.type == pygame.MOUSEBUTTONDOWN:
                        row,col = (pygame.mouse.get_pos()[1] // CELLSIZE, pygame.mouse.get_pos()[0] // CELLSIZE)
                        cell = self.grid.grid_list[row][col]
                        cell.revealed = True

                        if cell.type == "B":
                            print("Game Over!")
                        else:
                            cell.revealed = True
            if self.state == "front-page":
                self.front_page()
            elif self.state == "play":
                self.layout.fill(DARKGREEN)
                self.grid.draw(self.layout)
                # self.grid_lines()
            pygame.display.update()
        
        pygame.quit()
