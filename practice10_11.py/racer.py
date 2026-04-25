import pygame
import random

pygame.init()

WIDTH, HEIGHT = 480, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer: Pixel Perfect Edition")
clock = pygame.time.Clock()

# --- Загрузка ресурсов ---
try:
    player_img = pygame.image.load("player.png").convert_alpha()
    enemy_img = pygame.image.load("enemy.png").convert_alpha()
    coin_img = pygame.image.load("coin.png").convert_alpha()
    road_img = pygame.transform.scale(pygame.image.load("road.png"), (WIDTH, HEIGHT))
except:
    print("Ошибка загрузки картинок!")
    pygame.quit()
    exit()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT - 70))
        # СОЗДАЕМ МАСКУ (контур машинки)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 7

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.move_ip(self.speed, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        # СОЗДАЕМ МАСКУ ДЛЯ ВРАГА
        self.mask = pygame.mask.from_surface(self.image)
        self.reset()

    def reset(self):
        self.rect.center = (random.randint(40, WIDTH-40), -100)
        self.speed = random.randint(4, 7)

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.reset()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(coin_img, (30, 30))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image) # Тоже маска
        self.reset()

    def reset(self):
        self.rect.center = (random.randint(40, WIDTH-40), -50)
        self.weight = random.choice([1, 5, 10])

    def move(self):
        self.rect.move_ip(0, 5)
        if self.rect.top > HEIGHT:
            self.reset()

# Создание объектов
P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)
coins_group = pygame.sprite.Group()
coins_group.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

score = 0
font = pygame.font.SysFont("Verdana", 20)

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(road_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    P1.move()
    E1.move()
    C1.move()

    # --- СТОЛКНОВЕНИЕ С МОНЕТОЙ (теперь по маске) ---
    if pygame.sprite.spritecollide(P1, coins_group, False, pygame.sprite.collide_mask):
        score += C1.weight
        C1.reset()

    # --- СТОЛКНОВЕНИЕ С ВРАГОМ (теперь по маске) ---
    # Добавляем аргумент pygame.sprite.collide_mask — это и есть магия точности
    if pygame.sprite.spritecollideany(P1, enemies, pygame.sprite.collide_mask):
        print(f"GAME OVER! Score: {score}")
        running = False

    # Отрисовка
    for sprite in all_sprites:
        screen.blit(sprite.image, sprite.rect)

    score_text = font.render(f"Coins: {score}", True, (255, 255, 255))
    screen.blit(score_text, (WIDTH - 120, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()