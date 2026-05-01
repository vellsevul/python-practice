# main.py
import pygame
import sys
import json
import os
from config import *
from game import GameState
from db import Database
from game import GameState, Snake, Food, PoisonFood, PowerUp, Obstacles
class Button:
    """Simple button class for UI"""
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.SysFont("Verdana", FONT_SIZE_MEDIUM)
    
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 3)
        
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

class Settings:
    """Manage game settings from JSON file"""
    def __init__(self, filename='settings.json'):
        self.filename = filename
        self.defaults = {
            'snake_color': [0, 255, 0],
            'grid_overlay': True,
            'sound': True
        }
        self.load()
    
    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
                for key, value in self.defaults.items():
                    setattr(self, key, data.get(key, value))
        else:
            for key, value in self.defaults.items():
                setattr(self, key, value)
            self.save()
    
    def save(self):
        with open(self.filename, 'w') as f:
            json.dump({
                'snake_color': self.snake_color,
                'grid_overlay': self.grid_overlay,
                'sound': self.sound
            }, f, indent=4)
    
    def __getitem__(self, key):
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        setattr(self, key, value)

class SnakeGame:
    """Main game application with screens"""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game - TSIS 4")
        self.clock = pygame.time.Clock()
        
        # Initialize database and settings
        self.db = Database()
        self.settings = Settings()
        
        # Game state
        self.username = ""
        self.username_entered = False
        self.game_state = None
        
        # Current screen
        self.current_screen = "menu"  # menu, game, game_over, leaderboard, settings
        
        # Fonts
        self.font_small = pygame.font.SysFont("Verdana", FONT_SIZE)
        self.font_medium = pygame.font.SysFont("Verdana", FONT_SIZE_MEDIUM)
        self.font_large = pygame.font.SysFont("Verdana", FONT_SIZE_LARGE)
        
        # Colors
        self.MENU_BG = (20, 20, 40)
        self.BUTTON_COLOR = (0, 100, 0)
        self.BUTTON_HOVER = (0, 150, 0)
    
    def draw_text_centered(self, text, y, font=None, color=WHITE):
        """Draw centered text"""
        if font is None:
            font = self.font_medium
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(WIDTH // 2, y))
        self.screen.blit(text_surf, text_rect)
    
    def username_input_screen(self):
        """Get username from player"""
        input_active = True
        username = ""
        
        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and username.strip():
                        self.username = username.strip()
                        self.username_entered = True
                        return True
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        if len(username) < 20 and event.unicode.isalnum():
                            username += event.unicode
            
            self.screen.fill(self.MENU_BG)
            
            # Title
            title_font = pygame.font.SysFont("Verdana", 50)
            self.draw_text_centered("SNAKE GAME", 100, title_font, GREEN)
            
            # Instruction
            self.draw_text_centered("Enter your username:", 200)
            
            # Input field
            input_rect = pygame.Rect(WIDTH//2 - 150, 280, 300, 50)
            pygame.draw.rect(self.screen, WHITE, input_rect, 2)
            text_surf = self.font_medium.render(username, True, WHITE)
            text_rect = text_surf.get_rect(center=input_rect.center)
            self.screen.blit(text_surf, text_rect)
            
            # Hint
            self.draw_text_centered("Press ENTER to continue", 380, self.font_small, (150, 150, 150))
            
            pygame.display.update()
            self.clock.tick(30)
        return True
    
    def menu_screen(self):
        """Main menu screen"""
        buttons = [
            Button(WIDTH//2 - 100, 200, 200, 50, "PLAY", 
                   self.BUTTON_COLOR, self.BUTTON_HOVER),
            Button(WIDTH//2 - 100, 280, 200, 50, "LEADERBOARD",
                   self.BUTTON_COLOR, self.BUTTON_HOVER),
            Button(WIDTH//2 - 100, 360, 200, 50, "SETTINGS",
                   self.BUTTON_COLOR, self.BUTTON_HOVER),
            Button(WIDTH//2 - 100, 440, 200, 50, "QUIT",
                   self.BUTTON_COLOR, self.BUTTON_HOVER)
        ]
        
        while self.current_screen == "menu":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
                for button in buttons:
                    if button.is_clicked(event):
                        if button.text == "PLAY":
                            self.game_state = GameState(self.db, self.username, self.settings)
                            self.current_screen = "game"
                            return True
                        elif button.text == "LEADERBOARD":
                            self.current_screen = "leaderboard"
                        elif button.text == "SETTINGS":
                            self.current_screen = "settings"
                        elif button.text == "QUIT":
                            return False
            
            self.screen.fill(self.MENU_BG)
            
            # Title
            title_font = pygame.font.SysFont("Verdana", 60)
            self.draw_text_centered(f"SNAKE GAME", 100, title_font, GREEN)
            self.draw_text_centered(f"Logged in as: {self.username}", 160, self.font_small, (150, 150, 150))
            
            for button in buttons:
                button.draw(self.screen)
            
            pygame.display.update()
            self.clock.tick(60)
        
        return True
    
    def game_screen(self):
        """Main gameplay screen"""
        last_move_time = pygame.time.get_ticks()
        
        while self.current_screen == "game" and not self.game_state.game_over:
            current_time = pygame.time.get_ticks()
            
            # Handle movement speed
            if current_time - last_move_time > 1000 // self.game_state.snake.speed:
                self.game_state.update()
                last_move_time = current_time
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                        self.game_state.snake.change_direction(event.key)
                    elif event.key == pygame.K_ESCAPE:
                        self.current_screen = "menu"
                        return True
            
            # Draw game
            self.screen.fill(BLACK)
            self.game_state.draw(self.screen)
            pygame.display.update()
            self.clock.tick(60)
        
        # Game over - save to database and go to game over screen
        if self.game_state.game_over:
            self.db.save_game_result(self.username, self.game_state.score, self.game_state.level)
            self.current_screen = "game_over"
        
        return True
    
    def game_over_screen(self):
        """Game over screen with stats"""
        best_score = self.db.get_personal_best(self.username)
        
        buttons = [
            Button(WIDTH//2 - 120, 400, 200, 50, "RETRY",
                   self.BUTTON_COLOR, self.BUTTON_HOVER),
            Button(WIDTH//2 + 20, 400, 200, 50, "MENU",
                   self.BUTTON_COLOR, self.BUTTON_HOVER)
        ]
        
        while self.current_screen == "game_over":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
                for button in buttons:
                    if button.is_clicked(event):
                        if button.text == "RETRY":
                            self.game_state = GameState(self.db, self.username, self.settings)
                            self.current_screen = "game"
                            return True
                        elif button.text == "MENU":
                            self.current_screen = "menu"
                            return True
            
            self.screen.fill(self.MENU_BG)
            
            # Game over title
            self.draw_text_centered("GAME OVER", 120, self.font_large, RED)
            
            # Stats
            self.draw_text_centered(f"Score: {self.game_state.score}", 220)
            self.draw_text_centered(f"Level: {self.game_state.level}", 270)
            self.draw_text_centered(f"Personal Best: {best_score}", 320)
            
            for button in buttons:
                button.draw(self.screen)
            
            pygame.display.update()
            self.clock.tick(60)
        
        return True
    
    def leaderboard_screen(self):
        """Display top scores from database"""
        leaders = self.db.get_leaderboard(10)
        
        back_button = Button(WIDTH//2 - 100, HEIGHT - 80, 200, 50, "BACK",
                            self.BUTTON_COLOR, self.BUTTON_HOVER)
        
        while self.current_screen == "leaderboard":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if back_button.is_clicked(event):
                    self.current_screen = "menu"
                    return True
            
            self.screen.fill(self.MENU_BG)
            
            # Title
            title_font = pygame.font.SysFont("Verdana", 45)
            self.draw_text_centered("TOP 10 SCORES", 60, title_font, GOLD)
            
            # Column headers
            headers = ["RANK", "USERNAME", "SCORE", "LEVEL", "DATE"]
            header_x = [50, 150, 400, 550, 650]
            for i, header in enumerate(headers):
                text = self.font_small.render(header, True, WHITE)
                self.screen.blit(text, (header_x[i], 120))
            
            # Draw line
            pygame.draw.line(self.screen, WHITE, (30, 150), (WIDTH - 30, 150), 2)
            
            # Display top scores
            y = 180
            for idx, (username, score, level, played_at) in enumerate(leaders, 1):
                color = GOLD if idx == 1 else (200, 200, 200) if idx == 2 else (180, 120, 80) if idx == 3 else WHITE
                
                rank_text = self.font_small.render(str(idx), True, color)
                name_text = self.font_small.render(username[:15], True, color)
                score_text = self.font_small.render(str(score), True, color)
                level_text = self.font_small.render(str(level), True, color)
                date_text = self.font_small.render(played_at.strftime("%Y-%m-%d"), True, (150, 150, 150))
                
                self.screen.blit(rank_text, (50, y))
                self.screen.blit(name_text, (150, y))
                self.screen.blit(score_text, (420, y))
                self.screen.blit(level_text, (550, y))
                self.screen.blit(date_text, (650, y))
                
                y += 35
                if y > HEIGHT - 120:
                    break
            
            back_button.draw(self.screen)
            
            pygame.display.update()
            self.clock.tick(60)
        
        return True
    
    def settings_screen(self):
        """Settings screen with options"""
        color_options = ['GREEN', 'RED', 'BLUE', 'ORANGE', 'PURPLE']
        color_values = {
            'GREEN': [0, 255, 0],
            'RED': [255, 0, 0],
            'BLUE': [0, 0, 255],
            'ORANGE': [255, 165, 0],
            'PURPLE': [128, 0, 128]
        }
        color_index = list(color_values.values()).index(self.settings.snake_color)
        
        grid_options = ['ON', 'OFF']
        grid_index = 0 if self.settings.grid_overlay else 1
        
        sound_options = ['ON', 'OFF']
        sound_index = 0 if self.settings.sound else 1
        
        back_button = Button(WIDTH//2 - 100, HEIGHT - 80, 200, 50, "SAVE & BACK",
                            self.BUTTON_COLOR, self.BUTTON_HOVER)
        
        while self.current_screen == "settings":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]:
                            pass  # For color navigation
                    if event.key == pygame.K_RIGHT:
                        pass
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Check color button clicks
                    if WIDTH//2 - 50 < event.pos[0] < WIDTH//2 + 50:
                        if 250 < event.pos[1] < 300:
                            color_index = (color_index + 1) % len(color_options)
                            self.settings.snake_color = color_values[color_options[color_index]]
                        elif 350 < event.pos[1] < 400:
                            grid_index = (grid_index + 1) % 2
                            self.settings.grid_overlay = (grid_index == 0)
                        elif 450 < event.pos[1] < 500:
                            sound_index = (sound_index + 1) % 2
                            self.settings.sound = (sound_index == 0)
                
                if back_button.is_clicked(event):
                    self.settings.save()
                    self.current_screen = "menu"
                    return True
            
            self.screen.fill(self.MENU_BG)
            
            # Title
            self.draw_text_centered("SETTINGS", 80, self.font_large, GREEN)
            
            # Snake Color setting
            self.draw_text_centered("SNAKE COLOR:", 250, self.font_medium)
            color_rect = pygame.Rect(WIDTH//2 - 50, 260, 100, 40)
            pygame.draw.rect(self.screen, self.settings.snake_color, color_rect)
            pygame.draw.rect(self.screen, WHITE, color_rect, 2)
            color_text = self.font_small.render(color_options[color_index], True, WHITE)
            color_text_rect = color_text.get_rect(center=color_rect.center)
            self.screen.blit(color_text, color_text_rect)
            self.draw_text_centered("(Click to change)", 310, self.font_small, (150, 150, 150))
            
            # Grid setting
            self.draw_text_centered("GRID OVERLAY:", 350, self.font_medium)
            grid_rect = pygame.Rect(WIDTH//2 - 50, 360, 100, 40)
            pygame.draw.rect(self.screen, WHITE, grid_rect, 2)
            grid_text = self.font_small.render(grid_options[grid_index], True, WHITE)
            grid_text_rect = grid_text.get_rect(center=grid_rect.center)
            self.screen.blit(grid_text, grid_text_rect)
            
            # Sound setting
            self.draw_text_centered("SOUND:", 450, self.font_medium)
            sound_rect = pygame.Rect(WIDTH//2 - 50, 460, 100, 40)
            pygame.draw.rect(self.screen, WHITE, sound_rect, 2)
            sound_text = self.font_small.render(sound_options[sound_index], True, WHITE)
            sound_text_rect = sound_text.get_rect(center=sound_rect.center)
            self.screen.blit(sound_text, sound_text_rect)
            
            back_button.draw(self.screen)
            
            pygame.display.update()
            self.clock.tick(60)
        
        return True
    
    def run(self):
        """Main game loop"""
        # Get username first
        if not self.username_entered:
            if not self.username_input_screen():
                return
        
        running = True
        while running:
            if self.current_screen == "menu":
                running = self.menu_screen()
            elif self.current_screen == "game":
                running = self.game_screen()
            elif self.current_screen == "game_over":
                running = self.game_over_screen()
            elif self.current_screen == "leaderboard":
                running = self.leaderboard_screen()
            elif self.current_screen == "settings":
                running = self.settings_screen()
        
        self.db.close()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()