# Programming 4 Lesson 2
# Space Shooter Game - OOP version

import pygame
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

class Player:
    '''The player's spaceship.'''
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5          
    
    def move_left(self):
        """Move the player left, staying on screen."""
        if self.x > 0:
            self.x -= self.speed
    
    def move_right(self):
        """Move the player right, staying on screen."""
        if self.x < SCREEN_WIDTH - 20:      # Ship width is 20
            self.x += self.speed
        
    def draw(self, screen):
        """Draw the player as a green triangle"""
        points = [
            (self.x + 20 // 2, self.y),      # Top Centre point, Width = 20
            (self.x, self.y + 15),           # Bottom Left Corner point, Height = 15
            (self.x + 20, self.y + 15)        # Bottom Right Corner point
        ]
        pygame.draw.polygon(screen, GREEN, points)
  
class Bullet:
    """A bullet fired by the player."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = -7     # Negative speed = moving upward

    def move(self):
        """Move the bullet upward"""
        self.y += self.speed
    
    def is_off_screen(self):
        """Returns True if the bullet has left the top of the screen."""
        return self.y < 0
    
    def draw(self, screen):
        """Draws the bullet as a small yellow rectangle"""
        pygame.draw.rect(screen, YELLOW, (self.x - 2, self.y, 4, 10))

class Enemy:
    """An enemy spaceship."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.randint(2, 5)
        self.width = 10
        self.height = 30

    def move(self):
        """Move the enemy downward."""
        self.y += self.speed

    def is_off_screen(self):
        """Returns True if the enemy has moved past te bottom of the screen."""
        return self.y > SCREEN_HEIGHT

    def draw(self, screen):
        """Draw the enemy as a red rectangle"""
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

    def collides_with(self, bullet):
        """Return True if this enemy has been hit by the given bullet."""
        distance = ((self.x - bullet.x)**2 + (self.y - bullet.y)**2)**0.5
        return distance < 20

# ===== Initialize Pygame =====
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter OOP")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# ===== Game State =====
player = Player(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 60)
bullets = []
enemies = []
score = 0
enemy_timer = 0
running = True

# ===== Main Loop =====
while running:

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(Bullet(player.x + 3, player.y))

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right()

    # Spawn Enemies
    enemy_timer += 1
    if enemy_timer >= 60:
        enemies.append(Enemy(random.randint(0, SCREEN_WIDTH - 30),0))
        enemy_timer = 0
    
    # Update bullets
    for bullet in bullets[:]:
        bullet.move()
        if bullet.is_off_screen():
            bullets.remove(bullet)

    # Update enemies
    for enemy in enemies[:]:
        enemy.move()
        if enemy.is_off_screen():
            enemies.remove(enemy)

    # Collision detection
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if enemy.collides_with(bullet):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                break

    # Draw everything
    screen.fill(BLACK)
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()