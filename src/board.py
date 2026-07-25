"""
Board / Lawn representation.

The lawn is a logical 5x9 grid laid over Frontyard.png (GameRules.md).
Drawing grid lines on top of the image is optional and we don't do it,
but every plant-placement / collision decision in the game is expressed
in terms of this grid.
"""

import pygame

from . import constants as C
from .assets import load_image


class Cell:
    """A single grid cell. Holds at most one plant (GameRules.md)."""

    __slots__ = ("row", "col", "plant")

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.plant = None

    @property
    def is_empty(self):
        return self.plant is None


class Board:
    def __init__(self):
        self.rows = C.BOARD_ROWS
        self.cols = C.BOARD_COLS
        self.cells = [[Cell(r, c) for c in range(self.cols)] for r in range(self.rows)]
        self.background = load_image(C.IMG["frontyard"], size=C.LAWN_IMAGE_SIZE, alpha=False)

    # -- coordinate helpers --------------------------------------------------
    def cell_rect(self, row, col):
        x = C.BOARD_ORIGIN_X + col * C.CELL_WIDTH
        y = C.BOARD_ORIGIN_Y + row * C.CELL_HEIGHT
        return pygame.Rect(x, y, C.CELL_WIDTH, C.CELL_HEIGHT)

    def cell_center(self, row, col):
        rect = self.cell_rect(row, col)
        return rect.centerx, rect.centery

    def col_to_x(self, col):
        """Continuous column (float) -> pixel x of that column's left edge."""
        return C.BOARD_ORIGIN_X + col * C.CELL_WIDTH

    def row_center_y(self, row):
        return C.BOARD_ORIGIN_Y + row * C.CELL_HEIGHT + C.CELL_HEIGHT / 2

    def pixel_to_cell(self, x, y):
        """Return (row, col) for a screen pixel, or None if outside the lawn."""
        if y < C.BOARD_ORIGIN_Y or y >= C.BOARD_ORIGIN_Y + C.LAWN_IMAGE_SIZE[1]:
            return None
        if x < C.BOARD_ORIGIN_X or x >= C.BOARD_ORIGIN_X + C.LAWN_IMAGE_SIZE[0]:
            return None
        col = int((x - C.BOARD_ORIGIN_X) // C.CELL_WIDTH)
        row = int((y - C.BOARD_ORIGIN_Y) // C.CELL_HEIGHT)
        row = max(0, min(self.rows - 1, row))
        col = max(0, min(self.cols - 1, col))
        return row, col

    # -- plant bookkeeping ----------------------------------------------------
    def get_plant(self, row, col):
        return self.cells[row][col].plant

    def is_empty(self, row, col):
        return self.cells[row][col].is_empty

    def place_plant(self, row, col, plant):
        self.cells[row][col].plant = plant

    def remove_plant(self, row, col):
        self.cells[row][col].plant = None

    def plant_at_nearest_col(self, row, col):
        """Plant occupying the given integer column in a row, if any."""
        if 0 <= col < self.cols:
            return self.cells[row][col].plant
        return None

    def all_plants(self):
        for row in self.cells:
            for cell in row:
                if cell.plant is not None:
                    yield cell.plant

    # -- drawing ---------------------------------------------------------------
    def draw(self, surface, hover_cell=None):
        surface.blit(self.background, (C.BOARD_ORIGIN_X, C.BOARD_ORIGIN_Y))
        if hover_cell is not None:
            row, col = hover_cell
            if self.is_empty(row, col):
                rect = self.cell_rect(row, col)
                hl = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                hl.fill(C.COLOR_GRID_HOVER)
                surface.blit(hl, rect.topleft)
