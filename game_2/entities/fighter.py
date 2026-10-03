import pygame
from constants import *
from entities.entity import Entity

class Fighter(Entity):
    def __init__(self, x, y, archetype_name, player_num=1):
        # Load archetype stats
        stats = ARCHETYPES[archetype_name]
        width, height = stats["size"]
        color = stats["color"]

        super().__init__(x, y, width, height, color)

        self.archetype = archetype_name
        self.player_num = player_num
        self.health = stats["health"]
        self.max_health = stats["health"]
        self.speed = stats["speed"]
        self.jump_force = stats["jump"]
        self.damage_mod = stats["damage_mod"]

        self.super_meter = 0
        self.state = "IDLE"
        self.direction = 1 if player_num == 1 else -1
        self.is_attacking = False
        self.attack_type = None
        self.attack_timer = 0
        self.hit_stun = 0
        self.combo_count = 0
        self.last_attack_time = 0

        # Defense states
        self.is_blocking = False
        self.block_timer = 0

        # Input mapping
        self.controls = {
            1: {'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w, 'attack': pygame.K_f, 'special': pygame.K_g, 'block': pygame.K_s},
            2: {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'jump': pygame.K_UP, 'attack': pygame.K_l, 'special': pygame.K_k, 'block': pygame.K_DOWN}
        }[player_num]

    def handle_input(self, sound_manager=None):
        if self.hit_stun > 0:
            return

        keys = pygame.key.get_pressed()

        # Blocking
        if keys[self.controls['block']]:
            self.is_blocking = True
            self.state = "BLOCKING"
            self.vel.x = 0
        else:
            self.is_blocking = False

        if self.is_blocking:
            return # Cannot move or attack while blocking

        # Movement
        if keys[self.controls['left']]:
            self.vel.x = -self.speed
            self.direction = -1
            self.state = "WALKING"
        elif keys[self.controls['right']]:
            self.vel.x = self.speed
            self.direction = 1
            self.state = "WALKING"
        else:
            self.state = "IDLE"

        # Jump
        if keys[self.controls['jump']] and self.pos.y >= SCREEN_HEIGHT - self.height - 51:
            self.vel.y = self.jump_force
            self.state = "JUMPING"
            if sound_manager:
                sound_manager.play('jump')

        # Combo System Check
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time > COMBO_WINDOW:
            self.combo_count = 0

        # Attack
        if keys[self.controls['attack']] and not self.is_attacking:
            self.attack("LIGHT", sound_manager)

        if keys[self.controls['special']] and not self.is_attacking:
            if self.super_meter >= SUPER_COST_SPECIAL:
                self.attack("SUPER", sound_manager)
            else:
                self.attack("HEAVY", sound_manager)

    def attack(self, type, sound_manager=None):
        self.is_attacking = True
        self.attack_type = type

        if type == "LIGHT":
            self.attack_timer = 15
        elif type == "HEAVY":
            self.attack_timer = 30
        elif type == "SUPER":
            self.attack_timer = 60
            self.super_meter -= SUPER_COST_SPECIAL
            if sound_manager:
                sound_manager.play('special')

        self.state = "ATTACKING"
        self.last_attack_time = pygame.time.get_ticks()
        self.combo_count += 1

    def update(self):
        if self.hit_stun > 0:
            self.hit_stun -= 1

        if self.attack_timer > 0:
            self.attack_timer -= 1
        else:
            self.is_attacking = False

        super().update()

    def get_attack_rect(self):
        if not self.is_attacking:
            return None

        if self.attack_type == "LIGHT":
            width = 60
            height = 40
        elif self.attack_type == "HEAVY":
            width = 100
            height = 60
        elif self.attack_type == "SUPER":
            width = 200
            height = 100
        else:
            return None

        x = self.pos.x + self.width if self.direction == 1 else self.pos.x - width
        # The attack box now follows the character's current Y position (crucial for jumping attacks)
        y = self.pos.y + 20 if self.attack_type != "SUPER" else self.pos.y - 20

        return pygame.Rect(x, y, width, height)

    def take_damage(self, amount, knockback_dir):
        self.health -= amount
        self.hit_stun = 20
        self.vel.x = knockback_dir * KNOCKBACK_FORCE
        self.state = "HIT"
        if self.health < 0:
            self.health = 0

    def take_heavy_damage(self, amount, knockback_dir):
        self.health -= amount
        self.hit_stun = 40 # Double stun for heavy hits
        self.vel.x = knockback_dir * KNOCKBACK_SUPER
        self.state = "HIT"
        if self.health < 0:
            self.health = 0

    def draw(self, surface):
        # Change color based on state for better visual feedback
        current_color = self.color
        if self.state == "ATTACKING":
            current_color = YELLOW if self.attack_type == "SUPER" else WHITE
        elif self.state == "HIT":
            current_color = GRAY
        elif self.state == "BLOCKING":
            # Make the fighter a slightly darker version of their color or a distinct "shield" color
            current_color = (max(0, current_color[0]-50), max(0, current_color[1]-50), max(0, current_color[2]-50))

        # Draw the fighter body
        pygame.draw.rect(surface, current_color, self.rect)

        # Draw "Eyes" to show direction
        eye_x = self.rect.x + 10 if self.direction == -1 else self.rect.x + self.width - 20
        pygame.draw.rect(surface, BLACK, (eye_x, self.rect.y + 20, 10, 10))

