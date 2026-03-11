# Programming 4 Lesson 3
# Space Shooter Game - Inheritance version

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




        


