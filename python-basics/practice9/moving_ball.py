import pygame

pygame.init()

WIDTH = 600
HEIGHT = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")

white = (255, 255, 255)
red = (255, 0, 0)

x = WIDTH // 2
y = HEIGHT // 2
radius = 25
step = 20

run = True

while run:
    screen.fill(white)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and x - step - radius >= 0:
                x -= step
            if event.key == pygame.K_RIGHT and x + step + radius <= WIDTH:
                x += step
            if event.key == pygame.K_UP and y - step - radius >= 0:
                y -= step
            if event.key == pygame.K_DOWN and y + step + radius <= HEIGHT:
                y += step

    pygame.draw.circle(screen, red, (x, y), radius)

    pygame.display.update()

pygame.quit()