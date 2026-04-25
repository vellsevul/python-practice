import pygame
import sys
from datetime import datetime
import math

# Инициализация
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Mickey Clock")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28, bold=True)

# Загрузка и масштабирование фона
background = pygame.image.load("clock.png").convert()
background = pygame.transform.scale(background, (600, 600))

# Загрузка и масштабирование тела Микки (300x300)
mickey = pygame.image.load("mickey.png").convert_alpha()
mickey_size = (300, 300)
mickey = pygame.transform.scale(mickey, mickey_size)
mickey_pos = ((600 - mickey_size[0]) // 2, (600 - mickey_size[1]) // 2)

# Загрузка заготовки руки
hand_source = pygame.image.load("mickey_hand.png").convert_alpha()

# Минутная стрелка (длиннее)
min_hand_img = pygame.transform.scale(hand_source, (170, 170))
min_offset = pygame.math.Vector2(0, -60)

# Секундная стрелка (короче)
sec_hand_img = pygame.transform.scale(hand_source, (130, 130))
sec_offset = pygame.math.Vector2(0, -45)

# Центр вращения
pivot = pygame.math.Vector2(300, 300)

def get_time():
    now = datetime.now()
    return now.minute, now.second

def rotate_hand(surface, image, angle, pivot, offset):
    rotated_image = pygame.transform.rotate(image, -angle)
    rotated_offset = offset.rotate(angle)
    rect = rotated_image.get_rect(center=pivot + rotated_offset)
    surface.blit(rotated_image, rect)

def draw_time(minutes, seconds):
    # Форматирование и отрисовка цифрового времени
    text_str = f"{minutes:02}:{seconds:02}"
    render = font.render(text_str, True, (40, 40, 40))
    rect = render.get_rect(center=(300, 560))
    screen.blit(render, rect)

# Основной цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    minutes, seconds = get_time()

    # Расчет углов
    second_angle = seconds * 6
    minute_angle = minutes * 6 + seconds * 0.1

    # Отрисовка слоев
    screen.blit(background, (0, 0))
    screen.blit(mickey, mickey_pos)

    # Отрисовка стрелок
    rotate_hand(screen, sec_hand_img, second_angle, pivot, sec_offset)
    rotate_hand(screen, min_hand_img, minute_angle, pivot, min_offset)

    # Отрисовка цифрового времени
    draw_time(minutes, seconds)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()