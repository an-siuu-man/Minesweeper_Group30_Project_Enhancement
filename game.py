import pygame

DARKGREEN = (0,128,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
ROWS = 10*50
COLS = 10*50
SIZE = 50

class Game:
    def __init__(self):
        pygame.init()

        self.layout = pygame.display.set_mode((ROWS, COLS))

        pygame.display.set_caption("Minesweeper")

        self.timer = pygame.time.Clock()

        self.grid = self.empty_game_board_generation()

        self.isGameActive = True

    def empty_game_board_generation(self):
        grid_Structure = [[0 for i in range(10)] for i in range(10)]
        return grid_Structure
    
    def grid_Cells(self):
        for i in range(10):
            for j in range(10):
                cell = pygame.Rect(j*50, i*50, 50, 50)
                if self.grid[i][j] == 1:
                    cell_color = DARKGREEN
                else:
                    cell_color = GREEN
                pygame.draw.rect(self.layout, cell_color, cell)
    
    def grid_Lines(self):
        for width in range(0, 10 * 50 + 1, 50):
            pygame.draw.line(self.layout, BLACK, (width,0), (width, 10 * 50), 2)

        for height in range(0, 10 * 50 + 1, 50):
            pygame.draw.line(self.layout, BLACK, (0, height), (10 * 50, height), 2)
    
    def play_Game(self):
        while (self.isGameActive == True):
            self.timer.tick(60)
            for action in pygame.event.get():
                if action.type == pygame.QUIT:
                    self.isGameActive = False
                if action.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    row = y // 50
                    col = x // 50

                    self.grid[row][col] = 1

            self.grid_Cells()
            self.grid_Lines()
            pygame.display.update()
        
        pygame.quit()




