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
        self.grid = None
        # self.grid.display_board()
        self.state = "front-page"
        self.bomb_amount = 10 # Default
        self.bomb_min = 10
        self.bomb_max = 20

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
        # This is for the display of amount of bombs selected.
        bomb_selector_font = pygame.font.SysFont("Times New Roman", 32)
        bomb_selector_text = bomb_selector_font.render(f"Bombs: {self.bomb_amount}", True, WHITE)
        bomb_selector_pos = bomb_selector_text.get_rect(center=(COLUMNS * CELLSIZE // 2, ROWS * CELLSIZE // 2))
        self.layout.blit(bomb_selector_text, bomb_selector_pos)
        # This is the arrows for adding more/less bombs.
        left_arrow = pygame.Rect(bomb_selector_pos.left - 40, bomb_selector_pos.centery - 15, 30, 30)
        right_arrow = pygame.Rect(bomb_selector_pos.right + 10, bomb_selector_pos.centery - 15, 30, 30)
        pygame.draw.polygon(self.layout, LIGHTBLUE, [(left_arrow.right, left_arrow.top), (left_arrow.right, left_arrow.bottom), (left_arrow.left, left_arrow.centery)])
        pygame.draw.polygon(self.layout, LIGHTBLUE, [(right_arrow.left, right_arrow.top), (right_arrow.left, right_arrow.bottom), (right_arrow.right, right_arrow.centery)])
        # Button to generate.
        button_font = pygame.font.SysFont("Times New Roman", 40, bold=True)
        button_title = button_font.render("Generate", True, BLUE)
        button_pos = pygame.Rect(0, 0, 200, 60)
        button_pos.center = (COLUMNS * CELLSIZE // 2, ROWS * CELLSIZE // 1.5)
        pygame.draw.rect(self.layout, LIGHTBLUE, button_pos)
        self.layout.blit(button_title, button_title.get_rect(center=button_pos.center))

        return button_pos, left_arrow, right_arrow


    def play_game(self):
        while (self.isGameActive == True):
            self.timer.tick(60)
            for action in pygame.event.get():
                if action.type == pygame.QUIT:
                    self.isGameActive = False
                if self.state == "front-page":
                    if action.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        button_pos, left_arrow, right_arrow = self.front_page()
                        if left_arrow.collidepoint(mouse_pos):
                            if self.bomb_amount > self.bomb_min:
                                self.bomb_amount -=1
                        elif right_arrow.collidepoint(mouse_pos):
                            if self.bomb_amount < self.bomb_max:
                                self.bomb_amount +=1
                        elif button_pos.collidepoint(mouse_pos):
                            self.grid = Grid(bomb_amount=self.bomb_amount)
                            self.grid.display_board()
                            self.state = "play"

                elif self.state == "play":
                    if action.type == pygame.MOUSEBUTTONDOWN:
                        row,col = (pygame.mouse.get_pos()[1] // CELLSIZE, pygame.mouse.get_pos()[0] // CELLSIZE)
                        cell = self.grid.grid_list[row][col]
                        
                        if self.grid.bombs_generated == False:
                            self.grid.generate_bombs(row,col)
                            self.grid.generate_numbers()
                            self.grid.display_board()
                            
                        cell.revealed = True

                        if cell.type == "B":
                            self.state = "game-over"
                            #print("Game Over!")
                        #else:
                            #cell.revealed = True
            if self.state == "front-page":
                self.front_page()
            elif self.state == "play":
                self.layout.fill(DARKGREEN)
                self.grid.draw(self.layout)
                # self.grid_lines()
            elif self.state == "game-over":
                self.layout.fill(DARKGREEN)
                self.grid.draw(self.layout)
                self.game_over_page()
            pygame.display.update()
        
        pygame.quit()

    def game_over_page(self):
        overlay = pygame.Surface((COLUMNS * CELLSIZE, ROWS * CELLSIZE), pygame.SRCALPHA)
        overlay.fill((100, 100, 100, 100))
        self.layout.blit(overlay, (0, 0))

        font = pygame.font.SysFont("Times New Roman", 60, bold=True)
        text = font.render("Game Over!", True, BLACK)
        text_rect = text.get_rect(center=(COLUMNS * CELLSIZE // 2, ROWS * CELLSIZE // 2))
        self.layout.blit(text, text_rect)