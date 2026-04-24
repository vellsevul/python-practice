import pygame

# Инициализация
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint: 7-Brush, 8-Triangle, 1-6-Other Shapes")

# Холст
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

# Переменные
drawing = False
last_pos = None
current_tool = "brush"
current_color = (255, 0, 0)
brush_size = 5

running = True
while running:
    screen.blit(canvas, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Инструменты
            if event.key == pygame.K_1: current_tool = "rect"
            if event.key == pygame.K_2: current_tool = "circle"
            if event.key == pygame.K_3: current_tool = "square"
            if event.key == pygame.K_4: current_tool = "right_triangle"
            if event.key == pygame.K_5: current_tool = "rhombus"
            if event.key == pygame.K_6: 
                current_tool = "eraser"
                current_color = (255, 255, 255)
            if event.key == pygame.K_7: current_tool = "brush"
            if event.key == pygame.K_8: current_tool = "triangle" # Обычный треугольник
            
            # Цвета
            if event.key == pygame.K_r: current_color = (255, 0, 0)
            if event.key == pygame.K_g: current_color = (0, 255, 0)
            if event.key == pygame.K_b: current_color = (0, 0, 255)

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos
            last_pos = event.pos

        if event.type == pygame.MOUSEMOTION:
            if drawing and current_tool in ["brush", "eraser"]:
                pygame.draw.line(canvas, current_color, last_pos, event.pos, brush_size)
                last_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = event.pos
                x, y = start_pos
                w, h = end_pos[0] - x, end_pos[1] - y
                
                # Рисование фигур
                if current_tool == "rect":
                    pygame.draw.rect(canvas, current_color, (x, y, w, h), 2)
                elif current_tool == "circle":
                    radius = int(((w**2 + h**2)**0.5) / 2)
                    pygame.draw.circle(canvas, current_color, (x + w//2, y + h//2), radius, 2)
                elif current_tool == "square":
                    side = max(abs(w), abs(h))
                    pygame.draw.rect(canvas, current_color, (x, y, side, side), 2)
                elif current_tool == "right_triangle":
                    points = [(x, y), (x, y + h), (x + w, y + h)]
                    pygame.draw.polygon(canvas, current_color, points, 2)
                elif current_tool == "rhombus":
                    points = [(x + w//2, y), (x, y + h//2), (x + w//2, y + h), (x + w, y + h//2)]
                    pygame.draw.polygon(canvas, current_color, points, 2)
                elif current_tool == "triangle":
                    # ОБЫЧНЫЙ ТРЕУГОЛЬНИК (Равнобедренный)
                    # Вершина по центру X, основание внизу
                    points = [(x + w//2, y), (x, y + h), (x + w, y + h)]
                    pygame.draw.polygon(canvas, current_color, points, 2)

                drawing = False
                last_pos = None

    # UI панель
    pygame.draw.rect(screen, (30, 30, 30), (0, HEIGHT-40, WIDTH, 40))
    font = pygame.font.SysFont("Arial", 16)
    txt = f"Tool: {current_tool} | 7: Brush | 8: Triangle | 1-5: Shapes | 6: Eraser"
    screen.blit(font.render(txt, True, (255, 255, 255)), (10, HEIGHT-30))

    pygame.display.update()

pygame.quit()