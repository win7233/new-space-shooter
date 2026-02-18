# Programming 4 Lesson 1 
# Space Shooter Game

import pygame
import random

# ===== Game Constants =====
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Space Shooter - Procedural Style')
clock = pygame.time.Clock()

# Player variables
player_x =  SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 50
player_speed = 5

# Lists to store game objects
enemies = []
bullets = []

# Game variables
running = True
score = 0
enemy_spawn_timer = 0

def draw_player(screen, x, y):
    """Draw the player's spaceship as a triangle"""
    points = [
        (x, y - 20),        # Top point
        (x - 15, y + 20),    # Bottom left
        (x + 15, y + 20)    # Bottom right
    ]
    pygame.draw.polygon(screen, GREEN, points)

def draw_enemy(screen, x, y):
    """Draw an enemy as a red circle"""
    pygame.draw.circle(screen, RED, (int(x), int(y)), 15)

def draw_bullet(screen, x, y):
    """Draw a bullet as a white rectangle"""
    pygame.draw.rect(screen, WHITE, (int(x) - 2, int(y) - 5, 4, 10))

def create_enemy():
    """Create a new enemy with random position and speed"""
    enemy = {
        'x': random.randint(20, SCREEN_WIDTH - 20),
        'y': -20,
        'speed': random.randint(1, 3)
    }
    return enemy

# Main Game loop
while running:
    clock.tick(FPS)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Create a bullet
                bullet = {
                    'x': player_x,
                    'y': player_y,
                    'speed': -7
                }
                bullets.append(bullet)

    # Player Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 20:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - 20:
        player_x += player_speed

    # Spawn enemies
    enemy_spawn_timer += 1
    if enemy_spawn_timer >= 60:     # Spawn every second
        enemies.append(create_enemy())
        enemy_spawn_timer = 0 

    # Update enemies
    for enemy in enemies[:]:        # Use slice to avoid modifying list while iterating 
        enemy['y'] += enemy['speed']
        if enemy['y'] > SCREEN_HEIGHT:
            enemies.remove(enemy)

    # Update bullets
    for bullet in bullets[:]:   
        bullet['y'] += bullet['speed']
        if bullet['y'] < 0:
            bullets.remove(bullet)

    # Check for collisions
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            # Simple circle collision detection
            distance = ((bullet['x'] - enemy['x'])**2 + (bullet['y'] - enemy['y'])**2)**0.5
            if distance < 20:
                if bullet in bullets:
                    bullets.remove(bullet)
                if enemy in enemies:
                    enemies.remove(enemy)
                score += 10
                break

    # Draw everything
    screen.fill(BLACK)

    # Draw player
    draw_player(screen, player_x, player_y)

    # Draw all enemies
    for enemy in enemies:
        draw_enemy(screen, enemy['x'], enemy['y'])
    
    # Draw all bullets
    for bullet in bullets:
        draw_bullet(screen, bullet['x'], bullet['y'])

    # Draw score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10,10))

    pygame.display.flip()

pygame.quit()

