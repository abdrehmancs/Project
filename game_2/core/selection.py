import pygame
from constants import *

class SelectionScreen:
    def __init__(self, game):
        self.game = game
        self.font_title = pygame.font.SysFont("Arial", 60, bold=True)
        self.font_label = pygame.font.SysFont("Arial", 30)

        self.p1_selection = "BALANCED"
        self.p2_selection = "BALANCED"

        self.archetypes = list(ARCHETYPES.keys())
        self.p1_index = 0
        self.p2_index = 1

    def draw(self, surface):
        surface.fill(MENU_COLOR)

        title = self.font_title.render("CHOOSE YOUR FIGHTER", True, WHITE)
        surface.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 100)))

        # Player 1 Section
        p1_label = self.font_label.render("Player 1", True, BLUE)
        surface.blit(p1_label, (SCREEN_WIDTH // 4 - 50, 200))
        self.draw_archetype_list(surface, self.p1_index, SCREEN_WIDTH // 4, 250)

        # Player 2 Section
        p2_label = self.font_label.render("Player 2", True, RED)
        surface.blit(p2_label, (3 * SCREEN_WIDTH // 4 - 50, 200))
        self.draw_archetype_list(surface, self.p2_index, 3 * SCREEN_WIDTH // 4, 250)

        # Start Button
        self.start_btn_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 150, 200, 60)
        pygame.draw.rect(surface, BUTTON_COLOR, self.start_btn_rect, border_radius=10)
        start_text = self.font_label.render("READY! FIGHT!", True, WHITE)
        surface.blit(start_text, start_text.get_rect(center=self.start_btn_rect.center))

        instr = self.font_label.render("P1: A/D to switch | P2: Left/Right to switch", True, GRAY)
        surface.blit(instr, instr.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)))

    def draw_archetype_list(self, surface, index, x, y):
        for i, arch in enumerate(self.archetypes):
            color = SELECT_COLOR if i == index else BUTTON_COLOR
            rect = pygame.Rect(x - 100, y + i * 70, 200, 50)
            pygame.draw.rect(surface, color, rect, border_radius=5)

            text = self.font_label.render(arch, True, WHITE)
            surface.blit(text, text.get_rect(center=rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            # Optional: add hover effect for mouse selection
            pass

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            # Check P1 list
            for i in range(len(self.archetypes)):
                rect = pygame.Rect(SCREEN_WIDTH // 4 - 100, 250 + i * 70, 200, 50)
                if rect.collidepoint(mouse_pos):
                    self.p1_index = i
                    self.p1_selection = self.archetypes[i]

            # Check P2 list
            for i in range(len(self.archetypes)):
                rect = pygame.Rect(3 * SCREEN_WIDTH // 4 - 100, 250 + i * 70, 200, 50)
                if rect.collidepoint(mouse_pos):
                    self.p2_index = i
                    self.p2_selection = self.archetypes[i]

            # Check Start Button
            if hasattr(self, 'start_btn_rect') and self.start_btn_rect.collidepoint(mouse_pos):
                return "START"

        if event.type == pygame.KEYDOWN:
            # Keep keyboard controls for accessibility
            if event.key == pygame.K_a:
                self.p1_index = (self.p1_index - 1) % len(self.archetypes)
                self.p1_selection = self.archetypes[self.p1_index]
            elif event.key == pygame.K_d:
                self.p1_index = (self.p1_index + 1) % len(self.archetypes)
                self.p1_selection = self.archetypes[self.p1_index]
            elif event.key == pygame.K_w:
                self.p1_selection = self.archetypes[self.p1_index]

            if event.key == pygame.K_LEFT:
                self.p2_index = (self.p2_index - 1) % len(self.archetypes)
                self.p2_selection = self.archetypes[self.p2_index]
            elif event.key == pygame.K_RIGHT:
                self.p2_index = (self.p2_index + 1) % len(self.archetypes)
                self.p2_selection = self.archetypes[self.p2_index]
            elif event.key == pygame.K_UP:
                self.p2_selection = self.archetypes[self.p2_index]
            elif event.key == pygame.K_RETURN:
                return "START"

        return None
