import pygame
from racer import WIDTH, HEIGHT

BG_COLOR = (25, 25, 35)

def draw_btn(screen, text, x, y, w, h):
    m_pos = pygame.mouse.get_pos()
    rect = pygame.Rect(x, y, w, h)
    hover = rect.collidepoint(m_pos)
    pygame.draw.rect(screen, (80, 80, 80) if hover else (50, 50, 50), rect, border_radius=10)
    pygame.draw.rect(screen, (200, 200, 200), rect, 2, border_radius=10)
    f = pygame.font.SysFont("Verdana", 20, bold=True)
    t_surf = f.render(text, True, (255, 255, 255))
    screen.blit(t_surf, t_surf.get_rect(center=rect.center))
    return hover and pygame.mouse.get_pressed()[0]

class MainMenu:
    def __init__(self, screen): self.screen = screen
    def run(self):
        self.screen.fill(BG_COLOR)
        bw, bh = 200, 50
        bx = WIDTH // 2 - bw // 2
        if draw_btn(self.screen, "START RACE", bx, 200, bw, bh): return "play"
        if draw_btn(self.screen, "LEADERBOARD", bx, 270, bw, bh): return "leaderboard"
        if draw_btn(self.screen, "SETTINGS", bx, 340, bw, bh): return "settings"
        return "menu"

class GameOverScreen:
    def __init__(self, screen): self.screen = screen
    def run(self, s, d):
        # Затемняем фон
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(160)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0,0))

        f = pygame.font.SysFont("Verdana", 40, True)
        txt = f.render("CRASHED!", True, (255, 50, 50))
        self.screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, 150))
        
        bw, bh = 200, 50
        bx = WIDTH // 2 - bw // 2
        if draw_btn(self.screen, "RETRY", bx, 300, bw, bh): return "retry"
        if draw_btn(self.screen, "MENU", bx, 370, bw, bh): return "menu"
        return "gameover"

class SettingsScreen:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
    def run(self):
        self.screen.fill(BG_COLOR)
        d = self.settings.get("difficulty", 1)
        txt = pygame.font.SysFont("Verdana", 25, True).render(f"Difficulty: {d}", True, (255,255,255))
        self.screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, 150))
        bw, bh = 200, 50
        bx = WIDTH // 2 - bw // 2
        if draw_btn(self.screen, "CHANGE", bx, 220, bw, bh):
            pygame.time.delay(150)
            self.settings["difficulty"] = d + 1 if d < 3 else 1
            return "save_settings"
        if draw_btn(self.screen, "BACK", bx, 450, bw, bh): return "menu"
        return "settings"

class LeaderboardScreen:
    def __init__(self, screen, data):
        self.screen = screen
        self.data = data
    def run(self):
        self.screen.fill(BG_COLOR)
        y = 100
        for i, r in enumerate(self.data[:10]):
            txt = pygame.font.SysFont("Verdana", 18).render(f"{i+1}. Score: {r['score']} | {r['distance']}m", True, (200,200,200))
            self.screen.blit(txt, (80, y))
            y += 35
        bw, bh = 200, 50
        if draw_btn(self.screen, "BACK", WIDTH // 2 - bw // 2, 500, bw, bh): return "menu"
        return "leaderboard"