import pygame
from settings import *
from assets import *


class Game:
    def __init__(self):
        pygame.init()

        self.layout = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Minesweeper")
        self.timer = pygame.time.Clock()
        self.isGameActive = True
        self.grid = None
        self.gameover_click = False
        # self.grid.display_board()
        self.state = "front-page"
        self.bomb_amount = 10 # Default
        self.bomb_min = 10
        self.bomb_max = 20
        pygame.mixer.init()
        pygame.mixer.music.load('Assets/game-music.wav')
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
        self.game_over_sound = pygame.mixer.Sound("Assets/game-lose-music.wav") # Add game losing music
        self.game_win_sound = pygame.mixer.Sound("Assets/game-win-music.wav") # Add game winning music
        pygame.mixer.init()

    def front_page(self):
        self.layout.blit(background_img, (0, 0))
        title_font = pygame.font.SysFont("Verdana", 55, bold=True)
        front_page_title = title_font.render(TITLE, True, BLACK)
        title_pos = front_page_title.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        self.layout.blit(front_page_title, title_pos)

        # This is for the display of amount of bombs selected.
        bomb_selector_font = pygame.font.SysFont("Verdana",25, bold=True)
        bomb_selector_text = bomb_selector_font.render(f"Bombs: {self.bomb_amount}", True, BLACK)
        bomb_selector_pos = bomb_selector_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.layout.blit(bomb_selector_text, bomb_selector_pos)

        # This is the arrows for adding more/less bombs.
        left_arrow = pygame.Rect(bomb_selector_pos.left - 40, bomb_selector_pos.centery - 15, 30, 30)
        right_arrow = pygame.Rect(bomb_selector_pos.right + 10, bomb_selector_pos.centery - 15, 30, 30)
        pygame.draw.polygon(self.layout, LIGHTGREEN, [(left_arrow.right, left_arrow.top), (left_arrow.right, left_arrow.bottom), (left_arrow.left, left_arrow.centery)])
        pygame.draw.polygon(self.layout, LIGHTGREEN, [(right_arrow.left, right_arrow.top), (right_arrow.left, right_arrow.bottom), (right_arrow.right, right_arrow.centery)])

        # Play Game Button
        button_font = pygame.font.SysFont("Verdana", 30, bold=True)
        button_title = button_font.render("Play Game!", True, WHITE)
        button_pos = pygame.Rect(0, 0, 220, 60)
        button_pos.center = (WIDTH // 2, HEIGHT // 1.5)
        pygame.draw.rect(self.layout, LIGHTGREEN, button_pos, border_radius=15)
        self.layout.blit(button_title, button_title.get_rect(center=button_pos.center))

        return button_pos, left_arrow, right_arrow

    def draw_hud(self):
        if hasattr(self.grid, "flags_remaining"):
            hud_font = pygame.font.SysFont("Verdana", 16, bold=True)
            flags_text = hud_font.render(f"Flags Left: {self.grid.flags_remaining()}", True, WHITE)
            text_rect = flags_text.get_rect(center=((flags_text.get_width() // 2) + 25, PADDING // 2))
            self.layout.blit(flags_text, text_rect)

            hud_font = pygame.font.SysFont("Verdana", 24, bold=True)
            status_text = hud_font.render("Playing", True, WHITE)
            text_rect = status_text.get_rect(center=(self.layout.get_width() // 2, PADDING // 2))
            self.layout.blit(status_text, text_rect)

            hud_font = pygame.font.SysFont("Verdana", 16, bold=True)
            mines_text = hud_font.render(f"Mines Left: {self.grid.flags_remaining()}", True, WHITE)
            text_rect = mines_text.get_rect(center=(self.layout.get_width() - (mines_text.get_width() // 2) - 25, PADDING // 2))
            self.layout.blit(mines_text, text_rect)

    def draw_label(self):
        font = pygame.font.SysFont("Verdana", 15, bold=True)

        # --- Column labels (A-J) ---
        for col in range(COLUMNS):
            label = chr(ord('A') + col)
            text = font.render(label, True, WHITE)
            text_rect = text.get_rect(
                center=(PADDING + col * CELLSIZE + CELLSIZE // 2,  # X centered over cell
                        HEIGHT - PADDING // 2)                     # Bottom padding center
            )
            self.layout.blit(text, text_rect)

        # --- Row labels (1-10) ---
        for row in range(ROWS):
            label = str(row + 1)
            text = font.render(label, True, WHITE)
            text_rect = text.get_rect(
                center=(PADDING // 2,                               # Left padding center
                        PADDING + row * CELLSIZE + CELLSIZE // 2)  # Y centered to cell
            )
            self.layout.blit(text, text_rect)

    def play_game(self):
        while (self.isGameActive or self.state == "game-win"):
            self.timer.tick(60)
            for action in pygame.event.get():
                if action.type == pygame.QUIT:
                    self.isGameActive = False

                if self.state == "front-page":
                    self.front_page()
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
                    self.layout.fill(DARKGREEN)
                    self.draw_hud()
                    self.draw_label()
                    self.grid.draw(self.layout)

                    if action.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()
                        row, col = (my - PADDING) // CELLSIZE, (mx - PADDING) // CELLSIZE
                        if my < PADDING:
                            continue
                        cell = self.grid.grid_list[row][col]
                        
                        if self.grid.bombs_generated == False:
                            self.grid.generate_bombs(row,col)
                            self.grid.generate_numbers()
                            self.grid.display_board()

                        # ---right-click toggles flag added ---
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
                            result = self.grid.dig(row,col)
                            if not result:
                                self.game_over_sound.play()
                                self.state = "game-over"
                            is_winner = self.grid.check_win() # If not a bomb, check if this was the winning move.
                            if self.grid.check_win():  
                                self.game_win_sound.play()
                                self.state = "game-win"   
        
                        #if cell.type == "B":
                            #self.game_over_sound.play()
                            #self.state = "game-over"
                        #is_winner = self.grid.check_win() # If not a bomb, check if this was the winning move.
                        #if is_winner:
                            #self.game_win_sound.play()
                            #self.state = "game-win"
                elif self.state == "game-over":
                    self.layout.fill(DARKGREEN)
                    self.draw_hud()
                    self.draw_label()
                    self.grid.draw(self.layout)
                    self.grid.reveal_bombs()
                    retry = self.game_over_page()

                    if action.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if retry.collidepoint(mouse_pos):
                            self.grid = Grid(bomb_amount = self.bomb_amount)
                            self.state = "front-page"
                elif self.state == "game-win":
                    self.layout.fill(DARKGREEN)
                    self.draw_hud()
                    self.draw_label()
                    self.grid.draw(self.layout)
                    # self.grid.reveal_bombs()
                    retry = self.game_win_page()
                    if action.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if retry.collidepoint(mouse_pos):
                            self.grid = Grid(bomb_amount = self.bomb_amount)
                            self.state = "front-page"
            pygame.display.update()
        
        pygame.quit()

    def game_ended_page (self, text):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((100, 100, 100, 100))
        self.layout.blit(overlay, (0, 0))

        font = pygame.font.SysFont("Verdana", 55, bold=True)
        text = font.render(text, True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        self.layout.blit(text, text_rect)

        retry_image = pygame.image.load("Assets/Retry.png").convert_alpha()
        retry_image_scaled = pygame.transform.scale(retry_image, (60, 60))
        retry_circle_layer = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(retry_circle_layer, (255, 255, 255, 255), (30, 30), 30)
        retry_circle_image = retry_image_scaled.copy()
        retry_circle_image.blit(retry_circle_layer, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

        retry_rect = retry_circle_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        self.layout.blit(retry_circle_image, retry_rect)

        return retry_rect
    
    def game_over_page(self):
        return self.game_ended_page("Game Over!")

    def game_win_page(self):
        return self.game_ended_page("YOU WIN!")