import pygame
import random

# Инициализация
pygame.init()

# Настройки экрана и сетки
CELL_SIZE = 20
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Practice 11: Levels & Timers")
clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
BLACK = (0, 0, 0)

# Шрифты
font = pygame.font.SysFont("Verdana", 25)

class Snake:
    def __init__(self):
        self.body = [(100, 100), (80, 100), (60, 100)]
        self.direction = pygame.K_RIGHT
        self.score = 0
        self.level = 1
        self.speed = 10

    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == pygame.K_UP: head_y -= CELL_SIZE
        elif self.direction == pygame.K_DOWN: head_y += CELL_SIZE
        elif self.direction == pygame.K_LEFT: head_x -= CELL_SIZE
        elif self.direction == pygame.K_RIGHT: head_x += CELL_SIZE
        
        self.body.insert(0, (head_x, head_y))

    def check_collision(self):
        head = self.body[0]
        # 1. Проверка границ (Border collision)
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            return True
        # 2. Столкновение с самим собой
        if head in self.body[1:]:
            return True
        return False

class Food:
    def __init__(self, snake_body):
        self.reset(snake_body)

    def reset(self, snake_body):
        # 3. Генерация еды так, чтобы она не упала на змейку
        while True:
            self.pos = (random.randint(0, (WIDTH-CELL_SIZE)//CELL_SIZE) * CELL_SIZE,
                        random.randint(0, (HEIGHT-CELL_SIZE)//CELL_SIZE) * CELL_SIZE)
            if self.pos not in snake_body:
                break
        
        # 4. Рандомный вес еды (Practice 11)
        self.weight = random.choice([1, 3, 5])
        self.color = RED if self.weight == 1 else GOLD
        
        # 5. Таймер еды (исчезает через 5 секунд / 5000 мс)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 5000 

    def is_expired(self):
        # Проверяем, не вышло ли время жизни еды
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.pos[0], self.pos[1], CELL_SIZE, CELL_SIZE))

# Создаем объекты
snake = Snake()
food = Food(snake.body)

running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # Запрещаем разворот на 180 градусов
            if event.key == pygame.K_UP and snake.direction != pygame.K_DOWN: snake.direction = event.key
            if event.key == pygame.K_DOWN and snake.direction != pygame.K_UP: snake.direction = event.key
            if event.key == pygame.K_LEFT and snake.direction != pygame.K_RIGHT: snake.direction = event.key
            if event.key == pygame.K_RIGHT and snake.direction != pygame.K_LEFT: snake.direction = event.key

    # Движение
    snake.move()

    # 6. Проверка уровня и скорости
    # Каждые 3 съеденных веса (или по очкам) повышаем уровень
    new_level = (snake.score // 5) + 1
    if new_level > snake.level:
        snake.level = new_level
        snake.speed += 2 # Увеличиваем скорость (Practice 11)

    # 7. Проверка: съели ли еду
    if snake.body[0] == food.pos:
        snake.score += food.weight
        food.reset(snake.body)
    else:
        snake.body.pop() # Убираем хвост, если не ели

    # 8. Проверка таймера еды
    if food.is_expired():
        food.reset(snake.body)

    # 9. Проверка проигрыша
    if snake.check_collision():
        print(f"GAME OVER! Level: {snake.level}, Score: {snake.score}")
        running = False

    # Отрисовка
    food.draw()
    for segment in snake.body:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE-2, CELL_SIZE-2))

    # UI: Счет и Уровень
    score_txt = font.render(f"Score: {snake.score}", True, WHITE)
    level_txt = font.render(f"Level: {snake.level}", True, WHITE)
    screen.blit(score_txt, (10, 10))
    screen.blit(level_txt, (10, 40))

    pygame.display.update()
    clock.tick(snake.speed)

pygame.quit()