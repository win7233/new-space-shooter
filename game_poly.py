# Programming 4 Lesson 4
# Space Shooter Game - Polymorphism version

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
        self.point_value = 0
        self.team = "neutral"       # Default

    def move(self):
        """Default move behaviour - child classes can override this."""
        self.y += self.speed

    def is_off_screen(self):
        """Default: never off screen.  Child classes override this."""
        return False

    def draw(self, screen):
        """To be overridden by each child class."""
        pass

    def collides_with(self, other):
        distance = ((self.x - other.x) **2 + (self.y - other.y)**2)**0.5
        return distance < 20

    def __str__(self):
        return f'{self.__class__.__name__} at ({self.x}, {self.y}) speed={self.speed}' 
    
    def __repr__(self):
        return f'{self.__class__.__name__}(x={self.x}, y={self.y}, speed={self.speed})'

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, speed=5, colour=GREEN)
        self.width = 30
        self.height = 20
        self.health = 3
        self.team = "player" 

    def move(self):
        pass

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

    def __str__(self):
        return f'Player at ({self.x}, {self.y}) HP: {self.health}'

class Bullet(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, speed=-8, colour=YELLOW)
        self.width = 4
        self.height = 10
        self.team = "player"

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
        self.point_value = 10
        self.team = "enemy"

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

    def __str__(self):
        return f'Enemy at ({self.x}, {self.y}) points:{self.point_value}'

    def __eq__(self, other):
        if not isinstance(other, Enemy):
            return NotImplemented
        return (self.point_value == other.point_value and   
                self.x == other.x and self.y == other.y)
            
    def __lt__(self, other):
        if not isinstance(other, Enemy):
            return NotImplemented
        return self.point_value < other.point_value

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

    def __str__(self):
        return f'FastEnemy at({self.x}, {self.y}  age:{self.age})'
    
class SpriteList:
    """A container that holds all game srites."""

    def __init__(self):
        self._sprites = []       # the internal list

    def add(self, sprite):
        self._sprites.append(sprite)

    def remove(self, sprite):
        self._sprites.remove(sprite)

    def update(self):
        """Call move() on every sprite"""
        for sprite in self._sprites:
            sprite.move()

    def draw(self, screen):
        """Call draw() on every sprite."""
        for sprite in self._sprites:
            sprite.draw(screen)

    def __len__(self):
        return len(self._sprites)

    def __contains__(self, sprite):
        return sprite in self._sprites
    
    def __iter__(self):
        return iter(self._sprites)
    
    def __str__(self):
        return f'SpriteList({len(self)} sprites)'

    def __repr__(self):
        return f'SpriteList({self._sprites!r})'
    
# ===== Initialize Pygame =====
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter OOP")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# ===== Game State =====
player = Player(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 60)
sprites = SpriteList()              # every game object lives here
sprites.add(player)
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
                b = Bullet(player.x, player.y)
                sprites.add(b)

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
            f = FastEnemy(x, 0)
            sprites.add(f)
        else:
            e = Enemy(x, 0)
            sprites.add(e)
        enemy_timer = 0
    
    # Update ALL sprites (polymorphism!)
    sprites.update()
    
    # Collision detection with instanceof bonus points
    to_remove = []

    for sprite1 in sprites:
        for sprite2 in sprites:
            if sprite1.team != sprite2.team: 
                    if sprite2.collides_with(sprite1):
                        score += sprite2.point_value
                        to_remove.append(sprite1)
                        to_remove.append(sprite2)
                        break    # bullet is gone, stop checking it
    
    for s in to_remove:
        if s in sprites:
            sprites.remove(s)
    
    # Remove sprites that have left the screen
    off_screen = []
    
    for s in sprites:
        if s.is_off_screen():
            off_screen.append(s)

    for s in off_screen:
        sprites.remove(s)

    # Draw everything
    screen.fill(BLACK)
    sprites.draw(screen)
    score_text = font.render(f'Score: {score}', True, WHITE)
    hp_text = font.render(f'HP:{player.health}', True, WHITE)
    info_text = font.render(f'Sprites: {len(sprites)}', True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(hp_text, (10, 36))
    screen.blit(info_text, (SCREEN_WIDTH - 160, 10))
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()


 