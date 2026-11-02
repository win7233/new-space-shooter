# Programming 4 Lesson 3
# Space Shooter Game - Inheritance version

import pygame
import random
import math

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
ORANGE = (255, 165, 0)

class Entity:
    """Base class for all game objects that exist on screen."""

    def __init__(self, x, y, speed, colour):
        self.x = x
        self.y = y
        self.speed = speed
        self.colour = colour

    def move(self):
        """Default move behaviour - child classes can override this."""
        self.y += self.speed

    def draw(self, screen):
        """To be overridden by each child class."""
        pass

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, speed=5, colour=GREEN)
        self.width = 30
        self.height = 20

    def move_left(self):
        if self.x > 0:
            self.x -= self.speed
        
    def move_right(self):
        if self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
        
    def draw(self, screen):
        """Override Entity.draw() to draw a green triangle ship."""
        tip_x = self.x + self.width // 2
        points = [
            (tip_x, self.y),
            (self.x, self.y+self.height),
            (self.x + self.width, self.y + self.height)
        ]
        pygame.draw.polygon(screen, self.colour, points)

class Bullet(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, speed=-8, colour=YELLOW)
        self.width = 4
        self.height = 10

    #move() is inherited from Entity - we don't need to rewrite it
    #Entity.move() adds self.speed to self.y, which is -8 so it goes up

    def is_off_screen(self):
        return self.y < 0
    
    def draw(self, screen):
        """Override Entity.draw() to draw a yellow rectangle."""
        pygame.draw.rect(
            screen, self.colour,
            (self.x - self.width // 2, self.y, self.width, self.height)
        )

class Enemy(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, speed=2, colour=RED)
        self.size = 20

    # move is inherited from Entity - enemy drifts downward automatically

    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT
    
    def collides_with(self, bullet):
        """Return True if bullet is within 20px of this enemy's centre."""
        distance = ((self.x - bullet.x)**2 + (self.y - bullet.y)**2)**0.5
        return distance < 20
    
    def draw(self, screen):
        """Override Entity.draw() to draw a red diamond."""
        points = [
            (self.x, self.y - self.size),       # top
            (self.x + self.size, self.y),       # right
            (self.x, self.y + self.size),       # bottom
            (self.x - self.size, self.y)        # left

        ]
        pygame.draw.polygon(screen, self.colour, points)

class FastEnemy(Enemy):
    """
    A dangerous variant that moves faster and zigzags.
    FastEnemy s an Enemy, which is an Entity -- a 3-level hierarchy!
    """

    def __init__(self, x, y):
        super().__init__(x, y)      # calls Enemy.__init__
        self.speed = 5              # override the default speed from Enemy
        self.colour = ORANGE        # stand out - make it orange
        self.age = 0                # track how long this enemy has been alive

    def move(self):                 # override Entity.move() entirely
        """Move down fast AND drift sideways using a sine wave."""
        self.age += 1
        self.y += self.speed
        self.x += int(math.sin(self.age * 0.1) * 3)     # zigzag!

    def draw(self, screen):
        """Draw a scary looking X shape instead of a diamond."""
        s = self.size
        pygame.draw.line(screen, self.colour, (self.x - s, self.y - s), (self.x + s, self.y + s), 3)
        pygame.draw.line(screen, self.colour, (self.x + s, self.y - s), (self.x - s, self.y + s), 3)

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

    # Spawn Enemies - occasionally make a fast one
    enemy_timer += 1
    if enemy_timer >= 60:
        x = random.randint(20, SCREEN_WIDTH - 20)
        if random.random() < 0.25:      # 25% chance of a FastEnemy
            enemies.append(FastEnemy(x, 0))
        else:
            enemies.append(Enemy(x, 0))
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

    # Collision detection with instanceof bonus points
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if enemy.collides_with(bullet):
                bullets.remove(bullet)
                enemies.remove(enemy)
                if isinstance(enemy, FastEnemy):   # bonus points!
                    score += 25
                else:
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

