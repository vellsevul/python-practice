import pygame
import os

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((600, 200))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont(None, 35)

songs = ["track1.mp3", "track2.mp3"]
current = 0

def load_song():
    pygame.mixer.music.load(songs[current])
    pygame.mixer.music.play()

load_song()

run = True

while run:
    screen.fill((255,255,255))

    text = font.render("Now: " + songs[current], True, (0,0,0))
    screen.blit(text, (20, 80))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_p:
                pygame.mixer.music.play()

            if event.key == pygame.K_s:
                pygame.mixer.music.stop()

            if event.key == pygame.K_n:
                current = (current + 1) % len(songs)
                load_song()
                pygame.mixer.music.play()

            if event.key == pygame.K_b:
                current = (current - 1) % len(songs)
                load_song()
                pygame.mixer.music.play()

            if event.key == pygame.K_q:
                run = False

    pygame.display.update()

pygame.quit()