"""
Plants: PeaShooter, SunFlower, WallNut.

Numbers are taken from docs/characters/PeaShooter.md, SunFlower.md and
WallNut.md. Each subclass only implements the behaviour that is specific
to it; shared bookkeeping (hp, position, drawing the current animation
frame) lives in the Plant base class.
"""

from .. import constants as C
from ..assets import AnimatedSprite
from .entity import Entity
from .projectile import Pea
from .sun_drop import SunDrop


class Plant(Entity):
    plant_type = None  # overridden by subclasses

    def __init__(self, row, col, board):
        config = C.PLANT_CONFIG[self.plant_type]
        super().__init__(config["hp"])
        self.row = row
        self.col = col
        self.board = board
        self.config = config
        self.x, self.y = board.cell_center(row, col)
        self.sprite = self._build_sprite()

    def _build_sprite(self):
        raise NotImplementedError

    def update(self, dt, game):
        self.sprite.update(dt)

    def draw(self, surface):
        image = self.sprite.image
        rect = image.get_rect(center=(self.x, self.y))
        surface.blit(image, rect)


class PeaShooter(Plant):
    plant_type = "PeaShooter"

    def __init__(self, row, col, board):
        super().__init__(row, col, board)
        self.shoot_timer = 0.0

    def _build_sprite(self):
        return AnimatedSprite(C.IMG["plant_peashooter"], size=self.config["display_size"])

    def _zombie_ahead_exists(self, game):
        for zombie in game.zombies:
            if zombie.alive and zombie.row == self.row and zombie.col > self.col:
                return True
        return False

    def update(self, dt, game):
        super().update(dt, game)
        if not self._zombie_ahead_exists(game):
            # Nothing to shoot at: don't creep the timer up for no reason.
            self.shoot_timer = 0.0
            return

        self.shoot_timer += dt
        if self.shoot_timer >= self.config["shoot_interval"]:
            self.shoot_timer = 0.0
            pea = Pea(self.row, self.col + 0.6, self.config["damage"], game.board)
            game.projectiles.append(pea)


class SunFlower(Plant):
    plant_type = "SunFlower"

    def __init__(self, row, col, board):
        super().__init__(row, col, board)
        self.produce_timer = 0.0
        self.first_produced = False

    def _build_sprite(self):
        return AnimatedSprite(C.IMG["plant_sunflower"], size=self.config["display_size"])

    def update(self, dt, game):
        super().update(dt, game)
        self.produce_timer += dt
        threshold = self.config["first_sun_delay"] if not self.first_produced else self.config["sun_interval"]
        if self.produce_timer >= threshold:
            self.produce_timer = 0.0
            self.first_produced = True
            drop = SunDrop.spawn_from_plant(self.x, self.y - 20, self.config["sun_value"])
            game.suns.append(drop)


class WallNut(Plant):
    plant_type = "WallNut"

    def _build_sprite(self):
        self.healthy_sprite = AnimatedSprite(C.IMG["plant_wallnut"], size=self.config["display_size"])
        self.dying_sprite = AnimatedSprite(C.IMG["plant_wallnut_dying"], size=self.config["display_size"])
        return self.healthy_sprite

    def update(self, dt, game):
        # Switch to the cracked/dying animation once badly hurt (visual only,
        # WallNut.md marks the damaged-state art as optional).
        active = self.dying_sprite if self.hp_ratio < 0.35 else self.healthy_sprite
        active.update(dt)
        self.sprite = active


PLANT_CLASSES = {
    "PeaShooter": PeaShooter,
    "SunFlower": SunFlower,
    "WallNut": WallNut,
}
