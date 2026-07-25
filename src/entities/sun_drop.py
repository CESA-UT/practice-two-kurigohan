"""
Collectible Sun currency.

Two ways a Sun appears on the field (GameRules.md / SunFlower.md):
  * a "sky" sun that falls from the top of the screen at a random column
  * a sun produced by a SunFlower, which appears just above the plant

Either way, the player clicks it to collect its value before it expires.
"""

import random

from .. import constants as C
from ..assets import load_image


class SunDrop:
    def __init__(self, x, target_y, value, falling):
        self.x = x
        self.y = 0.0 if falling else target_y
        self.target_y = target_y
        self.value = value
        self.falling = falling
        self.lifetime = C.SUN_LIFETIME
        self.alive = True
        self.image = load_image(C.IMG["sun"], size=C.SUN_DISPLAY_SIZE)

    @classmethod
    def spawn_from_sky(cls):
        x = random.uniform(C.CELL_WIDTH * 0.5, C.SCREEN_WIDTH - C.CELL_WIDTH * 0.5)
        row = random.randint(0, C.BOARD_ROWS - 1)
        target_y = C.BOARD_ORIGIN_Y + row * C.CELL_HEIGHT + C.CELL_HEIGHT * 0.5
        return cls(x, target_y, C.SUN_VALUE, falling=True)

    @classmethod
    def spawn_from_plant(cls, x, y, value):
        return cls(x, y, value, falling=False)

    def get_rect(self):
        return self.image.get_rect(center=(self.x, self.y))

    def contains_point(self, px, py):
        return self.get_rect().collidepoint(px, py)

    def update(self, dt, game):
        if self.falling and self.y < self.target_y:
            self.y = min(self.target_y, self.y + C.SUN_FALL_SPEED * dt)
            if self.y >= self.target_y:
                self.falling = False
        else:
            self.lifetime -= dt
            if self.lifetime <= 0:
                self.alive = False

    def collect(self):
        self.alive = False
        return self.value

    def draw(self, surface):
        rect = self.get_rect()
        # fade out during the last two seconds so players get a visual warning
        if not self.falling and self.lifetime < 2.0:
            image = self.image.copy()
            alpha = max(0, int(255 * (self.lifetime / 2.0)))
            image.set_alpha(alpha)
            surface.blit(image, rect)
        else:
            surface.blit(self.image, rect)
