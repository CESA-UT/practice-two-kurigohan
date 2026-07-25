"""
WaveManager - schedules zombie spawns according to Waves.md.

Uses the "minimum acceptable" wave table: 3 waves, 15 zombies total,
starting at 20s / 50s / 90s of play time. Zombies within a wave are
staggered a bit so they don't all appear stacked in the same instant.
"""

import random

from . import constants as C
from .assets import play_sound
from .entities.zombie import ZOMBIE_CLASSES


class WaveManager:
    def __init__(self, waves_config=None):
        self.waves = waves_config or C.WAVES
        self.elapsed = 0.0
        self.next_wave_index = 0
        self.pending_spawns = []
        self.spawn_timer = 0.0
        self.total_zombies = sum(w["count"] for w in self.waves)
        self.spawned_count = 0
        self.current_wave_number = 0

    @property
    def all_zombies_spawned(self):
        return self.next_wave_index >= len(self.waves) and not self.pending_spawns

    def update(self, dt, game):
        self.elapsed += dt

        if self.next_wave_index < len(self.waves):
            wave = self.waves[self.next_wave_index]
            if self.elapsed >= wave["start_time"]:
                self._start_wave(wave, game)

        if self.pending_spawns:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                self._spawn_one(game)

    def _start_wave(self, wave, game):
        self.current_wave_number += 1
        self.pending_spawns.extend([wave["type"]] * wave["count"])
        self.spawn_timer = 0.0
        self.next_wave_index += 1
        game.hud.show_wave_banner(f"Wave {self.current_wave_number} incoming!")
        play_sound(game.sounds.get("wave_incoming"), volume=0.7)

    def _spawn_one(self, game):
        zombie_type = self.pending_spawns.pop(0)
        row = random.randint(0, C.BOARD_ROWS - 1)
        zombie = ZOMBIE_CLASSES[zombie_type](row, game.board)
        game.zombies.append(zombie)
        self.spawned_count += 1
        self.spawn_timer = C.WAVE_SPAWN_STAGGER
        play_sound(game.sounds.get("groan"), volume=0.25)
