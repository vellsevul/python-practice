import pygame
from racer import Game
from ui import MainMenu, GameOverScreen, LeaderboardScreen, SettingsScreen
from persistence import load_settings, save_settings, load_leaderboard, save_leaderboard

pygame.init()
WIDTH, HEIGHT = 480, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer TSIS 3")
clock = pygame.time.Clock()

settings = load_settings()
leaderboard_data = load_leaderboard()

menu = MainMenu(screen)
gameover_scr = GameOverScreen(screen)
settings_scr = SettingsScreen(screen, settings)
lb_scr = LeaderboardScreen(screen, leaderboard_data)

game = Game(screen, settings)
state = "menu"
score_saved = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); exit()

    if state == "menu":
        score_saved = False
        state = menu.run()
        if state == "play": game = Game(screen, settings)

    elif state == "play":
        state = game.run()

    elif state == "gameover":
        if not score_saved:
            if game.score > 0:
                leaderboard_data.append({"name": "Player", "score": game.score, "distance": game.distance})
                leaderboard_data = sorted(leaderboard_data, key=lambda x: x["score"], reverse=True)[:10]
                save_leaderboard(leaderboard_data)
                lb_scr.data = leaderboard_data
            score_saved = True
        
        res = gameover_scr.run(game.score, game.distance)
        if res == "retry":
            game = Game(screen, settings)
            state = "play"
        elif res == "menu": state = "menu"

    elif state == "leaderboard": state = lb_scr.run()
    elif state == "settings":
        res = settings_scr.run()
        if res == "save_settings":
            save_settings(settings)
            state = "settings"
        else: state = res

    pygame.display.flip()
    clock.tick(60)