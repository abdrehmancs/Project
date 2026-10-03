import pygame
import random
from constants import *

class AIPlayer:
    def __init__(self, fighter):
        self.fighter = fighter

    def update(self, target):
        # Simple State Machine for AI
        dist = target.pos.x - self.fighter.pos.x
        abs_dist = abs(dist)

        # 1. Movement: Try to get within attack range
        if abs_dist > 100:
            if dist > 0:
                self.fighter.vel.x = WALK_SPEED
                self.fighter.direction = 1
                self.fighter.state = "WALKING"
            else:
                self.fighter.vel.x = -WALK_SPEED
                self.fighter.direction = -1
                self.fighter.state = "WALKING"
        elif abs_dist < 60:
            # Too close, back up a bit
            if dist > 0:
                self.fighter.vel.x = -WALK_SPEED
                self.fighter.direction = -1
            else:
                self.fighter.vel.x = WALK_SPEED
                self.fighter.direction = 1
        else:
            self.fighter.vel.x = 0
            self.fighter.state = "IDLE"

        # 2. Combat: Attack if in range
        if abs_dist < 120 and not self.fighter.is_attacking:
            # Randomly choose between Light and Heavy, or Super if available
            roll = random.random()
            if self.fighter.super_meter >= SUPER_COST_SPECIAL and roll < 0.1:
                self.fighter.attack("SUPER")
            elif roll < 0.4:
                self.fighter.attack("HEAVY")
            else:
                self.fighter.attack("LIGHT")

        # 3. Jump randomly to be annoying
        if random.random() < 0.01 and self.fighter.pos.y >= SCREEN_HEIGHT - self.fighter.height - 51:
            self.fighter.vel.y = JUMP_FORCE
