import pygame
from constants import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(0, 0)
        self.width = width
        self.height = height
        self.color = color

    def apply_force(self, force):
        self.acc += force

    def update(self):
        self.acc.y = GRAVITY
        self.vel += self.acc
        self.vel.x *= FRICTION
        self.pos += self.vel
        self.acc *= 0

        # Floor collision
        if self.pos.y > SCREEN_HEIGHT - self.height - 50:
            self.pos.y = SCREEN_HEIGHT - self.height - 50
            self.vel.y = 0

        # Wall collision
        if self.pos.x < 0:
            self.pos.x = 0
            self.vel.x = 0
        elif self.pos.x > SCREEN_WIDTH - self.width:
            self.pos.x = SCREEN_WIDTH - self.width
            self.vel.x = 0

        self.rect.topleft = (self.pos.x, self.pos.y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
