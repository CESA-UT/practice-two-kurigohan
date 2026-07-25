"""
LawnMower - optional defensive tool (docs/characters/LawnMower.md).

One per row, sitting at the left edge. The first time a zombie reaches the
left edge of its row, the row's mower (if unused) wipes every zombie in
that row and then trundles off-screen. If a zombie reaches the edge again
after the mower has already been used, the player loses (handled in Game).
"""

from .. import constants as C
from ..assets import AnimatedSprite, load_image, play_sound


class LawnMower:
    SPEED_CELLS_PER_SEC = 5.0

    def __init__(self, row, board):
        self.row = row
        self.board = board
        self.state = "idle"  # idle -> active -> done
        self.col = -0.4  # sits just to the left of the playable board
        self.idle_image = load_image(C.IMG["lawnmower_idle"], size=(70, 70))
        self.active_sprite = AnimatedSprite(C.IMG["lawnmower_active"], size=(70, 70))

    @property
    def used(self):
        return self.state != "idle"

    def activate(self, game):
        if self.state != "idle":
            return
        self.state = "active"
        for zombie in game.zombies:
            if zombie.alive and zombie.row == self.row:
                zombie.alive = False
        play_sound(game.sounds.get("lawnmower"), volume=0.7)

    def update(self, dt, game):
        if self.state != "active":
            return
        self.active_sprite.update(dt)
        self.col += self.SPEED_CELLS_PER_SEC * dt
        if self.col > C.BOARD_COLS + 1:
            self.state = "done"

    @property
    def visible(self):
        return self.state in ("idle", "active")

    def draw(self, surface):
        if self.state == "done":
            return
        x = self.board.col_to_x(self.col) + 20
        y = self.board.row_center_y(self.row)
        image = self.active_sprite.image if self.state == "active" else self.idle_image
        rect = image.get_rect(center=(x, y))
        surface.blit(image, rect)
