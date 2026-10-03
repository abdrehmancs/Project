import pygame
from constants import *
from entities.fighter import Fighter
from core.engine import EffectManager
from core.sound_manager import SoundManager
from entities.ai import AIPlayer
from core.stage import Stage
from core.menu import Menu
from core.selection import SelectionScreen

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mighty Clash 2D")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.winner = None
        self.state = "MENU" # Added state management: MENU, SELECT, PLAYING, GAME_OVER

        # Stage
        self.stage = Stage()

        # Entities - Initialized as None, created after selection
        self.player1 = None
        self.player2 = None
        self.fighters = []
        self.effects = EffectManager()
        self.sound_manager = SoundManager()

        # AI Logic
        self.ai_enabled = True # Toggle this to switch between PVP and PVE
        self.ai_player2 = None

        # UI Managers
        self.menu = Menu(self)
        self.selection = SelectionScreen(self)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.state == "MENU":
                action = self.menu.handle_event(event)
                if action == "start":
                    self.state = "SELECT"
                elif action == "pvp":
                    self.state = "SELECT"
                    self.ai_enabled = False
                elif action == "exit":
                    self.running = False

            elif self.state == "SELECT":
                action = self.selection.handle_event(event)
                if action == "START":
                    self.start_match()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.start_match()

            elif self.state == "PLAYING":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "MENU"

            elif self.state == "GAME_OVER":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.reset_game()
                        self.state = "MENU"

    def update(self):
        if self.state != "PLAYING":
            return

        # Stage Update
        self.stage.update()

        # AI Update
        if self.ai_enabled and self.ai_player2:
            self.ai_player2.update(self.player1)

        for f in self.fighters:
            # Only handle input for players NOT controlled by AI
            if f == self.player2 and self.ai_enabled:
                pass
            else:
                f.handle_input(self.sound_manager)
            f.update()

        self.effects.update()

        # Combat collision
        for attacker in self.fighters:
            attack_rect = attacker.get_attack_rect()
            if attack_rect:
                for target in self.fighters:
                    if attacker != target and attack_rect.colliderect(target.rect):
                        # Calculate damage with combo multiplier
                        multiplier = 1.0 + (attacker.combo_count * COMBO_MULTIPLIER_STEP)

                        if attacker.attack_type == "LIGHT":
                            base_damage = 5 * multiplier
                            meter_gain = 5
                        elif attacker.attack_type == "HEAVY":
                            base_damage = 15 * multiplier
                            meter_gain = 10
                        elif attacker.attack_type == "SUPER":
                            # Use archetype-specific super stats
                            arch_stats = ARCHETYPES[attacker.archetype]
                            base_damage = arch_stats["special_damage"] * multiplier
                            meter_gain = 0
                            knockback = arch_stats["special_knockback"]
                        else:
                            base_damage = 0
                            meter_gain = 0
                            knockback = 0

                        if attacker.attack_type != "SUPER":
                            knockback = attacker.direction * (1.0 if attacker.attack_type == "LIGHT" else 1.5)

                        # Defense Logic
                        if target.is_blocking:
                            final_damage = base_damage * BLOCK_REDUCTION
                            final_knockback = knockback * 0.2
                        else:
                            final_damage = base_damage
                            final_knockback = knockback

                        target.take_damage(final_damage, final_knockback)
                        attacker.super_meter = min(SUPER_METER_MAX, attacker.super_meter + meter_gain)

                        self.effects.add_hit_effect(target.pos.x + target.width//2, target.pos.y + 50)

                        # Play sound based on attack type
                        sound_key = 'hit_light' if attacker.attack_type == "LIGHT" else 'hit_heavy'
                        self.sound_manager.play(sound_key)

                        # Prevent multiple hits per attack
                        attacker.is_attacking = False
                        attacker.attack_timer = 0

        # Check for game over
        if self.player1 and self.player2:
            if self.player1.health <= 0:
                self.state = "GAME_OVER"
                self.winner = "Player 2"
            elif self.player2.health <= 0:
                self.state = "GAME_OVER"
                self.winner = "Player 1"

    def draw(self):
        if self.state == "MENU":
            self.menu.draw(self.screen)
            pygame.display.flip()
            return

        if self.state == "SELECT":
            self.selection.draw(self.screen)
            pygame.display.flip()
            return

        shake_x, shake_y = self.effects.get_shake_offset()

        # Draw Stage ( Background )
        self.stage.draw(self.screen)

        # Draw Fighters
        for f in self.fighters:
            original_pos = f.rect.topleft
            f.rect.x += shake_x
            f.rect.y += shake_y
            f.draw(self.screen)
            f.rect.topleft = original_pos

        # Draw Effects
        self.effects.draw(self.screen)

        # Draw UI
        self.draw_ui()

        # Game Over Overlay
        if self.state == "GAME_OVER":
            self.draw_game_over()

        pygame.display.flip()

    def reset_game(self):
        # Return to menu and clear entities
        self.player1 = None
        self.player2 = None
        self.fighters = []
        self.ai_player2 = None

    def start_match(self):
        # Instantiate fighters based on selection
        self.player1 = Fighter(200, 400, self.selection.p1_selection, 1)
        self.player2 = Fighter(1000, 400, self.selection.p2_selection, 2)
        self.fighters = [self.player1, self.player2]

        if self.ai_enabled:
            self.ai_player2 = AIPlayer(self.player2)
        else:
            self.ai_player2 = None

        self.state = "PLAYING"

    def draw_ui(self):
        # Health Bars
        p1_bar_width = (self.player1.health / self.player1.max_health) * 400
        p2_bar_width = (self.player2.health / self.player2.max_health) * 400

        # Player 1 Bar (Top Left)
        pygame.draw.rect(self.screen, GRAY, (50, 50, 400, 30))
        pygame.draw.rect(self.screen, BLUE, (50, 50, p1_bar_width, 30))

        # Player 2 Bar (Top Right)
        pygame.draw.rect(self.screen, GRAY, (SCREEN_WIDTH - 450, 50, 400, 30))
        pygame.draw.rect(self.screen, RED, (SCREEN_WIDTH - 450 - (400 - p2_bar_width), 50, p2_bar_width, 30))

        # Super Meters
        p1_super_width = (self.player1.super_meter / SUPER_METER_MAX) * 300
        p2_super_width = (self.player2.super_meter / SUPER_METER_MAX) * 300

        pygame.draw.rect(self.screen, GRAY, (50, 90, 300, 15))
        pygame.draw.rect(self.screen, YELLOW, (50, 90, p1_super_width, 15))

        pygame.draw.rect(self.screen, GRAY, (SCREEN_WIDTH - 350, 90, 300, 15))
        pygame.draw.rect(self.screen, YELLOW, (SCREEN_WIDTH - 350 + (300 - p2_super_width), 90, p2_super_width, 15))

    def draw_game_over(self):
        # Simple overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        font = pygame.font.SysFont("Arial", 72, bold=True)
        text = font.render(f"{self.winner} WINS!", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)

        sub_font = pygame.font.SysFont("Arial", 32)
        sub_text = sub_font.render("Press ESC to Return to Menu", True, WHITE)
        sub_text_rect = sub_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(sub_text, sub_text_rect)


    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
