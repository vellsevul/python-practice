# config.py
import pygame

# Initialize pygame for colors
pygame.init()

# Screen settings
CELL_SIZE = 20
WIDTH, HEIGHT = 800, 600
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)
DARK_RED = (139, 0, 0)  # Poison food
GOLD = (255, 215, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 200, 255)  # Speed boost power-up
PURPLE = (128, 0, 128)  # Slow motion power-up
YELLOW = (255, 255, 0)  # Shield power-up
GRAY = (128, 128, 128)  # Obstacles
ORANGE = (255, 165, 0)

# Game settings
INITIAL_SPEED = 10
SPEED_INCREMENT = 2
FOODS_PER_LEVEL = 3

# Power-up settings
POWERUP_DURATION = 5000  # 5 seconds
POWERUP_FIELD_DURATION = 8000  # 8 seconds on field

# Food settings
FOOD_LIFETIME = 5000  # 5 seconds

# Font settings
FONT_SIZE = 25
FONT_SIZE_LARGE = 50
FONT_SIZE_MEDIUM = 35

#Sound effects
SOUND_ENABLED = True
SOUND_VOLUME = 0.5