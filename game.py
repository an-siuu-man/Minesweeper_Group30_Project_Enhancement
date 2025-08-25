import pygame

DARKGREEN = (0,255,0)

class Game:
    def __init__(self):
        pygame.init()

        self.layout = pygame.display.set_mode((10*50, 10*50))

        pygame.display.set_caption("Minesweeper")

        self.timer = pygame.time.Clock()

        self.grid = self.gridGeneration()

        self.isGameActive = True

    def gridGeneration(self):
        gridStructure = [[0 for i in range(10)] for i in range(10)]
        return gridStructure
    
    def playGame(self):
        while (self.isGameActive == True):
            self.timer.tick(60)
            for action in pygame.event.get():
                if action.type == pygame.QUIT:
                    self.isGameActive = False
            
            self.layout.fill(DARKGREEN)
            pygame.display.update()
        
        pygame.quit()




