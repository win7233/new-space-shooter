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


    