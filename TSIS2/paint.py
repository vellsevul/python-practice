import pygame
import datetime
from tools import flood_fill, draw_equilateral_triangle, draw_rhombus

pygame.init()

# Настройки окна
WIDTH, HEIGHT = 1100, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mega Paint: Palette & Tools")

# Константы для интерфейса
UI_WIDTH = 200
CANVAS_WIDTH = WIDTH - UI_WIDTH
canvas = pygame.Surface((CANVAS_WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

# Цвета палитры (Радуга + база)
PALETTE = [
    (255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), 
    (0, 0, 255), (75, 0, 130), (148, 0, 211), # Радуга
    (0, 0, 0), (255, 255, 255), (128, 128, 128), (101, 67, 33) # Черн, бел, сер, корич
]

TOOLS = ["pencil", "line", "rect", "circle", "square", "right_triangle", "equilateral", "rhombus", "fill", "text", "eraser"]
SIZES = [2, 5, 10]

# Состояние
current_color = (0, 0, 0)
current_tool = "pencil"
brush_size = 5
drawing = False
start_pos = None
last_pos = None
is_typing = False
text_content = ""
text_pos = (0, 0)

font = pygame.font.SysFont("Arial", 18)
bold_font = pygame.font.SysFont("Arial", 18, bold=True)

def draw_ui():
    # Фон панели
    pygame.draw.rect(screen, (220, 220, 220), (CANVAS_WIDTH, 0, UI_WIDTH, HEIGHT))
    pygame.draw.line(screen, (150, 150, 150), (CANVAS_WIDTH, 0), (CANVAS_WIDTH, HEIGHT), 2)

    # 1. Секция Цветов
    y_offset = 20
    screen.blit(bold_font.render("COLORS", True, (0, 0, 0)), (CANVAS_WIDTH + 10, y_offset))
    y_offset += 30
    
    color_rects = []
    for i, color in enumerate(PALETTE):
        rect = pygame.Rect(CANVAS_WIDTH + 15 + (i % 3) * 55, y_offset + (i // 3) * 55, 45, 45)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 1) # Обводка
        if color == current_color:
            pygame.draw.rect(screen, (0, 0, 0), rect, 3) # Выделение активного
        color_rects.append((rect, color))
    
    # 2. Секция Инструментов
    y_offset += 240
    screen.blit(bold_font.render("TOOLS", True, (0, 0, 0)), (CANVAS_WIDTH + 10, y_offset))
    y_offset += 30
    
    tool_rects = []
    for i, tool in enumerate(TOOLS):
        rect = pygame.Rect(CANVAS_WIDTH + 10, y_offset + i * 32, UI_WIDTH - 20, 28)
        color = (180, 180, 180) if tool == current_tool else (255, 255, 255)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 1)
        screen.blit(font.render(tool.capitalize(), True, (0, 0, 0)), (rect.x + 5, rect.y + 3))
        tool_rects.append((rect, tool))

    # 3. Секция Размеров
    y_offset = HEIGHT - 100
    screen.blit(bold_font.render("BRUSH SIZE", True, (0, 0, 0)), (CANVAS_WIDTH + 10, y_offset))
    size_rects = []
    for i, s in enumerate(SIZES):
        rect = pygame.Rect(CANVAS_WIDTH + 15 + i * 60, y_offset + 30, 50, 30)
        bg = (180, 180, 180) if s == brush_size else (255, 255, 255)
        pygame.draw.rect(screen, bg, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 1)
        screen.blit(font.render(str(s), True, (0, 0, 0)), (rect.centerx - 5, rect.centery - 10))
        size_rects.append((rect, s))

    return color_rects, tool_rects, size_rects

running = True
while running:
    screen.fill((255, 255, 255))
    screen.blit(canvas, (0, 0))
    color_rects, tool_rects, size_rects = draw_ui()
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if is_typing:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    txt_surf = font.render(text_content, True, current_color)
                    canvas.blit(txt_surf, text_pos)
                    text_content, is_typing = "", False
                elif event.key == pygame.K_BACKSPACE: text_content = text_content[:-1]
                else: text_content += event.unicode
            continue

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Проверка клика по UI
            if mouse_pos[0] > CANVAS_WIDTH:
                for rect, color in color_rects:
                    if rect.collidepoint(mouse_pos): current_color = color
                for rect, tool in tool_rects:
                    if rect.collidepoint(mouse_pos): 
                        current_tool = tool
                        if tool == "eraser": current_color = (255, 255, 255)
                for rect, s in size_rects:
                    if rect.collidepoint(mouse_pos): brush_size = s
            else:
                # Клик по холсту
                if current_tool == "fill":
                    flood_fill(canvas, mouse_pos[0], mouse_pos[1], current_color)
                elif current_tool == "text":
                    is_typing, text_pos = True, mouse_pos
                else:
                    drawing = True
                    start_pos = mouse_pos
                    last_pos = mouse_pos

        if event.type == pygame.MOUSEMOTION and drawing:
            if current_tool in ["pencil", "eraser"]:
                pygame.draw.line(canvas, current_color, last_pos, mouse_pos, brush_size)
                last_pos = mouse_pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                x, y = start_pos
                w, h = mouse_pos[0] - x, mouse_pos[1] - y
                # Отрисовка всех фигур
                if current_tool == "line": pygame.draw.line(canvas, current_color, start_pos, mouse_pos, brush_size)
                elif current_tool == "rect": pygame.draw.rect(canvas, current_color, (x, y, w, h), brush_size)
                elif current_tool == "circle":
                    r = int(((w**2 + h**2)**0.5) / 2)
                    pygame.draw.circle(canvas, current_color, (x + w//2, y + h//2), r, brush_size)
                elif current_tool == "square":
                    side = max(abs(w), abs(h))
                    pygame.draw.rect(canvas, current_color, (x, y, side, side), brush_size)
                elif current_tool == "right_triangle":
                    pygame.draw.polygon(canvas, current_color, [(x, y), (x, y + h), (x + w, y + h)], brush_size)
                elif current_tool == "equilateral": draw_equilateral_triangle(canvas, current_color, start_pos, mouse_pos, brush_size)
                elif current_tool == "rhombus": draw_rhombus(canvas, current_color, start_pos, mouse_pos, brush_size)
                drawing = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                name = f"save_{datetime.datetime.now().strftime('%H%M%S')}.png"
                pygame.image.save(canvas, name)

    # Предпросмотр
    if drawing and current_tool not in ["pencil", "eraser"]:
        x, y = start_pos
        w, h = mouse_pos[0] - x, mouse_pos[1] - y
        if current_tool == "line": pygame.draw.line(screen, current_color, start_pos, mouse_pos, brush_size)
        elif current_tool == "rect": pygame.draw.rect(screen, current_color, (x, y, w, h), brush_size)
        # Можно добавить остальные превью по аналогии

    if is_typing:
        screen.blit(font.render(text_content + "|", True, current_color), text_pos)

    pygame.display.flip()

pygame.quit()