import pygame
from racer import WIDTH, HEIGHT

BG_COLOR = (25, 25, 35)

def draw_btn(screen, text, x, y, w, h, color=None):
    m_pos = pygame.mouse.get_pos()
    rect = pygame.Rect(x, y, w, h)
    hover = rect.collidepoint(m_pos)
    btn_color = color if color else (80, 80, 80) if hover else (50, 50, 50)
    pygame.draw.rect(screen, btn_color, rect, border_radius=10)
    pygame.draw.rect(screen, (200, 200, 200), rect, 2, border_radius=10)
    f = pygame.font.SysFont("Verdana", 20, bold=True)
    t_surf = f.render(text, True, (255, 255, 255))
    screen.blit(t_surf, t_surf.get_rect(center=rect.center))
    return hover and pygame.mouse.get_pressed()[0]

class MainMenu:
    def __init__(self, screen): 
        self.screen = screen
        self.title_font = pygame.font.SysFont("Verdana", 48, bold=True)
        
    def run(self):
        self.screen.fill(BG_COLOR)
        
        # Title
        title = self.title_font.render("TSIS 3 RACER", True, (255, 215, 0))
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))
        
        bw, bh = 200, 50
        bx = WIDTH // 2 - bw // 2
        
        if draw_btn(self.screen, "START RACE", bx, 200, bw, bh): return "play"
        if draw_btn(self.screen, "LEADERBOARD", bx, 270, bw, bh): return "leaderboard"
        if draw_btn(self.screen, "SETTINGS", bx, 340, bw, bh): return "settings"
        if draw_btn(self.screen, "QUIT", bx, 410, bw, bh): 
            pygame.quit()
            exit()
        return "menu"

class UsernameScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Verdana", 24)
        self.input_font = pygame.font.SysFont("Verdana", 32)
        self.username = ""
        self.active = True
        
    def run(self):
        self.username = ""
        input_rect = pygame.Rect(WIDTH//2 - 150, 300, 300, 50)
        
        while self.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.username:
                        return self.username or "Player"
                    elif event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    else:
                        if len(self.username) < 15 and event.unicode.isprintable():
                            self.username += event.unicode
            
            self.screen.fill(BG_COLOR)
            
            title = self.font.render("ENTER YOUR NAME", True, (255, 215, 0))
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 200))
            
            pygame.draw.rect(self.screen, (100, 100, 100), input_rect, 2)
            name_text = self.input_font.render(self.username or "_", True, (255, 255, 255))
            self.screen.blit(name_text, (input_rect.x + 10, input_rect.y + 10))
            
            instruction = self.font.render("Press ENTER to continue", True, (150, 150, 150))
            self.screen.blit(instruction, (WIDTH//2 - instruction.get_width()//2, 400))
            
            pygame.display.flip()
        
        return "Player"

class GameOverScreen:
    def __init__(self, screen): 
        self.screen = screen
        self.font = pygame.font.SysFont("Verdana", 36, bold=True)
        
    def run(self, score, distance):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0,0))

        title = self.font.render("GAME OVER", True, (255, 50, 50))
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        
        score_font = pygame.font.SysFont("Verdana", 24)
        score_txt = score_font.render(f"Final Score: {score}", True, (255, 215, 0))
        dist_txt = score_font.render(f"Distance: {distance}m", True, (255, 255, 255))
        
        self.screen.blit(score_txt, (WIDTH//2 - score_txt.get_width()//2, 200))
        self.screen.blit(dist_txt, (WIDTH//2 - dist_txt.get_width()//2, 240))
        
        bw, bh = 200, 50
        bx = WIDTH // 2 - bw // 2
        if draw_btn(self.screen, "RETRY", bx, 350, bw, bh): return "retry"
        if draw_btn(self.screen, "MAIN MENU", bx, 420, bw, bh): return "menu"
        return "gameover"

class SettingsScreen:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.options = ["difficulty", "car_color", "sound"]
        self.selected = 0
        self.car_colors = ["red", "blue", "green"]
        
    def run(self):
        self.screen.fill(BG_COLOR)
        
        title = pygame.font.SysFont("Verdana", 36, True).render("SETTINGS", True, (255, 215, 0))
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
        
        # Difficulty
        diff = self.settings.get("difficulty", 1)
        diff_names = {1: "Easy", 2: "Medium", 3: "Hard"}
        diff_txt = pygame.font.SysFont("Verdana", 24).render(f"Difficulty: {diff_names[diff]}", True, (255, 255, 255))
        self.screen.blit(diff_txt, (80, 150))
        
        # Car Color
        color = self.settings.get("car_color", "red")
        color_txt = pygame.font.SysFont("Verdana", 24).render(f"Car Color: {color.upper()}", True, (255, 255, 255))
        self.screen.blit(color_txt, (80, 220))
        
        # Sound
        sound = self.settings.get("sound", True)
        sound_txt = pygame.font.SysFont("Verdana", 24).render(f"Sound: {'ON' if sound else 'OFF'}", True, (255, 255, 255))
        self.screen.blit(sound_txt, (80, 290))
        
        # Buttons
        bw, bh = 150, 40
        if draw_btn(self.screen, "Change Difficulty", 300, 145, bw, bh):
            self.settings["difficulty"] = self.settings.get("difficulty", 1) % 3 + 1
        if draw_btn(self.screen, "Change Color", 300, 215, bw, bh):
            colors = ["red", "blue", "green"]
            current = colors.index(self.settings.get("car_color", "red"))
            self.settings["car_color"] = colors[(current + 1) % 3]
        if draw_btn(self.screen, "Toggle Sound", 300, 285, bw, bh):
            self.settings["sound"] = not self.settings.get("sound", True)
        
        # Save and Back buttons
        bw, bh = 200, 50
        bx = WIDTH // 2 - bw // 2
        if draw_btn(self.screen, "SAVE", bx, 400, bw, bh):
            return "menu"
        if draw_btn(self.screen, "BACK", bx, 470, bw, bh):
            return "menu"
        return "settings"

class LeaderboardScreen:
    def __init__(self, screen, data):
        self.screen = screen
        self.data = data
        self.font = pygame.font.SysFont("Verdana", 18)
        self.title_font = pygame.font.SysFont("Verdana", 32, bold=True)
        
    def run(self):
        self.screen.fill(BG_COLOR)
        
        title = self.title_font.render("TOP 10 RACERS", True, (255, 215, 0))
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))
        
        y = 100
        headers = self.font.render("RANK  NAME                 SCORE    DISTANCE", True, (200, 200, 200))
        self.screen.blit(headers, (40, y))
        y += 30
        
        for i, entry in enumerate(self.data[:10]):
            color = (255, 215, 0) if i == 0 else (200, 200, 200)
            rank = f"{i+1}."
            name = entry.get("name", "Unknown")[:15]
            score = str(entry.get("score", 0))
            distance = f"{entry.get('distance', 0)}m"
            
            text = f"{rank:<4} {name:<16} {score:>8}   {distance:>8}"
            txt_surf = self.font.render(text, True, color)
            self.screen.blit(txt_surf, (40, y))
            y += 30
            
            if y > 500:
                break
        
        if not self.data:
            empty_txt = self.font.render("No scores yet! Play the game!", True, (150, 150, 150))
            self.screen.blit(empty_txt, (WIDTH//2 - empty_txt.get_width()//2, 250))
        
        bw, bh = 200, 50
        if draw_btn(self.screen, "BACK", WIDTH // 2 - bw // 2, 520, bw, bh):
            return "menu"
        return "leaderboard"
