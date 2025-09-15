"""
    Program Name: game.py
    Authors: Kusuma Murthy, Sophia Jacob, Anna Lin, Nikka Voung, Nimra Syed
    Creation Date:
    Last modified:
    Purpose:
    Inputs:
    Outputs:
    Collaborators:
    Sources:
"""
import pygame
from settings import * # Imports global constants and settings
from cell import * # Import cell-related logic for Minesweeper
from grid import * # Import grid logic for Minesweeper

class Game:
    def __init__(self):
        """
        Initializes the game window, settings, and audio.
        """
        pygame.init() # Initialize the pygame
    
        # This following block sets up the display window
        self.layout = pygame.display.set_mode((FULL_WIDTH, FULL_HEIGHT))
        pygame.display.set_caption("Minesweeper")

        # The following variable are the game control attributes
        self.timer = pygame.time.Clock()
        self.isGameActive = True # Default state
        self.grid = None # Grid object created when the game starts
        self.gameover_click = False # Default state
        self.state = "front-page" # Default page
        self.bomb_amount = 10 # Default number of bombs
        self.bomb_min = 10 # Default lower limit for bomb selection
        self.bomb_max = 20 # Default upper limit for bomb selection

        # This block of code is related to the game's Audio
        pygame.mixer.init()
        pygame.mixer.music.load('Assets/game-music.wav') # Background music
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1) # This will allow the background music to loop forever
        self.game_over_sound = pygame.mixer.Sound("Assets/game-lose-music.wav") # Add game losing music
        self.game_win_sound = pygame.mixer.Sound("Assets/game-win-music.wav") # Add game winning music
        pygame.mixer.init()

    def front_page(self):
        """
        Display the front page menu where the player can see the game title, select the number of bomns, and start the game.
        """
        # This is the background and title
        self.layout.blit(background_img, (0, 0))
        title_font = pygame.font.SysFont("Verdana", 55, bold = True)
        front_page_title = title_font.render(TITLE, True, BLACK)
        title_pos = front_page_title.get_rect(center = (FULL_WIDTH // 2, FULL_HEIGHT // 3))
        self.layout.blit(front_page_title, title_pos)

        # This is for the display of amount of bombs selected
        bomb_selector_font = pygame.font.SysFont("Verdana",25, bold = True)
        bomb_selector_text = bomb_selector_font.render(f"Bombs: {self.bomb_amount}", True, BLACK)
        bomb_selector_pos = bomb_selector_text.get_rect(center = (FULL_WIDTH // 2, FULL_HEIGHT // 2))
        self.layout.blit(bomb_selector_text, bomb_selector_pos)

        # This is the arrows for adding more/less bombs
        left_arrow = pygame.Rect(bomb_selector_pos.left - 40, bomb_selector_pos.centery - 15, 30, 30) # The left arrow button decreases the nummber of bombs
        right_arrow = pygame.Rect(bomb_selector_pos.right + 10, bomb_selector_pos.centery - 15, 30, 30) # The right arrow button increases the number of bombs
        # Formatting the arrows as triangles
        pygame.draw.polygon(self.layout, LIGHTGREEN, [(left_arrow.right, left_arrow.top), (left_arrow.right, left_arrow.bottom), (left_arrow.left, left_arrow.centery)])
        pygame.draw.polygon(self.layout, LIGHTGREEN, [(right_arrow.left, right_arrow.top), (right_arrow.left, right_arrow.bottom), (right_arrow.right, right_arrow.centery)])

        # Play Game Button
        button_font = pygame.font.SysFont("Verdana", 30, bold = True)
        button_title = button_font.render("Play Game!", True, WHITE)
        button_pos = pygame.Rect(0, 0, 220, 60) # Rectangular button
        button_pos.center = (FULL_WIDTH // 2, FULL_HEIGHT // 1.5) # Position the button to the center
        pygame.draw.rect(self.layout, LIGHTGREEN, button_pos, border_radius = 15) # Draws the buttom
        self.layout.blit(button_title, button_title.get_rect(center = button_pos.center)) # Draws the text on the button

        return button_pos, left_arrow, right_arrow # Returns the button rectangles for click detection

    def draw_hud(self):
        """
        Displays heads up display (HUD) which includes the flags left, mines left, and game status.
        """
        if hasattr(self.grid, "flags_remaining"):
            # Display the flags left
            hud_font = pygame.font.SysFont("Verdana", 16, bold = True)
            flags_text = hud_font.render(f"Flags Left: {self.grid.flags_remaining()}", True, WHITE)
            text_rect = flags_text.get_rect(center=((flags_text.get_width() // 2) + 25, PADDING // 2))
            self.layout.blit(flags_text, text_rect)

            # Display the current game status
            hud_font = pygame.font.SysFont("Verdana", 24, bold = True)
            status_text = hud_font.render("Playing", True, WHITE)
            text_rect = status_text.get_rect(center = (self.layout.get_width() // 2, PADDING // 2))
            self.layout.blit(status_text, text_rect)

            #Display the mines left
            hud_font = pygame.font.SysFont("Verdana", 16, bold = True)
            mines_text = hud_font.render(f"Mines Left: {self.grid.flags_remaining()}", True, WHITE)
            text_rect = mines_text.get_rect(center = (self.layout.get_width() - (mines_text.get_width() // 2) - 25, PADDING // 2))
            self.layout.blit(mines_text, text_rect)

    def draw_label(self):
        """
        Draws the row and column labels, around the grid. Columns are denoted by letters (A-J) and rows are denoted by numbers (1-10).
        """
        font = pygame.font.SysFont("Verdana", 15, bold = True)

        # Draw column labels (A-J)
        for col in range(COLUMNS):
            label = chr(ord('A') + col) # Converts the column indec to letters
            text = font.render(label, True, WHITE)
            text_rect = text.get_rect(
                center=(PADDING + col * CELLSIZE + CELLSIZE // 2,  # X centered over cell
                        FULL_HEIGHT - PADDING // 2) # Bottom padding center
            )
            self.layout.blit(text, text_rect)

        # Draw row labels (1-10)
        for row in range(ROWS):
            label = str(row + 1)
            text = font.render(label, True, WHITE)
            text_rect = text.get_rect(
                center=(PADDING // 2, # Left padding center
                        PADDING + row * CELLSIZE + CELLSIZE // 2) # Y centered to cell
            )
            self.layout.blit(text, text_rect)

    def play_game(self):
        """
        Main game loop that handles game states, user inputs, and rendering.
        """
        # This is the main game loop
        while (self.isGameActive or self.state == "game-win"):
            self.timer.tick(60) # Runs the loop at 60 FPS

            for action in pygame.event.get():
                if action.type == pygame.QUIT: # Quit event quits the game and closes the window
                    self.isGameActive = False # Exits the game

                if self.state == "front-page": # Front page code
                    self.front_page()

                    if action.type == pygame.MOUSEBUTTONDOWN: # Detects the mouse button down action
                        mouse_pos = pygame.mouse.get_pos()
                        button_pos, left_arrow, right_arrow = self.front_page()

                        # Adjust the bomb amount with arrows
                        if left_arrow.collidepoint(mouse_pos) and (self.bomb_amount > self.bomb_min):
                            self.bomb_amount -= 1
                        elif right_arrow.collidepoint(mouse_pos) and (self.bomb_amount < self.bomb_max):
                            self.bomb_amount += 1
                        # Start the game when the "Play" button is clicked
                        elif button_pos.collidepoint(mouse_pos):
                            self.grid = Grid(bomb_amount = self.bomb_amount)
                            self.grid.display_board()
                            self.state = "play"

                # This is the game play logic
                elif self.state == "play":
                    self.layout.fill(DARKGREEN) # Background color
                    self.draw_hud() # Show HUD
                    self.draw_label() # Show labels
                    self.grid.draw(self.layout) # Draw the grid

                    if action.type == pygame.MOUSEBUTTONDOWN:
                       # Get grid cordinates from mouse position
                        mx, my = pygame.mouse.get_pos()
                        row, col = (my - PADDING) // CELLSIZE, (mx - PADDING) // CELLSIZE
                        if my < PADDING or mx < PADDING or row >= ROWS or col >= COLUMNS: # If click is outside the grid, ignore
                            continue
                        cell = self.grid.grid_list[row][col]
                        
                        # Generates the bumbs on the first click and ensures the first click is a safe click
                        if self.grid.bombs_generated == False:
                            self.grid.generate_bombs(row,col)
                            self.grid.generate_numbers()
                            self.grid.display_board()

                        # Right-click toggles flag added
                        if action.button == 3:
                            if hasattr(self.grid, "toggle_flag"):
                                self.grid.toggle_flag(row, col)
                            # do not continue to uncover on right-click
                            continue

                        # Left-click logic, but block if flagged
                        if action.button == 1:
                            if getattr(cell, "flagged", False):
                                # can't uncover a flagged cell
                                continue

                            if cell.type == "B": # is the clicked cell is the bomb then game over
                                self.state = "game-over"
                                self.game_over_sound.play()
                            else: # It is a safe cell, therefore we do the recursive dig function
                                self.grid.dig(row,col)
                            
                            # Check the win condition
                            if self.grid.check_win(): # If not a bomb, check if this was the winning move.
                                self.state = "game-win"
                                self.game_win_sound.play()

                # This is the game over logic
                elif self.state == "game-over":
                    self.grid.reveal_bombs(row, col) # Show/reveal all of the bombs on the grid
                    self.layout.fill(DARKGREEN)
                    self.draw_hud()
                    self.draw_label()
                    self.grid.draw(self.layout)
                    retry = self.game_over_page()

                    if action.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()

                        if retry.collidepoint(mouse_pos):
                            self.retry()

                # This is the game win logic
                elif self.state == "game-win":
                    self.layout.fill(DARKGREEN)
                    self.draw_hud()
                    self.draw_label()
                    self.grid.draw(self.layout)
                    retry = self.game_win_page()

                    if action.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()

                        if retry.collidepoint(mouse_pos):
                            self.retry()

            pygame.display.update() # Refreshes the screen each frame
        
        pygame.quit() # Ends the game when the loop exists

    def game_ended_page (self, text):
        """
        Draws the overlay show when the game ends and it also shows the win, loose and retry button/screens.
        """
        # Creates the transparent overlay
        overlay = pygame.Surface((FULL_WIDTH, FULL_HEIGHT), pygame.SRCALPHA)
        overlay.fill((100, 100, 100, 100))
        self.layout.blit(overlay, (0, 0))

        # Creates the end-game text
        font = pygame.font.SysFont("Verdana", 55, bold = True)
        text = font.render(text, True, BLACK)
        text_rect = text.get_rect(center = (FULL_WIDTH // 2, FULL_HEIGHT // 2 - 20))
        self.layout.blit(text, text_rect)

        # Creates the rety button
        retry_image = pygame.image.load("Assets/Retry.png").convert_alpha()
        retry_image_scaled = pygame.transform.scale(retry_image, (60, 60))
        retry_circle_layer = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(retry_circle_layer, (255, 255, 255, 255), (30, 30), 30)
        retry_circle_image = retry_image_scaled.copy()
        retry_circle_image.blit(retry_circle_layer, (0, 0), special_flags = pygame.BLEND_RGBA_MIN)

        retry_rect = retry_circle_image.get_rect(center = (FULL_WIDTH // 2, FULL_HEIGHT // 2 + 60))
        self.layout.blit(retry_circle_image, retry_rect)

        return retry_rect # Returns the retry button
    
    def game_over_page(self):
        """
        Shows the game over screen with a retry button option.
        """
        return self.game_ended_page("GAME OVER!")

    def game_win_page(self):
        """
        Shows the win screen with a retry button option.
        """
        return self.game_ended_page("YOU WIN!")
    
    def retry(self):
        """
        It resets the game state to play again if the retry button was selected.
        """
        self.grid = Grid(bomb_amount = self.bomb_amount) # This resets the grid
        self.state = "front-page" # This directs the pplayer back to the front page
        