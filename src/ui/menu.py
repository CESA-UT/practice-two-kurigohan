"""Full-screen overlays: start menu, pause menu, win/lose end screen."""

import pygame

from .. import constants as C
from ..assets import load_image


def _button(surface, rect, label, font, mouse_pos):
    hovered = rect.collidepoint(mouse_pos)
    color = (110, 170, 90) if hovered else (80, 130, 65)
    pygame.draw.rect(surface, color, rect, border_radius=10)
    pygame.draw.rect(surface, (30, 60, 20), rect, width=3, border_radius=10)
    text = font.render(label, True, C.COLOR_TEXT)
    surface.blit(text, text.get_rect(center=rect.center))


class StartMenu:
    def __init__(self):
        self.title_font = pygame.font.SysFont("arial", 54, bold=True)
        self.button_font = pygame.font.SysFont("arial", 30, bold=True)
        self.play_rect = pygame.Rect(0, 0, 220, 70)
        self.play_rect.center = (C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT // 2 + 60)
        self.background = load_image(C.IMG["frontyard"], size=(C.SCREEN_WIDTH, C.SCREEN_HEIGHT), alpha=False)

    def handle_click(self, pos):
        return "play" if self.play_rect.collidepoint(pos) else None

    def draw(self, surface, mouse_pos):
        surface.blit(self.background, (0, 0))
        dim = pygame.Surface((C.SCREEN_WIDTH, C.SCREEN_HEIGHT), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 90))
        surface.blit(dim, (0, 0))

        title = self.title_font.render("Plants vs Zombies", True, (255, 255, 255))
        shadow = self.title_font.render("Plants vs Zombies", True, (0, 0, 0))
        title_pos = title.get_rect(center=(C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT // 2 - 60))
        surface.blit(shadow, title_pos.move(3, 3))
        surface.blit(title, title_pos)

        subtitle_font = pygame.font.SysFont("arial", 20)
        subtitle = subtitle_font.render(
            "Advanced Programming - Practice 2", True, (230, 230, 230)
        )
        surface.blit(subtitle, subtitle.get_rect(center=(C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT // 2 - 10)))

        _button(surface, self.play_rect, "PLAY", self.button_font, mouse_pos)


class PauseMenu:
    def __init__(self):
        self.font_title = pygame.font.SysFont("arial", 44, bold=True)
        self.button_font = pygame.font.SysFont("arial", 26, bold=True)
        cx, cy = C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT // 2
        self.resume_rect = pygame.Rect(0, 0, 220, 60)
        self.resume_rect.center = (cx, cy + 10)
        self.restart_rect = pygame.Rect(0, 0, 220, 60)
        self.restart_rect.center = (cx, cy + 85)

    def handle_click(self, pos):
        if self.resume_rect.collidepoint(pos):
            return "resume"
        if self.restart_rect.collidepoint(pos):
            return "restart"
        return None

    def draw(self, surface, mouse_pos):
        dim = pygame.Surface((C.SCREEN_WIDTH, C.SCREEN_HEIGHT), pygame.SRCALPHA)
        dim.fill(C.COLOR_OVERLAY_BG)
        surface.blit(dim, (0, 0))

        title = self.font_title.render("Paused", True, (255, 255, 255))
        surface.blit(title, title.get_rect(center=(C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT // 2 - 70)))

        _button(surface, self.resume_rect, "Resume", self.button_font, mouse_pos)
        _button(surface, self.restart_rect, "Restart", self.button_font, mouse_pos)


class EndScreen:
    def __init__(self):
        self.font_title = pygame.font.SysFont("arial", 48, bold=True)
        self.button_font = pygame.font.SysFont("arial", 28, bold=True)
        self.win_icon = load_image(C.IMG["icon_win"], size=(90, 90))
        self.lose_icon = load_image(C.IMG["icon_lose"], size=(90, 90))
        self.restart_rect = pygame.Rect(0, 0, 240, 65)
        self.restart_rect.center = (C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT // 2 + 70)

    def handle_click(self, pos):
        return "restart" if self.restart_rect.collidepoint(pos) else None

    def draw(self, surface, mouse_pos, won):
        dim = pygame.Surface((C.SCREEN_WIDTH, C.SCREEN_HEIGHT), pygame.SRCALPHA)
        dim.fill(C.COLOR_OVERLAY_BG)
        surface.blit(dim, (0, 0))

        icon = self.win_icon if won else self.lose_icon
        icon_rect = icon.get_rect(center=(C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT // 2 - 90))
        surface.blit(icon, icon_rect)

        message = "You Win!" if won else "The Zombies Ate Your Brains!"
        color = (255, 230, 90) if won else (230, 90, 90)
        title = self.font_title.render(message, True, color)
        surface.blit(title, title.get_rect(center=(C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT // 2 - 20)))

        _button(surface, self.restart_rect, "Play Again", self.button_font, mouse_pos)
