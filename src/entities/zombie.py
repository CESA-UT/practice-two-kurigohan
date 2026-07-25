"""
Zombies. Only NormalZombie is required (NormalZombie.md) but the base
class is written so extra zombie types from docs/characters can be added
later with only a config entry + subclass.
"""

import math

import pygame

from .. import constants as C
from ..assets import AnimatedSprite, play_sound
from .entity import Entity


class Zombie(Entity):
    zombie_type = None

    def __init__(self, row, board):
        config = C.ZOMBIE_CONFIG[self.zombie_type]
        super().__init__(config["hp"])
        self.row = row
        self.board = board
        self.config = config
        self.speed = config["speed"]  # cells / second
        self.eat_damage = config["eat_damage"]
        # Zombies enter from just off the right edge of the lawn.
        self.col = C.BOARD_COLS + 0.5
        self.state = "walking"
        self.target_plant = None
        self.walk_sprite = self._build_walk_sprite()
        self.eat_sprite = self._build_eat_sprite()

    def _build_walk_sprite(self):
        raise NotImplementedError

    def _build_eat_sprite(self):
        raise NotImplementedError

    @property
    def x(self):
        return self.board.col_to_x(self.col)

    @property
    def y(self):
        return self.board.row_center_y(self.row)

    def reached_house(self):
        return self.col <= 0.0

    def update(self, dt, game):
        cell_index = int(math.floor(self.col))
        plant = self.board.plant_at_nearest_col(self.row, cell_index) if cell_index >= 0 else None

        if plant is not None and plant.alive:
            if self.state != "eating":
                play_sound(game.sounds.get("chomp"), volume=0.35)
            self.state = "eating"
            self.target_plant = plant
            plant.take_damage(self.eat_damage * dt)
            if not plant.alive:
                self.board.remove_plant(self.row, cell_index)
                self.target_plant = None
                self.state = "walking"
        else:
            self.state = "walking"
            self.target_plant = None
            self.col -= self.speed * dt

        active_sprite = self.eat_sprite if self.state == "eating" else self.walk_sprite
        active_sprite.update(dt)

    def draw(self, surface):
        sprite = self.eat_sprite if self.state == "eating" else self.walk_sprite
        image = sprite.image
        rect = image.get_rect(midbottom=(self.x, self.y + self.config["display_size"][1] / 2))
        surface.blit(image, rect)

        # small HP bar so damage feedback is visible during play-testing/demo
        if self.hp < self.max_hp:
            bar_w, bar_h = 40, 5
            bg = pygame.Rect(0, 0, bar_w, bar_h)
            bg.midbottom = (rect.centerx, rect.top - 4)
            pygame.draw.rect(surface, (60, 0, 0), bg)
            fg = bg.copy()
            fg.width = int(bar_w * self.hp_ratio)
            pygame.draw.rect(surface, (0, 200, 0), fg)


class NormalZombie(Zombie):
    zombie_type = "NormalZombie"

    def _build_walk_sprite(self):
        return AnimatedSprite(C.IMG["zombie_normal_walk"], size=self.config["display_size"])

    def _build_eat_sprite(self):
        return AnimatedSprite(C.IMG["zombie_normal_eat"], size=self.config["display_size"])


ZOMBIE_CLASSES = {
    "NormalZombie": NormalZombie,
}
