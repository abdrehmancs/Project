import pygame
import random
from constants import *

class Particle:
    def __init__(self, x, y, color):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(random.uniform(-5, 5), random.uniform(-5, 5))
        self.life = 255
        self.color = color

    def update(self):
        self.pos += self.vel
        self.life -= 10

    def draw(self, surface):
        if self.life > 0:
            # Create a surface with alpha for the particle
            s = pygame.Surface((4, 4))
            s.set_alpha(self.life)
            s.fill(self.color)
            surface.blit(s, self.pos)

class EffectManager:
    def __init__(self):
        self.particles = []
        self.screen_shake = 0

    def add_hit_effect(self, x, y, color=YELLOW):
        for _ in range(15):
            self.particles.append(Particle(x, y, color))
        self.screen_shake = 10

    def update(self):
        for p in self.particles[:]:
            p.update()
            if p.life <= 0:
                self.particles.remove(p)

        if self.screen_shake > 0:
            self.screen_shake -= 1

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)

    def get_shake_offset(self):
        if self.screen_shake > 0:
            return (random.randint(-self.screen_shake, self.screen_shake),
                    random.randint(-self.screen_shake, self.screen_shake))
        return (0, 0)
