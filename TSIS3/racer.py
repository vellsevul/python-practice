import pygame
import random

# Константы экрана
WIDTH, HEIGHT = 480, 600

class Player(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 70))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 7

    def move(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < WIDTH:
            self.rect.x += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, img, base_speed):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.base_speed = base_speed
        self.reset()

    def reset(self):
        # Спавним врагов так, чтобы они не вылетали за края с учетом нового размера
        self.rect.center = (random.randint(50, WIDTH-50), random.randint(-600, -100))
        self.speed = self.base_speed + random.randint(0, 2)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT: self.reset()

class Coin(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.raw_image = img
        self.reset()

    def reset(self):
        self.weight = random.choice([1, 5, 10])
        # Масштабируем монетку в зависимости от веса
        size = 25 + (self.weight * 2)
        self.image = pygame.transform.scale(self.raw_image, (size, size))
        self.rect = self.image.get_rect(center=(random.randint(50, WIDTH-50), random.randint(-500, -50)))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += 5
        if self.rect.top > HEIGHT: self.reset()

class Game:
    def __init__(self, screen, settings):
        self.screen = screen
        self.diff = settings.get("difficulty", 1)
        
        # Загружаем и сразу УМЕНЬШАЕМ картинки
        self.load_assets()
        
        self.player = Player(self.player_img)
        # Создаем врагов с уже уменьшенной картинкой
        self.enemies = pygame.sprite.Group([Enemy(self.enemy_img, 2 + self.diff) for _ in range(2 + self.diff)])
        self.coins = pygame.sprite.Group([Coin(self.coin_img) for _ in range(3)])
        
        self.score = 0
        self.distance = 0
        self.bg_y = 0
        self.font = pygame.font.SysFont("Verdana", 20, bold=True)

    def load_assets(self):
        # Желаемые размеры машин
        CAR_W, CAR_H = 45, 90 
        
        try:
            # Загружаем и масштабируем игрока
            p_orig = pygame.image.load("player.png").convert_alpha()
            self.player_img = pygame.transform.scale(p_orig, (CAR_W, CAR_H))
            
            # Загружаем и масштабируем врага
            e_orig = pygame.image.load("enemy.png").convert_alpha()
            self.enemy_img = pygame.transform.scale(e_orig, (CAR_W, CAR_H))
            
            # Монетку просто конвертируем (размер меняется в классе Coin)
            self.coin_img = pygame.image.load("coin.png").convert_alpha()
            
            # Дорога на весь экран
            r_orig = pygame.image.load("road.png").convert()
            self.road_img = pygame.transform.scale(r_orig, (WIDTH, HEIGHT))
            
        except Exception as e:
            print(f"Опять проблемы с файлами: {e}")
            # Если файлов нет, создаем маленькие прямоугольники
            self.player_img = pygame.Surface((CAR_W, CAR_H)); self.player_img.fill((0, 255, 0))
            self.enemy_img = pygame.Surface((CAR_W, CAR_H)); self.enemy_img.fill((255, 0, 0))
            self.coin_img = pygame.Surface((30, 30)); self.coin_img.fill((255, 215, 0))
            self.road_img = pygame.Surface((WIDTH, HEIGHT)); self.road_img.fill((50, 50, 50))

    def run(self):
        self.distance += 1
        self.player.move()
        self.enemies.update()
        self.coins.update()

        # Столкновения по маске теперь будут точными для маленьких машин
        if pygame.sprite.spritecollide(self.player, self.enemies, False, pygame.sprite.collide_mask):
            return "gameover"
        
        for c in pygame.sprite.spritecollide(self.player, self.coins, False, pygame.sprite.collide_mask):
            self.score += c.weight
            c.reset()

        # Рисуем фон
        self.bg_y = (self.bg_y + 5) % HEIGHT
        self.screen.blit(self.road_img, (0, self.bg_y - HEIGHT))
        self.screen.blit(self.road_img, (0, self.bg_y))
        
        self.enemies.draw(self.screen)
        self.coins.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)

        # Статистика
        s_txt = self.font.render(f"Score: {self.score}", True, (255, 215, 0))
        d_txt = self.font.render(f"{self.distance}m", True, (255, 255, 255))
        self.screen.blit(s_txt, (10, 10))
        self.screen.blit(d_txt, (10, 35))

        return "play"