import pygame

def flood_fill(surface, x, y, new_color):
    target_color = surface.get_at((x, y))
    if target_color == new_color: return
    
    stack = [(x, y)]
    width, height = surface.get_size()
    while stack:
        curr_x, curr_y = stack.pop()
        if not (0 <= curr_x < width and 0 <= curr_y < height): continue
        if surface.get_at((curr_x, curr_y)) != target_color: continue
            
        surface.set_at((curr_x, curr_y), new_color)
        stack.append((curr_x + 1, curr_y))
        stack.append((curr_x - 1, curr_y))
        stack.append((curr_x, curr_y + 1))
        stack.append((curr_x, curr_y - 1))

def draw_equilateral_triangle(surf, color, start, end, size):
    x, y = start
    w = end[0] - x
    h = int(abs(w) * 0.866) * (1 if (end[1] - y) > 0 else -1)
    points = [(x + w // 2, y), (x, y + h), (x + w, y + h)]
    pygame.draw.polygon(surf, color, points, size)

def draw_rhombus(surf, color, start, end, size):
    x, y = start
    w, h = end[0] - x, end[1] - y
    points = [(x + w // 2, y), (x, y + h // 2), (x + w // 2, y + h), (x + w, y + h // 2)]
    pygame.draw.polygon(surf, color, points, size)