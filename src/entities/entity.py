"""Base class shared by every living thing on the board (plants & zombies)."""

from abc import ABC, abstractmethod


class Entity(ABC):
    def __init__(self, hp):
        self.max_hp = hp
        self.hp = hp
        self.alive = True

    def take_damage(self, amount):
        if not self.alive:
            return
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.alive = False

    @property
    def hp_ratio(self):
        return max(0.0, self.hp / self.max_hp)

    @abstractmethod
    def update(self, dt, game):
        """Advance this entity's state by dt seconds."""
        raise NotImplementedError

    @abstractmethod
    def draw(self, surface):
        raise NotImplementedError
