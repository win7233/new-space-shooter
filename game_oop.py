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
        if self.x < SCREEN_WIDTH:
            self.x += self.speed
        
    def draw(self, screen):
        """Draw the player as a green triangle"""
        points = [
            (self.x + 6 // 2, self.y),      # Top Centre point
            (self.x, self.y + 7),           # Bottom Left Corner point
            (self.x + 6, self.y + 7)        # Bottom Right Corner point
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


    
