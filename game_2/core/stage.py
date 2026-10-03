import pygame
import random
from constants import *

class Stage:
    def __init__(self):
        self.bg_color = (30, 30, 50)
        self.grid_size = 100
        self.offset = 0
        self.scroll_speed = 2

    def update(self):
        # Slowly scroll the background for a "dynamic" feel
        self.offset += self.scroll_speed
        if self.offset >= self.grid_size:
            self.offset = 0

    def draw(self, surface):
        surface.fill(self.bg_color)

        # Draw a subtle cyber-grid background
        for x in range(0, SCREEN_WIDTH + self.grid_size, self.grid_size):
            pygame.draw.line(surface, (50, 50, 80), (x - self.offset, 0), (x - self.offset, SCREEN_HEIGHT), 1)

        for y in range(0, SCREEN_HEIGHT, self.grid_size):
            pygame.draw.line(surface, (50, 50, 80), (0, y), (SCREEN_WIDTH, y), 1)

        # Draw a stylized "fight floor"
        pygame.draw.rect(surface, (60, 60, 100), (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        pygame.draw.line(surface, (100, 100, 200), (0, SCREEN_HEIGHT - 50), (SCREEN_WIDTH, SCREEN_HEIGHT - 50), 3)
