import pygame
DARKGREEN = (0,255,0)
class Game:
    def __init__ (self):
        self.layout = pygame.display.set_mode((10*40, 10*40))

        pygame.display.set_caption("Minesweeper")

        self.timer = pygame.time.Clock()

        self.grid = self.gridGeneration()
        
        self.isGameActive = True




