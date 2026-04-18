import pygame
import sys
import math
from datetime import datetime

pygame.init()

screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Mickey Clock")

# загрузка картинки стрелки
hand_image = pygame.image.load("mickey_hand.png").convert_alpha()
center = (300, 300)
hand_image = pygame.image.load("mickey_hand.png").convert_alpha()
hand_image = pygame.transform.scale(hand_image, (120, 120)) 
clock = pygame.time.Clock()

def get_time():
    now = datetime.now()
    return now.minute, now.second

def draw_hand(image, angle):
    rotated = pygame.transform.rotate(image, -angle)
    rect = rotated.get_rect(center=center)
    screen.blit(rotated, rect)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    minutes, seconds = get_time()

    second_angle = seconds * 6
    minute_angle = minutes * 6 + seconds * 0.1

    screen.fill((255, 255, 255))

    # секундная (левая рука)
    draw_hand(hand_image, second_angle)

    # минутная (правая рука)
    draw_hand(hand_image, minute_angle)

    pygame.display.flip()
    clock.tick(1)

pygame.quit()
sys.exit()