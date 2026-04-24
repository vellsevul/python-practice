import pygame
import sys
from datetime import datetime
import math

pygame.init()

screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Mickey Clock")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# --- загрузка изображений ---
mickey = pygame.image.load("mickey.png").convert_alpha()
mickey = pygame.transform.scale(mickey, (400, 400))

hand = pygame.image.load("mickey_hand.png").convert_alpha()
hand = pygame.transform.scale(hand, (180, 180))

# --- центр часов ---
pivot = pygame.math.Vector2(300, 300)

# --- плечи (разнесли чуть в стороны) ---
left_pivot = pygame.math.Vector2(240, 280)
right_pivot = pygame.math.Vector2(330, 280)

# смещение руки
offset = pygame.math.Vector2(0, -60)


def get_time():
    now = datetime.now()
    return now.minute, now.second


def rotate_hand(image, angle, pivot, offset):
    rotated_image = pygame.transform.rotate(image, -angle)
    rotated_offset = offset.rotate(angle)
    rect = rotated_image.get_rect(center=pivot + rotated_offset)
    screen.blit(rotated_image, rect)

def draw_clock_face(center):
    circle_radius = 250
    number_radius = 240  # меньше круга

    for i in range(1, 13):
        angle = math.radians(i * 30 - 90)

        x = center.x + number_radius * math.cos(angle)
        y = center.y + number_radius * math.sin(angle)

        text = font.render(str(i), True, (0, 0, 0))
        rect = text.get_rect(center=(x, y))
        screen.blit(text, rect)

    # сам круг
    pygame.draw.circle(screen, (0, 0, 0),
                       (int(center.x), int(center.y)),
                       circle_radius, 2)


def draw_time(minutes, seconds):
    text = f"{minutes:02}:{seconds:02}"
    render = font.render(text, True, (0, 0, 0))
    rect = render.get_rect(center=(300, 560))
    screen.blit(render, rect)


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    minutes, seconds = get_time()

    # углы
    second_angle = seconds * 6
    minute_angle = minutes * 6 + seconds * 0.1

    screen.fill((255, 255, 255))

    # --- циферблат ---
    draw_clock_face(pivot)

    # --- Микки ---
    screen.blit(mickey, (100, 100))

    # --- руки ---
    rotate_hand(hand, second_angle, left_pivot, offset)   # секундная
    rotate_hand(hand, minute_angle, right_pivot, offset)  # минутная

    # --- цифровое время ---
    draw_time(minutes, seconds)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()