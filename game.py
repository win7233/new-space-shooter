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
pyayer_y = SCREEN_HEIGHT - 50
player_speed = 5

# Lists to store game objects
enemies = []
bullets = []

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

