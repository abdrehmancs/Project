import pygame
from constants import *

class Menu:
    def __init__(self, game):
        self.game = game
        self.font_title = pygame.font.SysFont("Arial", 80, bold=True)
        self.font_button = pygame.font.SysFont("Arial", 40)
        self.buttons = [
            {"label": "START GAME", "action": "start"},
            {"label": "PVP MODE", "action": "pvp"},
            {"label": "EXIT", "action": "exit"}
        ]
        self.hovered_button = None

    def draw(self, surface):
        surface.fill(MENU_COLOR)

        # Draw Title
        title_text = self.font_title.render("MIGHTY CLASH 2D", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        surface.blit(title_text, title_rect)

        # Draw Buttons
        for i, btn in enumerate(self.buttons):
            color = BUTTON_HOVER_COLOR if self.hovered_button == i else BUTTON_COLOR
            rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 300 + i * 80, 400, 60)
            pygame.draw.rect(surface, color, rect, border_radius=10)

            text = self.font_button.render(btn["label"], True, WHITE)
            text_rect = text.get_rect(center=rect.center)
            surface.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered_button = None
            for i, btn in enumerate(self.buttons):
                rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 300 + i * 80, 400, 60)
                if rect.collidepoint(event.pos):
                    self.hovered_button = i

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered_button is not None:
                action = self.buttons[self.hovered_button]["action"]
                return action
        return None
