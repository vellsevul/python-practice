import pygame
import random

WIDTH, HEIGHT = 480, 600

class Player(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.original_image = img
        self.image = img
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 70))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 7
        self.lane = 2
        self.shield_active = False
        self.invincible_timer = 0

    def move(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < WIDTH:
            self.rect.x += self.speed
        
        lane_width = WIDTH // 3
        self.lane = min(2, max(0, self.rect.centerx // lane_width))
        
        if self.shield_active:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.shield_active = False
                self.image = self.original_image
            else:
                if pygame.time.get_ticks() % 200 < 100:
                    self.image.set_alpha(180)
                else:
                    self.image.set_alpha(255)
        else:
            self.image.set_alpha(255)
            self.image = self.original_image

    def activate_shield(self, duration=300):
        self.shield_active = True
        self.invincible_timer = duration

class Enemy(pygame.sprite.Sprite):
    def __init__(self, img, base_speed, lane=None):
        super().__init__()
        self.image = img
        self.mask = pygame.mask.from_surface(self.image)
        self.lane = lane if lane is not None else random.randint(0, 2)
        lane_width = WIDTH // 3
        self.rect = self.image.get_rect()
        self.rect.centerx = lane_width // 2 + self.lane * lane_width
        self.rect.y = random.randint(-600, -100)
        self.speed = base_speed + random.uniform(0, 2)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, obstacle_type):
        super().__init__()
        self.type = obstacle_type
        self.rect = pygame.Rect(x, y, 40, 40)
        self.mask = pygame.mask.Mask((40, 40))
        self.mask.fill()
        self.speed = 5
        
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        if self.type == 'oil':
            pygame.draw.circle(self.image, (50, 50, 50), (20, 20), 18)
            pygame.draw.circle(self.image, (80, 80, 80), (20, 20), 15)
        elif self.type == 'pothole':
            pygame.draw.rect(self.image, (30, 30, 30), (10, 10, 20, 20))
            pygame.draw.rect(self.image, (20, 20, 20), (12, 12, 16, 16))
        else:  # barrier
            pygame.draw.rect(self.image, (150, 100, 50), (5, 10, 30, 20))
            pygame.draw.line(self.image, (200, 150, 50), (5, 20), (35, 20), 3)
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, power_type):
        super().__init__()
        self.type = power_type
        self.rect = pygame.Rect(x, y, 30, 30)
        self.mask = pygame.mask.Mask((30, 30))
        self.mask.fill()
        self.speed = 5
        self.lifetime = 300
        self.age = 0
        
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        if self.type == 'nitro':
            pygame.draw.circle(self.image, (0, 255, 255), (15, 15), 12)
            pygame.draw.circle(self.image, (100, 255, 255), (15, 15), 8)
        elif self.type == 'shield':
            pygame.draw.circle(self.image, (0, 255, 0), (15, 15), 12)
            pygame.draw.circle(self.image, (100, 255, 100), (15, 15), 8)
        else:
            pygame.draw.circle(self.image, (255, 255, 0), (15, 15), 12)
            pygame.draw.circle(self.image, (255, 255, 150), (15, 15), 8)
    
    def update(self):
        self.rect.y += self.speed
        self.age += 1
        if self.rect.top > HEIGHT or self.age > self.lifetime:
            self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.raw_image = img
        self.reset()
        self.speed = 5

    def reset(self):
        self.weight = random.choice([1, 5, 10])
        size = 25 + (self.weight // 2)
        self.image = pygame.transform.scale(self.raw_image, (size, size))
        lane_width = WIDTH // 3
        lane = random.randint(0, 2)
        self.rect = self.image.get_rect()
        self.rect.centerx = lane_width // 2 + lane * lane_width
        self.rect.y = random.randint(-500, -50)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.reset()

class DynamicEvent:
    def __init__(self):
        self.active = False
        self.type = None
        self.timer = 0
        
    def spawn(self, event_type, lane, duration=120):
        self.active = True
        self.type = event_type
        self.lane = lane
        self.duration = duration
        self.timer = duration
        lane_width = WIDTH // 3
        self.x = lane_width // 2 + lane * lane_width - 25
        
    def update(self):
        if self.active:
            self.timer -= 1
            if self.timer <= 0:
                self.active = False
            return True
        return False

class Game:
    def __init__(self, screen, settings, username="Player"):
        self.screen = screen
        self.diff = settings.get("difficulty", 1)
        self.username = username
        self.car_color = settings.get("car_color", "red")
        
        self.load_assets()
        
        self.player = Player(self.player_img)
        self.enemies = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.coins = pygame.sprite.Group([Coin(self.coin_img) for _ in range(5)])
        
        self.score = 0
        self.coins_collected = 0
        self.distance = 0
        self.bg_y1 = 0
        self.bg_y2 = -HEIGHT
        self.font = pygame.font.SysFont("Verdana", 20, bold=True)
        self.small_font = pygame.font.SysFont("Verdana", 16)
        
        self.active_powerup = None
        self.powerup_timer = 0
        self.nitro_speed = 1.0
        self.base_speed = 3 + self.diff
        self.spawn_timer = 0
        self.event_timer = 0
        self.dynamic_event = DynamicEvent()
        
        for _ in range(2 + self.diff):
            self.spawn_enemy()
        
        self.game_over = False
        self.game_over_reason = ""

    def load_assets(self):
        CAR_W, CAR_H = 45, 90
        
        try:
            if self.car_color == "red":
                p_orig = pygame.image.load("player.png").convert_alpha()
            else:
                p_orig = pygame.image.load("player.png").convert_alpha()
            self.player_img = pygame.transform.scale(p_orig, (CAR_W, CAR_H))
            
            self.enemy_img = pygame.transform.scale(
                pygame.image.load("enemy.png").convert_alpha(), 
                (CAR_W, CAR_H)
            )
            self.coin_img = pygame.image.load("coin.png").convert_alpha()
            self.road_img = pygame.transform.scale(
                pygame.image.load("road.png").convert(), 
                (WIDTH, HEIGHT)
            )
        except Exception as e:
            print(f"Error loading assets: {e}")
            self.player_img = pygame.Surface((CAR_W, CAR_H))
            self.player_img.fill((0, 255, 0))
            self.enemy_img = pygame.Surface((CAR_W, CAR_H))
            self.enemy_img.fill((255, 0, 0))
            self.coin_img = pygame.Surface((30, 30))
            self.coin_img.fill((255, 215, 0))
            self.road_img = pygame.Surface((WIDTH, HEIGHT))
            self.road_img.fill((50, 50, 50))

    def spawn_enemy(self):
        enemy = Enemy(self.enemy_img, self.base_speed)
        self.enemies.add(enemy)

    def spawn_obstacle(self):
        if random.random() < 0.3 + self.diff * 0.05:
            lane = random.randint(0, 2)
            lane_width = WIDTH // 3
            x = lane_width // 2 + lane * lane_width - 20
            obstacle_type = random.choice(['oil', 'pothole', 'barrier'])
            obstacle = Obstacle(x, -50, obstacle_type)
            self.obstacles.add(obstacle)

    def spawn_powerup(self):
        if random.random() < 0.05 and len(self.powerups) < 2:
            lane = random.randint(0, 2)
            lane_width = WIDTH // 3
            x = lane_width // 2 + lane * lane_width - 15
            power_type = random.choice(['nitro', 'shield', 'repair'])
            powerup = PowerUp(x, -50, power_type)
            self.powerups.add(powerup)

    def check_collisions(self):
        # 1. Столкновение с врагом (без щита)
        enemy_hits = pygame.sprite.spritecollide(self.player, self.enemies, False, pygame.sprite.collide_mask)
        if enemy_hits and not self.player.shield_active:
            self.game_over_reason = "CRASHED INTO ENEMY CAR!"
            return True
        elif enemy_hits and self.player.shield_active:
            enemy_hits[0].kill()
        
        # 2. Столкновение с барьером
        for obstacle in self.obstacles:
            if obstacle.type == 'barrier' and pygame.sprite.collide_mask(self.player, obstacle):
                self.game_over_reason = "HIT A BARRIER!"
                return True
        
        # Остальные препятствия
        for obstacle in pygame.sprite.spritecollide(self.player, self.obstacles, False, pygame.sprite.collide_mask):
            if obstacle.type == 'oil':
                self.nitro_speed = max(0.3, self.nitro_speed * 0.7)
                obstacle.kill()
            elif obstacle.type == 'pothole':
                self.score = max(0, self.score - 5)
                obstacle.kill()
        
        # Power-up collection
        for powerup in pygame.sprite.spritecollide(self.player, self.powerups, False, pygame.sprite.collide_mask):
            if powerup.type == 'nitro':
                self.active_powerup = 'Nitro'
                self.powerup_timer = 300
                self.nitro_speed = 2.0
            elif powerup.type == 'shield':
                self.player.activate_shield(300)
                self.active_powerup = 'Shield'
                self.powerup_timer = 300
            elif powerup.type == 'repair':
                self.score += 50
                self.active_powerup = 'Repair'
                self.powerup_timer = 30
            powerup.kill()
        
        # Update powerup timer
        if self.powerup_timer > 0:
            self.powerup_timer -= 1
            if self.powerup_timer <= 0:
                if self.active_powerup == 'Nitro':
                    self.nitro_speed = 1.0
                self.active_powerup = None
        
        return False

    def update_background(self):
        scroll_speed = int(self.base_speed * self.nitro_speed)
        
        self.bg_y1 += scroll_speed
        self.bg_y2 += scroll_speed
        
        if self.bg_y1 >= HEIGHT:
            self.bg_y1 = -HEIGHT
        if self.bg_y2 >= HEIGHT:
            self.bg_y2 = -HEIGHT
        
        self.screen.blit(self.road_img, (0, self.bg_y1))
        self.screen.blit(self.road_img, (0, self.bg_y2))

    def run(self):
        if self.game_over:
            return "gameover"
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.active_powerup == 'Nitro' and self.powerup_timer > 0:
            self.nitro_speed = 2.5
        elif self.active_powerup != 'Nitro':
            self.nitro_speed = 1.0
        
        self.player.move()
        
        current_speed = self.base_speed * self.nitro_speed
        self.distance += int(current_speed)
        
        # Начисляем очки за дистанцию (каждые 100 метров)
        if self.distance % 100 == 0 and self.distance > 0:
            self.score += 10
        
        # Spawn objects
        self.spawn_timer += 1
        spawn_delay = max(30, 50 - self.diff * 5)
        if self.spawn_timer > spawn_delay:
            if len(self.enemies) < 4 + self.diff:
                self.spawn_enemy()
            self.spawn_obstacle()
            self.spawn_powerup()
            self.spawn_timer = random.randint(0, 20)
        
        # Update speeds
        for enemy in self.enemies:
            enemy.speed = self.base_speed * self.nitro_speed + random.uniform(0, 2)
        
        self.enemies.update()
        self.obstacles.update()
        self.powerups.update()
        self.coins.update()
        
        # Check collisions (Game Over)
        if self.check_collisions():
            self.game_over = True
            return "gameover"
        
        # Collect coins
        for coin in pygame.sprite.spritecollide(self.player, self.coins, False, pygame.sprite.collide_mask):
            self.score += coin.weight
            self.coins_collected += 1
            coin.reset()
        
        # Draw everything
        self.update_background()
        self.enemies.draw(self.screen)
        self.obstacles.draw(self.screen)
        self.powerups.draw(self.screen)
        self.coins.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        
        # Draw UI
        score_txt = self.font.render(f"Score: {self.score}", True, (255, 215, 0))
        dist_txt = self.font.render(f"Distance: {self.distance}m", True, (255, 255, 255))
        coins_txt = self.small_font.render(f"Coins: {self.coins_collected}", True, (255, 215, 0))
        
        self.screen.blit(score_txt, (10, 10))
        self.screen.blit(dist_txt, (10, 35))
        self.screen.blit(coins_txt, (10, 60))
        
        # High score indicator (if beaten)
        try:
            with open('leaderboard.json', 'r') as f:
                import json
                scores = json.load(f)
                if scores and self.score > scores[0].get('score', 0):
                    record_txt = self.small_font.render("NEW RECORD!", True, (255, 215, 0))
                    self.screen.blit(record_txt, (WIDTH - 120, 35))
        except:
            pass
        
        # Power-up info
        if self.active_powerup and self.powerup_timer > 0:
            seconds = self.powerup_timer // 60
            if self.active_powerup == 'Nitro':
                power_txt = self.font.render(f"NITRO: {seconds}s", True, (0, 255, 255))
            elif self.active_powerup == 'Shield':
                power_txt = self.font.render(f"SHIELD: {seconds}s", True, (0, 255, 0))
            else:
                power_txt = self.font.render(f"REPAIR", True, (255, 255, 0))
            self.screen.blit(power_txt, (WIDTH - 150, 10))
        
        # Difficulty indicator
        diff_colors = {1: (0, 255, 0), 2: (255, 255, 0), 3: (255, 0, 0)}
        diff_txt = self.small_font.render(f"Difficulty: {self.diff}", True, diff_colors.get(self.diff, (255, 255, 255)))
        self.screen.blit(diff_txt, (WIDTH - 100, HEIGHT - 30))
        
        return "play"
