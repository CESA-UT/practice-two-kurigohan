"""Plant selection cards shown along the top of the screen."""

import pygame

from .. import constants as C
from ..assets import load_image

_CARD_IMG_KEY = {
    "PeaShooter": "card_peashooter",
    "SunFlower": "card_sunflower",
    "WallNut": "card_wallnut",
}

CARD_SIZE = (86, 100)


class Card:
    def __init__(self, plant_type, topleft):
        self.plant_type = plant_type
        config = C.PLANT_CONFIG[plant_type]
        self.cost = config["cost"]
        self.cooldown_max = config["card_cooldown"]
        self.cooldown_remaining = 0.0
        self.rect = pygame.Rect(topleft, CARD_SIZE)
        self.image = load_image(C.IMG[_CARD_IMG_KEY[plant_type]], size=CARD_SIZE)
        self.font = pygame.font.SysFont("arial", 16, bold=True)

    @property
    def ready(self):
        return self.cooldown_remaining <= 0.0

    def can_afford(self, sun_count):
        return sun_count >= self.cost

    def is_usable(self, sun_count):
        return self.ready and self.can_afford(sun_count)

    def trigger_cooldown(self):
        self.cooldown_remaining = self.cooldown_max

    def update(self, dt):
        if self.cooldown_remaining > 0:
            self.cooldown_remaining = max(0.0, self.cooldown_remaining - dt)

    def draw(self, surface, sun_count, selected):
        surface.blit(self.image, self.rect.topleft)

        if not self.can_afford(sun_count):
            tint = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            tint.fill((0, 0, 0, 120))
            surface.blit(tint, self.rect.topleft)

        if not self.ready:
            frac = self.cooldown_remaining / self.cooldown_max
            overlay_h = int(self.rect.height * frac)
            overlay = pygame.Surface((self.rect.width, overlay_h), pygame.SRCALPHA)
            overlay.fill(C.COLOR_CARD_LOCKED)
            surface.blit(overlay, (self.rect.x, self.rect.y))

        cost_label = self.font.render(str(self.cost), True, C.COLOR_TEXT)
        cost_bg_rect = cost_label.get_rect(bottomleft=(self.rect.x + 2, self.rect.bottom - 2))
        surface.blit(cost_label, cost_bg_rect)

        pygame.draw.rect(surface, (20, 20, 20), self.rect, width=2, border_radius=4)
        if selected:
            pygame.draw.rect(surface, C.COLOR_CARD_SELECTED, self.rect, width=3, border_radius=4)


class CardBar:
    def __init__(self, plant_order=None, origin=(16, 8)):
        plant_order = plant_order or C.PLANT_ORDER
        self.cards = []
        x, y = origin
        for plant_type in plant_order:
            self.cards.append(Card(plant_type, (x, y)))
            x += CARD_SIZE[0] + 10
        self.selected_index = None

    @property
    def selected_card(self):
        if self.selected_index is None:
            return None
        return self.cards[self.selected_index]

    def clear_selection(self):
        self.selected_index = None

    def update(self, dt):
        for card in self.cards:
            card.update(dt)

    def handle_click(self, pos, sun_count):
        """Returns True if the click was consumed by a card."""
        for index, card in enumerate(self.cards):
            if card.rect.collidepoint(pos):
                if card.is_usable(sun_count):
                    self.selected_index = None if self.selected_index == index else index
                return True
        return False

    def draw(self, surface, sun_count):
        for index, card in enumerate(self.cards):
            card.draw(surface, sun_count, selected=(index == self.selected_index))
