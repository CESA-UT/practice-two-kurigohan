"""Top HUD strip: sun counter, plant cards, shovel tool, pause button."""

import pygame

from .. import constants as C
from ..assets import load_image
from .card import CardBar, CARD_SIZE


class HUD:
    def __init__(self):
        self.card_bar = CardBar(origin=(16, (C.HUD_HEIGHT - CARD_SIZE[1]) // 2))

        self.font_big = pygame.font.SysFont("arial", 26, bold=True)
        self.font_med = pygame.font.SysFont("arial", 18, bold=True)

        self.sun_icon = load_image(C.IMG["sun"], size=(44, 44))
        cards_right_edge = self.card_bar.cards[-1].rect.right
        self.sun_icon_pos = (cards_right_edge + 24, C.HUD_HEIGHT // 2 - 22)

        self.shovel_image = load_image(C.IMG["shovel"], size=(52, 52))
        self.shovel_rect = pygame.Rect(0, 0, 66, 66)
        self.shovel_rect.center = (C.SCREEN_WIDTH - 130, C.HUD_HEIGHT // 2)
        self.shovel_selected = False

        self.pause_icon = load_image(C.IMG["icon_menu"], size=(30, 30))
        self.pause_rect = pygame.Rect(0, 0, 50, 50)
        self.pause_rect.center = (C.SCREEN_WIDTH - 40, C.HUD_HEIGHT // 2)

        self.wave_banner_text = ""
        self.wave_banner_timer = 0.0

    def show_wave_banner(self, text, duration=3.0):
        self.wave_banner_text = text
        self.wave_banner_timer = duration

    def update(self, dt):
        self.card_bar.update(dt)
        if self.wave_banner_timer > 0:
            self.wave_banner_timer -= dt

    def handle_click(self, pos, sun_count):
        """Returns an action string: 'pause', 'shovel', 'card', or None."""
        if self.pause_rect.collidepoint(pos):
            return "pause"

        if self.shovel_rect.collidepoint(pos):
            self.shovel_selected = not self.shovel_selected
            if self.shovel_selected:
                self.card_bar.clear_selection()
            return "shovel"

        if self.card_bar.handle_click(pos, sun_count):
            if self.card_bar.selected_index is not None:
                self.shovel_selected = False
            return "card"

        return None

    def draw(self, surface, sun_count):
        pygame.draw.rect(surface, C.COLOR_HUD_BG, (0, 0, C.SCREEN_WIDTH, C.HUD_HEIGHT))
        pygame.draw.rect(surface, C.COLOR_HUD_BORDER, (0, C.HUD_HEIGHT - 4, C.SCREEN_WIDTH, 4))

        self.card_bar.draw(surface, sun_count)

        surface.blit(self.sun_icon, self.sun_icon_pos)
        sun_label = self.font_big.render(str(int(sun_count)), True, C.COLOR_TEXT)
        surface.blit(sun_label, (self.sun_icon_pos[0] + 50, self.sun_icon_pos[1] + 10))

        shovel_bg = (C.COLOR_SHOVEL_SELECTED if self.shovel_selected else (90, 65, 40))
        pygame.draw.rect(surface, shovel_bg, self.shovel_rect, border_radius=8)
        shovel_img_rect = self.shovel_image.get_rect(center=self.shovel_rect.center)
        surface.blit(self.shovel_image, shovel_img_rect)

        pygame.draw.rect(surface, (90, 65, 40), self.pause_rect, border_radius=8)
        pause_img_rect = self.pause_icon.get_rect(center=self.pause_rect.center)
        surface.blit(self.pause_icon, pause_img_rect)

        if self.wave_banner_timer > 0 and self.wave_banner_text:
            alpha = 255 if self.wave_banner_timer > 0.5 else int(255 * (self.wave_banner_timer / 0.5))
            label = self.font_big.render(self.wave_banner_text, True, (255, 230, 90))
            label.set_alpha(alpha)
            rect = label.get_rect(center=(C.SCREEN_WIDTH // 2, C.HUD_HEIGHT + 26))
            bg_rect = rect.inflate(24, 12)
            bg = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
            bg.fill((0, 0, 0, min(160, alpha)))
            surface.blit(bg, bg_rect.topleft)
            surface.blit(label, rect)
