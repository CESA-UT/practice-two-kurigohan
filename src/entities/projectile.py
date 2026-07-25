"""Projectile fired by PeaShooter (GameRules.md: peas travel left -> right)."""

from .. import constants as C
from ..assets import load_image, play_sound


class Pea:
    def __init__(self, row, col, damage, board):
        self.row = row
        self.col = col  # continuous position, in cell units
        self.damage = damage
        self.board = board
        self.speed = C.PEA_SPEED_CELLS_PER_SEC
        self.alive = True
        self.image = load_image(C.IMG["pea"], size=C.PEA_DISPLAY_SIZE)

    @property
    def x(self):
        return self.board.col_to_x(self.col)

    @property
    def y(self):
        return self.board.row_center_y(self.row)

    def update(self, dt, game):
        self.col += self.speed * dt
        if self.col > C.BOARD_COLS + 1:
            self.alive = False
            return

        for zombie in game.zombies:
            if zombie.alive and zombie.row == self.row and abs(zombie.col - self.col) < 0.3:
                zombie.take_damage(self.damage)
                self.alive = False
                play_sound(game.sounds.get("splat"), volume=0.4)
                break

    def draw(self, surface):
        rect = self.image.get_rect(center=(self.x, self.y))
        surface.blit(self.image, rect)
