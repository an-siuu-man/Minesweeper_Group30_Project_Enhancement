"""
    Program Name: game.py
    Authors: Kusuma Murthy, Sophia Jacob, Anna Lin, Nikka Voung, Nimra Syed
    Creation Date: 8/29/2025
    Last modified: 9/15/2025
    Purpose: To create a fully functioning game board and the interactive UI.
    Inputs: Bomb amount that the user wants and clicks/actions for the cells
    Outputs: An updating game board based on the user's actions to uncover and reveal cells and play the game.
    Collaborators: N/A
    Sources: N/A
"""

import pygame
import random
from settings import * # Imports global constants and settings
from cell import * # Import cell-related logic for Minesweeper
from grid import * # Import grid logic for Minesweeper
from ai_solver import AISolver # Import AI solver for computer player

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

        # AI mode attributes
        self.ai_mode = False # Default: human player
        self.ai_difficulty = "easy" # Default AI difficulty
        self.ai_solver = None # AI solver instance
        self.ai_move_delay = 500 # Delay in milliseconds between AI moves
        self.last_ai_move_time = 0 # Track time of last AI move
        
        # Turn-by-turn mode attributes
        self.turn_by_turn = True # Default: cooperative turn-by-turn mode
        self.current_turn = "human" # Whose turn it is: "human" or "ai"
        self.ai_turn_ready = False # Flag to trigger AI turn
        
        # Track last clicked position for game over screen
        self.last_clicked_row = 0
        self.last_clicked_col = 0

        # This block of code is related to the game's Audio
        pygame.mixer.init()
        pygame.mixer.music.load('Assets/game-music.wav') # Background music
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1) # This will allow the background music to loop forever
        self.game_over_sound = pygame.mixer.Sound("Assets/game-lose-music.wav") # Add game losing music
        self.game_win_sound = pygame.mixer.Sound("Assets/game-win-music.wav") # Add game winning music
        pygame.mixer.init()

        # Hint system
        self.hints_safe = 3   # number of safe cell hints available
        self.hints_bomb = 2   # number of bomb hints available
        self.hint_button_rect = None
        self.hint_dropdown_open = False
        self.hint_safe_rect = None
        self.hint_bomb_rect = None

    def front_page(self):
        """
        Display the front page menu where the player can see the game title, select the number of bomns, and start the game.
        """
        # This is the background and title
        self.layout.blit(background_img, (0, 0))
        title_font = pygame.font.SysFont("Verdana", 55, bold = True)
        front_page_title = title_font.render(TITLE, True, BLACK)
        title_pos = front_page_title.get_rect(center = (FULL_WIDTH // 2, FULL_HEIGHT // 4))
        self.layout.blit(front_page_title, title_pos)

        # This is for the display of amount of bombs selected
        bomb_selector_font = pygame.font.SysFont("Verdana",25, bold = True)
        bomb_selector_text = bomb_selector_font.render(f"Bombs: {self.bomb_amount}", True, BLACK)
        bomb_selector_pos = bomb_selector_text.get_rect(center = (FULL_WIDTH // 2, FULL_HEIGHT // 2.5))
        self.layout.blit(bomb_selector_text, bomb_selector_pos)

        # This is the arrows for adding more/less bombs
        left_arrow = pygame.Rect(bomb_selector_pos.left - 40, bomb_selector_pos.centery - 15, 30, 30) # The left arrow button decreases the nummber of bombs
        right_arrow = pygame.Rect(bomb_selector_pos.right + 10, bomb_selector_pos.centery - 15, 30, 30) # The right arrow button increases the number of bombs
        # Formatting the arrows as triangles
        pygame.draw.polygon(self.layout, LIGHTGREEN, [(left_arrow.right, left_arrow.top), (left_arrow.right, left_arrow.bottom), (left_arrow.left, left_arrow.centery)])
        pygame.draw.polygon(self.layout, LIGHTGREEN, [(right_arrow.left, right_arrow.top), (right_arrow.left, right_arrow.bottom), (right_arrow.right, right_arrow.centery)])

        # AI Mode Toggle Button
        ai_toggle_font = pygame.font.SysFont("Verdana", 22, bold = True)
        ai_mode_text = "AI Mode: ON" if self.ai_mode else "AI Mode: OFF"
        ai_toggle_text = ai_toggle_font.render(ai_mode_text, True, WHITE)
        ai_toggle_pos = pygame.Rect(0, 0, 200, 50)
        ai_toggle_pos.center = (FULL_WIDTH // 2, FULL_HEIGHT // 1.9)
        button_color = LIGHTGREEN if self.ai_mode else DARKGREEN
        pygame.draw.rect(self.layout, button_color, ai_toggle_pos, border_radius = 10)
        self.layout.blit(ai_toggle_text, ai_toggle_text.get_rect(center = ai_toggle_pos.center))

        # AI Difficulty Selector (only shown when AI mode is ON)
        ai_diff_left = None
        ai_diff_right = None
        if self.ai_mode:
            diff_font = pygame.font.SysFont("Verdana", 20, bold = True)
            diff_text = diff_font.render(f"Difficulty: {self.ai_difficulty.upper()}", True, BLACK)
            diff_pos = diff_text.get_rect(center = (FULL_WIDTH // 2, FULL_HEIGHT // 1.65))
            self.layout.blit(diff_text, diff_pos)

            # Arrows for difficulty selection
            ai_diff_left = pygame.Rect(diff_pos.left - 40, diff_pos.centery - 12, 25, 25)
            ai_diff_right = pygame.Rect(diff_pos.right + 15, diff_pos.centery - 12, 25, 25)
            pygame.draw.polygon(self.layout, LIGHTGREEN, [(ai_diff_left.right, ai_diff_left.top), (ai_diff_left.right, ai_diff_left.bottom), (ai_diff_left.left, ai_diff_left.centery)])
            pygame.draw.polygon(self.layout, LIGHTGREEN, [(ai_diff_right.left, ai_diff_right.top), (ai_diff_right.left, ai_diff_right.bottom), (ai_diff_right.right, ai_diff_right.centery)])

        # Play Game Button
        button_font = pygame.font.SysFont("Verdana", 30, bold = True)
        button_title = button_font.render("Play Game!", True, WHITE)
        button_pos = pygame.Rect(0, 0, 220, 60) # Rectangular button
        button_pos.center = (FULL_WIDTH // 2, FULL_HEIGHT // 1.4) # Position the button to the center
        pygame.draw.rect(self.layout, LIGHTGREEN, button_pos, border_radius = 15) # Draws the buttom
        self.layout.blit(button_title, button_title.get_rect(center = button_pos.center)) # Draws the text on the button

        return button_pos, left_arrow, right_arrow, ai_toggle_pos, ai_diff_left, ai_diff_right # Returns the button rectangles for click detection

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
            if self.ai_mode and self.turn_by_turn:
                # Show whose turn it is in turn-by-turn mode
                turn_color = LIGHTGREEN if self.current_turn == "human" else (255, 200, 100)
                if self.current_turn == "human":
                    status_text = hud_font.render(f"Your Turn", True, turn_color)
                else:
                    status_text = hud_font.render(f"AI Turn ({self.ai_difficulty.upper()})", True, turn_color)
            elif self.ai_mode:
                status_text = hud_font.render(f"AI Playing ({self.ai_difficulty.upper()})", True, WHITE)
            else:
                status_text = hud_font.render("Playing", True, WHITE)
            text_rect = status_text.get_rect(center = (self.layout.get_width() // 2, PADDING // 2))
            self.layout.blit(status_text, text_rect)
            '''
            #Display the mines left
            hud_font = pygame.font.SysFont("Verdana", 16, bold = True)
            mines_text = hud_font.render(f"Mines Left: {self.grid.flags_remaining()}", True, WHITE)
            text_rect = mines_text.get_rect(center = (self.layout.get_width() - (mines_text.get_width() // 2) - 25, PADDING // 2))
            self.layout.blit(mines_text, text_rect)
            '''
            #Display hint button
            hint_button_font = pygame.font.SysFont("Verdana", 16, bold = True)
            total_hints = self.hints_safe + self.hints_bomb
            hint_button_text = hint_button_font.render(f"Hint ({total_hints})", True, WHITE)
            # create a button rect slightly larger than the text and position it at the same center
            button_w = hint_button_text.get_width() + 16
            button_h = hint_button_text.get_height() + 8
            hint_button_rect = pygame.Rect(0, 0, button_w, button_h)
            hint_button_rect.center = (self.layout.get_width() - (hint_button_text.get_width() // 2) - 25, PADDING // 2)
            
            # Color the button differently based on availability
            button_color = LIGHTGREEN if total_hints > 0 else (128, 128, 128)  # Gray if no hints left

             # draw background for the button and blit the text centered on it
            pygame.draw.rect(self.layout, button_color, hint_button_rect, border_radius = 6)
            self.layout.blit(hint_button_text, hint_button_text.get_rect(center = hint_button_rect.center))
            # store rect for click detection
            self.hint_button_rect = hint_button_rect
    def draw_hint_dropdown(self):
            """
            Draws the hint dropdown menu on top of everything else.
            """
            if self.hint_dropdown_open and self.hint_button_rect:
                dropdown_font = pygame.font.SysFont("Verdana", 14, bold = True)
                
                # Calculate dropdown dimensions first
                safe_text = dropdown_font.render(f"Reveal Safe ({self.hints_safe})", True, WHITE)
                bomb_text = dropdown_font.render(f"Reveal Bomb ({self.hints_bomb})", True, WHITE)
                
                # Use the wider text to determine dropdown width
                max_text_width = max(safe_text.get_width(), bomb_text.get_width())
                dropdown_width = max_text_width + 12
                dropdown_height = (safe_text.get_height() + 6) * 2 + 2  # 2 options + gap
                
                # Calculate position - check if dropdown would go off screen
                dropdown_x = self.hint_button_rect.left
                dropdown_y = self.hint_button_rect.bottom + 2
                
                # Adjust x position if dropdown would go off the right edge
                if dropdown_x + dropdown_width > FULL_WIDTH:
                    dropdown_x = FULL_WIDTH - dropdown_width - 10  # 10px margin from edge
                
                # Ensure dropdown doesn't go off the left edge
                if dropdown_x < 10:
                    dropdown_x = 10
                
                # Safe cell option
                safe_h = safe_text.get_height() + 6
                safe_rect = pygame.Rect(dropdown_x, dropdown_y, dropdown_width, safe_h)
                safe_color = LIGHTGREEN if self.hints_safe > 0 else (128, 128, 128)
                pygame.draw.rect(self.layout, safe_color, safe_rect, border_radius = 4)
                self.layout.blit(safe_text, safe_text.get_rect(center = safe_rect.center))
                self.hint_safe_rect = safe_rect
                
                # Bomb cell option
                bomb_h = bomb_text.get_height() + 6
                bomb_rect = pygame.Rect(dropdown_x, safe_rect.bottom + 2, dropdown_width, bomb_h)
                bomb_color = LIGHTGREEN if self.hints_bomb > 0 else (128, 128, 128)
                pygame.draw.rect(self.layout, bomb_color, bomb_rect, border_radius = 4)
                self.layout.blit(bomb_text, bomb_text.get_rect(center = bomb_rect.center))
                self.hint_bomb_rect = bomb_rect
            else:
                self.hint_safe_rect = None
                self.hint_bomb_rect = None
          
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
                        button_pos, left_arrow, right_arrow, ai_toggle_pos, ai_diff_left, ai_diff_right = self.front_page()

                        # Adjust the bomb amount with arrows
                        if left_arrow.collidepoint(mouse_pos) and (self.bomb_amount > self.bomb_min):
                            self.bomb_amount -= 1
                        elif right_arrow.collidepoint(mouse_pos) and (self.bomb_amount < self.bomb_max):
                            self.bomb_amount += 1
                        # Toggle AI mode
                        elif ai_toggle_pos.collidepoint(mouse_pos):
                            self.ai_mode = not self.ai_mode
                        # Adjust AI difficulty
                        elif self.ai_mode and ai_diff_left and ai_diff_left.collidepoint(mouse_pos):
                            difficulties = ["easy", "medium", "hard"]
                            current_idx = difficulties.index(self.ai_difficulty)
                            self.ai_difficulty = difficulties[(current_idx - 1) % 3]
                        elif self.ai_mode and ai_diff_right and ai_diff_right.collidepoint(mouse_pos):
                            difficulties = ["easy", "medium", "hard"]
                            current_idx = difficulties.index(self.ai_difficulty)
                            self.ai_difficulty = difficulties[(current_idx + 1) % 3]
                        # Start the game when the "Play" button is clicked
                        elif button_pos.collidepoint(mouse_pos):
                            self.grid = Grid(bomb_amount = self.bomb_amount)
                            self.grid.display_board()
                            if self.ai_mode:
                                self.ai_solver = AISolver(difficulty=self.ai_difficulty)
                                self.last_ai_move_time = pygame.time.get_ticks()
                                self.current_turn = "human"  # Human always starts
                                self.ai_turn_ready = False
                            self.state = "play"

                # This is the game play logic
                elif self.state == "play":
                    self.layout.fill(DARKGREEN) # Background color
                    self.draw_hud() # Show HUD
                    self.draw_label() # Show labels
                    self.grid.draw(self.layout) # Draw the grid
                    self.draw_hint_dropdown() # Draw hint dropdown if open

                    # Handle AI moves based on mode
                    if self.ai_mode and self.ai_solver:
                        if self.turn_by_turn:
                            # Turn-by-turn mode: AI only moves on its turn
                            if self.current_turn == "ai" and self.ai_turn_ready:
                                current_time = pygame.time.get_ticks()
                                if current_time - self.last_ai_move_time >= self.ai_move_delay:
                                    self.last_ai_move_time = current_time
                                    self._make_ai_move()
                                    self.ai_turn_ready = False
                                    self.current_turn = "human"  # Switch back to human
                        else:
                            # Automatic mode: AI plays continuously
                            current_time = pygame.time.get_ticks()
                            if current_time - self.last_ai_move_time >= self.ai_move_delay:
                                self.last_ai_move_time = current_time
                                self._make_ai_move()
                    
                    # Handle human player input
                    player_can_move = (not self.ai_mode) or (self.ai_mode and self.turn_by_turn and self.current_turn == "human")
                    
                    if action.type == pygame.MOUSEBUTTONDOWN and player_can_move:
                        mx, my = pygame.mouse.get_pos()
                        
                        # Check hint button click
                        if self.hint_button_rect and self.hint_button_rect.collidepoint(mx, my):
                            if self.hints_safe + self.hints_bomb > 0:  # Only open dropdown if hints available
                                self.hint_dropdown_open = not self.hint_dropdown_open
                            continue
                        
                        # Check hint dropdown clicks
                        if self.hint_dropdown_open:
                            if self.hint_safe_rect and self.hint_safe_rect.collidepoint(mx, my):
                                if self.hints_safe > 0:
                                    if self.grid.reveal_random_safe_cell():
                                        self.hints_safe -= 1
                                    self.hint_dropdown_open = False
                                continue
                            elif self.hint_bomb_rect and self.hint_bomb_rect.collidepoint(mx, my):
                                if self.hints_bomb > 0:
                                    if self.grid.reveal_random_bomb_cell():
                                        self.hints_bomb -= 1
                                    self.hint_dropdown_open = False
                                continue
                            else:
                                # Click outside dropdown, close it
                                self.hint_dropdown_open = False
                        
                        # Get grid coordinates from mouse position
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
                            # In turn-by-turn mode, switch to AI turn after flagging
                            if self.ai_mode and self.turn_by_turn:
                                self.current_turn = "ai"
                                self.ai_turn_ready = True
                                self.last_ai_move_time = pygame.time.get_ticks()
                            # do not continue to uncover on right-click
                            continue

                        # Left-click logic, but block if flagged
                        if action.button == 1:
                            if getattr(cell, "flagged", False):
                                # can't uncover a flagged cell
                                continue

                            # Store the clicked position for game over screen
                            self.last_clicked_row = row
                            self.last_clicked_col = col

                            if cell.type == "B": # is the clicked cell is the bomb then game over
                                self.state = "game-over"
                                self.game_over_sound.play()
                            else: # It is a safe cell, therefore we do the recursive dig function
                                self.grid.dig(row,col)
                                
                                # In turn-by-turn mode, switch to AI turn after human move
                                if self.ai_mode and self.turn_by_turn:
                                    self.current_turn = "ai"
                                    self.ai_turn_ready = True
                                    self.last_ai_move_time = pygame.time.get_ticks()
                            
                            # Check the win condition
                            if self.grid.check_win(): # If not a bomb, check if this was the winning move.
                                self.state = "game-win"
                                self.game_win_sound.play()

                # This is the game over logic
                elif self.state == "game-over":
                    self.grid.reveal_bombs(self.last_clicked_row, self.last_clicked_col) # Show/reveal all of the bombs on the grid
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
        # Reset hint counts
        self.hints_safe = 3
        self.hints_bomb = 2
        self.hint_dropdown_open = False
        # Reset AI solver
        self.ai_solver = None # Reset AI solver
        self.current_turn = "human" # Reset to human's turn
        self.ai_turn_ready = False # Reset AI turn flag
        
    def _make_ai_move(self):
        """
        Execute one AI move based on the current game state and AI difficulty.
        """
        # If bombs haven't been generated yet, make a random first move
        if not self.grid.bombs_generated:
            # Random first click for AI
            row, col = random.randint(0, ROWS - 1), random.randint(0, COLUMNS - 1)
            self.grid.generate_bombs(row, col)
            self.grid.generate_numbers()
            self.grid.display_board()
            self.grid.dig(row, col)
            
            # Check win condition after first move
            if self.grid.check_win():
                self.state = "game-win"
                self.game_win_sound.play()
            return
        
        # Get the next move from the AI solver
        move = self.ai_solver.get_move(self.grid)
        
        if move is None:
            # No valid moves available (shouldn't happen in normal gameplay)
            return
        
        action, row, col = move
        
        if action == "flag":
            # Place a flag
            self.grid.toggle_flag(row, col)
        elif action == "click":
            # Click on the cell
            cell = self.grid.grid_list[row][col]
            
            # Store the clicked position for game over screen
            self.last_clicked_row = row
            self.last_clicked_col = col
            
            if cell.type == "B":
                # AI clicked on a bomb - game over
                self.state = "game-over"
                self.game_over_sound.play()
            else:
                # Safe cell - dig it
                self.grid.dig(row, col)
                
                # Check win condition
                if self.grid.check_win():
                    self.state = "game-win"
                    self.game_win_sound.play()

