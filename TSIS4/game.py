# game.py
import pygame
import random
import json
from config import *
from db import Database

class Snake:
    """Snake class with movement and collision detection"""
    def __init__(self, start_positions=None):
        if start_positions is None:
            self.body = [(CELL_SIZE * 5, CELL_SIZE * 5),
                        (CELL_SIZE * 4, CELL_SIZE * 5),
                        (CELL_SIZE * 3, CELL_SIZE * 5)]
        else:
            self.body = start_positions
        self.direction = pygame.K_RIGHT
        self.next_direction = pygame.K_RIGHT
        self.shield_active = False
        self.speed = INITIAL_SPEED  # Add speed attribute
    
    def move(self):
        """Move snake forward"""
        head_x, head_y = self.body[0]
        
        # Use buffered direction
        self.direction = self.next_direction
        
        if self.direction == pygame.K_UP: head_y -= CELL_SIZE
        elif self.direction == pygame.K_DOWN: head_y += CELL_SIZE
        elif self.direction == pygame.K_LEFT: head_x -= CELL_SIZE
        elif self.direction == pygame.K_RIGHT: head_x += CELL_SIZE
        
        self.body.insert(0, (head_x, head_y))
    
    def change_direction(self, key):
        """Change snake direction (prevent 180-degree turns)"""
        if key == pygame.K_UP and self.direction != pygame.K_DOWN:
            self.next_direction = key
        elif key == pygame.K_DOWN and self.direction != pygame.K_UP:
            self.next_direction = key
        elif key == pygame.K_LEFT and self.direction != pygame.K_RIGHT:
            self.next_direction = key
        elif key == pygame.K_RIGHT and self.direction != pygame.K_LEFT:
            self.next_direction = key
    
    def cut(self, segments=2):
        """Cut snake length (for poison food)"""
        for _ in range(segments):
            if len(self.body) > 1:
                self.body.pop()
    
    def get_head(self):
        return self.body[0]
    
    def check_self_collision(self):
        """Check if snake collides with itself"""
        head = self.body[0]
        return head in self.body[1:]
    
    def draw(self, screen, snake_color):
        """Draw snake on screen"""
        for i, segment in enumerate(self.body):
            color = snake_color if not self.shield_active or i > 0 else YELLOW
            pygame.draw.rect(screen, color, 
                           (segment[0], segment[1], CELL_SIZE - 2, CELL_SIZE - 2))

class Food:
    """Normal food with weight and timer"""
    def __init__(self, snake_body, obstacles, powerup_positions):
        self.reset(snake_body, obstacles, powerup_positions)
    
    def reset(self, snake_body, obstacles, powerup_positions):
        """Generate new food position avoiding snake, obstacles, and power-ups"""
        all_occupied = set(snake_body) | set(obstacles) | set(powerup_positions)
        
        # Prevent infinite loop
        attempts = 0
        while True:
            self.pos = (random.randint(0, GRID_WIDTH - 1) * CELL_SIZE,
                       random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE)
            if self.pos not in all_occupied or attempts > 1000:
                break
            attempts += 1
        
        # Random weight (Practice 11)
        weights = [1, 1, 1, 3, 5]  # More chance for weight 1
        self.weight = random.choice(weights)
        
        if self.weight == 1:
            self.color = RED
        elif self.weight == 3:
            self.color = GOLD
        else:
            self.color = ORANGE
        
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = FOOD_LIFETIME
    
    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, 
                        (self.pos[0], self.pos[1], CELL_SIZE, CELL_SIZE))

class PoisonFood:
    """Poison food that shortens snake"""
    def __init__(self, snake_body, obstacles, powerup_positions):
        self.active = True
        self.reset(snake_body, obstacles, powerup_positions)
    
    def reset(self, snake_body, obstacles, powerup_positions):
        all_occupied = set(snake_body) | set(obstacles) | set(powerup_positions)
        
        attempts = 0
        while True:
            self.pos = (random.randint(0, GRID_WIDTH - 1) * CELL_SIZE,
                       random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE)
            if self.pos not in all_occupied or attempts > 1000:
                break
            attempts += 1
        
        self.color = DARK_RED
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = FOOD_LIFETIME
    
    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime
    
    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, self.color, 
                           (self.pos[0], self.pos[1], CELL_SIZE, CELL_SIZE))

class PowerUp:
    """Power-up items with different effects"""
    TYPES = ['speed_boost', 'slow_motion', 'shield']
    
    def __init__(self, snake_body, obstacles, foods, poison_food):
        self.active = True
        self.reset(snake_body, obstacles, foods, poison_food)
    
    def reset(self, snake_body, obstacles, foods, poison_food):
        all_occupied = set(snake_body) | set(obstacles)
        # Also avoid foods and poison foods
        for food in foods:
            all_occupied.add(food.pos)
        if poison_food and poison_food.active:
            all_occupied.add(poison_food.pos)
        
        attempts = 0
        while True:
            self.pos = (random.randint(0, GRID_WIDTH - 1) * CELL_SIZE,
                       random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE)
            if self.pos not in all_occupied or attempts > 1000:
                break
            attempts += 1
        
        self.type = random.choice(self.TYPES)
        if self.type == 'speed_boost':
            self.color = LIGHT_BLUE
        elif self.type == 'slow_motion':
            self.color = PURPLE
        else:  # shield
            self.color = YELLOW
        
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = POWERUP_FIELD_DURATION
    
    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime
    
    def apply_effect(self, game_state):
        """Apply power-up effect to game state"""
        game_state.active_powerup = self.type
        game_state.powerup_start_time = pygame.time.get_ticks()
        
        if self.type == 'speed_boost':
            game_state.snake.speed = min(game_state.snake.speed + 3, 25)
        elif self.type == 'slow_motion':
            game_state.snake.speed = max(game_state.snake.speed - 3, 5)
        elif self.type == 'shield':
            game_state.snake.shield_active = True
    
    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, self.color,
                           (self.pos[0], self.pos[1], CELL_SIZE, CELL_SIZE))

class Obstacles:
    """Static obstacles that appear from level 3"""
    def __init__(self, level, snake_head, count=5):
        self.blocks = []
        if level >= 3:
            self.generate(count, snake_head)
    
    def generate(self, count, snake_head):
        """Generate obstacle blocks avoiding snake head"""
        head_x, head_y = snake_head
        head_grid_x = head_x // CELL_SIZE
        head_grid_y = head_y // CELL_SIZE
        
        for _ in range(count):
            attempts = 0
            while True:
                x = random.randint(0, GRID_WIDTH - 1)
                y = random.randint(0, GRID_HEIGHT - 1)
                # Don't place obstacles near snake head (within 2 cells)
                if (abs(x - head_grid_x) > 2 or abs(y - head_grid_y) > 2) and \
                   (x * CELL_SIZE, y * CELL_SIZE) not in self.blocks and attempts < 100:
                    self.blocks.append((x * CELL_SIZE, y * CELL_SIZE))
                    break
                attempts += 1
    
    def check_collision(self, head):
        """Check if snake collides with obstacle"""
        return head in self.blocks
    
    def draw(self, screen):
        for block in self.blocks:
            pygame.draw.rect(screen, GRAY,
                           (block[0], block[1], CELL_SIZE, CELL_SIZE))

class GameState:
    """Main game state manager"""
    def __init__(self, db, username, settings):
        self.db = db
        self.username = username
        self.settings = settings  # This is the Settings object
        self.reset_game()
    
    def reset_game(self):
        """Reset all game variables"""
        self.snake = Snake()
        self.obstacles = Obstacles(1, self.snake.get_head())
        self.powerup = None
        self.active_powerup = None
        self.powerup_start_time = 0
        
        # Foods
        self.foods = []
        self.poison_food = None
        self._generate_initial_foods()
        
        # Game stats
        self.score = 0
        self.level = 1
        self.food_counter = 0
        self.snake.speed = INITIAL_SPEED
        self.game_over = False
        
        # Timers
        self.last_powerup_spawn = 0
        self.snake_move_timer = 0
    
    def _generate_initial_foods(self):
        """Generate initial food and poison food"""
        self.foods = []
        # Generate 2 normal foods initially
        powerup_positions = [self.powerup.pos] if self.powerup and self.powerup.active else []
        for _ in range(2):
            self.foods.append(Food(self.snake.body, self.obstacles.blocks, powerup_positions))
        
        # Generate poison food with 30% chance
        if random.random() < 0.3:
            self.poison_food = PoisonFood(self.snake.body, self.obstacles.blocks, powerup_positions)
    
    def update_level(self):
        """Update level based on score"""
        new_level = (self.score // (FOODS_PER_LEVEL * 5)) + 1
        
        if new_level > self.level:
            self.level = new_level
            self.snake.speed += SPEED_INCREMENT
            # Regenerate obstacles for new level
            self.obstacles = Obstacles(self.level, self.snake.get_head())
    
    def check_collisions(self):
        """Check all collision types"""
        head = self.snake.get_head()
        
        # Border collision
        if (head[0] < 0 or head[0] >= WIDTH or 
            head[1] < 0 or head[1] >= HEIGHT):
            if self.snake.shield_active:
                # Teleport to other side when shield is active
                if head[0] < 0: new_head = (WIDTH - CELL_SIZE, head[1])
                elif head[0] >= WIDTH: new_head = (0, head[1])
                elif head[1] < 0: new_head = (head[0], HEIGHT - CELL_SIZE)
                else: new_head = (head[0], 0)
                self.snake.body[0] = new_head
                self.snake.shield_active = False
                return False
            return True
        
        # Obstacle collision
        if self.obstacles.check_collision(head):
            if self.snake.shield_active:
                self.snake.shield_active = False
                return False
            return True
        
        # Self collision
        if self.snake.check_self_collision():
            if self.snake.shield_active:
                self.snake.shield_active = False
                return False
            return True
        
        return False
    
    def check_food_collision(self):
        """Check if snake eats food"""
        head = self.snake.get_head()
        
        # Normal food
        for food in self.foods[:]:
            if head == food.pos:
                self.score += food.weight
                self.food_counter += 1
                self.foods.remove(food)
                powerup_positions = [self.powerup.pos] if self.powerup and self.powerup.active else []
                # Add new food
                self.foods.append(Food(self.snake.body, self.obstacles.blocks, powerup_positions))
                return True  # Ate food, snake grows (don't pop tail)
        
        # Poison food
        if self.poison_food and self.poison_food.active and head == self.poison_food.pos:
            self.snake.cut(2)
            self.poison_food.active = False
            if len(self.snake.body) <= 1:
                self.game_over = True
            return True
        
        # No food eaten, remove tail
        self.snake.body.pop()
        return False
    
    def check_powerup_collision(self):
        """Check if snake collects power-up"""
        if self.powerup and self.powerup.active:
            head = self.snake.get_head()
            if head == self.powerup.pos:
                self.powerup.apply_effect(self)
                self.powerup.active = False
                return True
        return False
    
    def update_powerups(self):
        """Update power-up timers and spawn new ones"""
        # Remove expired power-up effect
        if self.active_powerup:
            elapsed = pygame.time.get_ticks() - self.powerup_start_time
            if elapsed > POWERUP_DURATION:
                # Reset effects
                if self.active_powerup == 'speed_boost':
                    self.snake.speed = INITIAL_SPEED + (self.level - 1) * SPEED_INCREMENT
                elif self.active_powerup == 'slow_motion':
                    self.snake.speed = INITIAL_SPEED + (self.level - 1) * SPEED_INCREMENT
                elif self.active_powerup == 'shield':
                    self.snake.shield_active = False
                self.active_powerup = None
        
        # Spawn new power-up if needed
        current_time = pygame.time.get_ticks()
        if not self.powerup and current_time - self.last_powerup_spawn > 10000:
            self.powerup = PowerUp(self.snake.body, self.obstacles.blocks,
                                 self.foods, self.poison_food)
            self.last_powerup_spawn = current_time
        
        # Remove expired power-up from field
        if self.powerup and self.powerup.is_expired():
            self.powerup = None
    
    def update_foods(self):
        """Update food timers and regenerate expired ones"""
        powerup_positions = [self.powerup.pos] if self.powerup and self.powerup.active else []
        
        # Check expired normal foods
        for food in self.foods[:]:
            if food.is_expired():
                self.foods.remove(food)
                self.foods.append(Food(self.snake.body, self.obstacles.blocks, powerup_positions))
        
        # Check expired poison food
        if self.poison_food and self.poison_food.is_expired():
            self.poison_food = None
    
    def update(self):
        """Main game update loop"""
        if self.game_over:
            return
        
        self.snake.move()
        
        # Check collisions after move
        if self.check_collisions():
            self.game_over = True
            return
        
        # Check food and power-up collisions
        self.check_food_collision()
        self.check_powerup_collision()
        
        # Update game elements
        self.update_foods()
        self.update_powerups()
        self.update_level()
        
        # Spawn new poison food occasionally
        if not self.poison_food and random.random() < 0.005 and len(self.foods) < 3:
            powerup_positions = [self.powerup.pos] if self.powerup and self.powerup.active else []
            self.poison_food = PoisonFood(self.snake.body, self.obstacles.blocks, powerup_positions)
    
    def draw(self, screen):
        """Draw all game elements"""
        # Grid overlay - FIXED: access settings correctly
        if self.settings.grid_overlay:  # Direct attribute access, not .get()
            for x in range(0, WIDTH, CELL_SIZE):
                pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, CELL_SIZE):
                pygame.draw.line(screen, (50, 50, 50), (0, y), (WIDTH, y))
        
        # Draw obstacles
        self.obstacles.draw(screen)
        
        # Draw foods
        for food in self.foods:
            food.draw(screen)
        
        # Draw poison food
        if self.poison_food and self.poison_food.active:
            self.poison_food.draw(screen)
        
        # Draw power-up
        if self.powerup and self.powerup.active:
            self.powerup.draw(screen)
        
        # Draw snake - FIXED: access snake_color correctly
        self.snake.draw(screen, self.settings.snake_color)
        
        # Draw UI text
        font = pygame.font.SysFont("Verdana", FONT_SIZE)
        
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        personal_best = font.render(f"Best: {self.db.get_personal_best(self.username)}", True, WHITE)
        
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 40))
        screen.blit(personal_best, (10, 70))
        
        # Show active power-up
        if self.active_powerup:
            remaining = max(0, (POWERUP_DURATION - (pygame.time.get_ticks() - self.powerup_start_time)) // 1000)
            powerup_text = font.render(f"{self.active_powerup}: {remaining}s", True, YELLOW)
            screen.blit(powerup_text, (WIDTH - 200, 10))