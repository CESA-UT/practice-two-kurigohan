"""
Game - top level orchestrator.

Owns the pygame window/clock, the board, every live entity list, the HUD
and the menu overlays, and drives the classic update -> draw loop. This
is intentionally the only class that "knows about everything"; every
other class only needs the small slice of state relevant to it (which is
why plants/zombies/projectiles receive `game` as a parameter instead of
importing this module directly).
"""

import sys

import pygame

from . import constants as C
from .assets import load_sound, play_sound
from .board import Board
from .entities import PLANT_CLASSES, LawnMower, SunDrop
from .game_state import GameState
from .ui import HUD, StartMenu, PauseMenu, EndScreen
from .wave_manager import WaveManager


class Game:
    def __init__(self):
        pygame.init()
        try:
            pygame.mixer.init()
        except pygame.error:
            pass  # no audio device available - the game must still run

        pygame.display.set_caption(C.GAME_TITLE)
        self.screen = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.sounds = {key: load_sound(path) for key, path in C.SND.items()}

        self.board = Board()
        self.hud = HUD()
        self.start_menu = StartMenu()
        self.pause_menu = PauseMenu()
        self.end_screen = EndScreen()

        self.state = GameState.MENU
        self._init_round_state()

    # -- (re)initialisation ---------------------------------------------------
    def _init_round_state(self):
        self.sun_count = C.INITIAL_SUN
        self.plants = []
        self.zombies = []
        self.projectiles = []
        self.suns = []
        self.lawnmowers = [LawnMower(row, self.board) for row in range(C.BOARD_ROWS)]
        self.wave_manager = WaveManager()
        self.sky_sun_timer = C.SKY_SUN_INTERVAL / 2  # first sky sun a bit sooner

        for row in self.board.cells:
            for cell in row:
                cell.plant = None

        self.hud.card_bar.clear_selection()
        self.hud.shovel_selected = False
        for card in self.hud.card_bar.cards:
            card.cooldown_remaining = 0.0

    def start_new_game(self):
        self._init_round_state()
        self.state = GameState.PLAYING

    # -- main loop --------------------------------------------------------------
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(C.FPS) / 1000.0
            running = self._handle_events()
            self._update(dt)
            self._draw()
            pygame.display.flip()
        pygame.quit()
        sys.exit()

    # -- events -----------------------------------------------------------------
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                self._handle_key(event.key)
        return True

    def _handle_key(self, key):
        if key in (pygame.K_ESCAPE, pygame.K_p):
            if self.state == GameState.PLAYING:
                self.state = GameState.PAUSED
            elif self.state == GameState.PAUSED:
                self.state = GameState.PLAYING

    def _handle_click(self, pos):
        if self.state == GameState.MENU:
            if self.start_menu.handle_click(pos) == "play":
                self.start_new_game()

        elif self.state == GameState.PAUSED:
            action = self.pause_menu.handle_click(pos)
            if action == "resume":
                self.state = GameState.PLAYING
            elif action == "restart":
                self.start_new_game()

        elif self.state in (GameState.WIN, GameState.LOSE):
            if self.end_screen.handle_click(pos) == "restart":
                self.start_new_game()

        elif self.state == GameState.PLAYING:
            self._handle_playing_click(pos)

    def _handle_playing_click(self, pos):
        if pos[1] < C.HUD_HEIGHT:
            action = self.hud.handle_click(pos, self.sun_count)
            if action == "pause":
                self.state = GameState.PAUSED
            return

        # 1) collecting a sun takes priority over planting/shovel actions
        for sun in reversed(self.suns):
            if sun.contains_point(*pos):
                self.sun_count += sun.collect()
                return

        cell = self.board.pixel_to_cell(*pos)
        if cell is None:
            return
        row, col = cell

        if self.hud.shovel_selected:
            plant = self.board.get_plant(row, col)
            if plant is not None:
                self.board.remove_plant(row, col)
                if plant in self.plants:
                    self.plants.remove(plant)
            self.hud.shovel_selected = False
            return

        card = self.hud.card_bar.selected_card
        if card is not None and self.board.is_empty(row, col) and card.is_usable(self.sun_count):
            plant_cls = PLANT_CLASSES[card.plant_type]
            plant = plant_cls(row, col, self.board)
            self.board.place_plant(row, col, plant)
            self.plants.append(plant)
            self.sun_count -= card.cost
            card.trigger_cooldown()
            self.hud.card_bar.clear_selection()
            play_sound(self.sounds.get("plant"), volume=0.5)

    # -- update -------------------------------------------------------------------
    def _update(self, dt):
        if self.state != GameState.PLAYING:
            return

        self.hud.update(dt)

        self.sky_sun_timer += dt
        if self.sky_sun_timer >= C.SKY_SUN_INTERVAL:
            self.sky_sun_timer = 0.0
            self.suns.append(SunDrop.spawn_from_sky())

        for plant in list(self.plants):
            plant.update(dt, self)
            if not plant.alive:
                self.board.remove_plant(plant.row, plant.col)
                self.plants.remove(plant)

        for zombie in list(self.zombies):
            zombie.update(dt, self)
            if zombie.alive and zombie.reached_house():
                self._handle_zombie_reached_house(zombie)
            if not zombie.alive:
                self.zombies.remove(zombie)

        for pea in list(self.projectiles):
            pea.update(dt, self)
            if not pea.alive:
                self.projectiles.remove(pea)

        for sun in list(self.suns):
            sun.update(dt, self)
            if not sun.alive:
                self.suns.remove(sun)

        for mower in self.lawnmowers:
            mower.update(dt, self)

        self.wave_manager.update(dt, self)

        self._check_end_conditions()

    def _handle_zombie_reached_house(self, zombie):
        mower = self.lawnmowers[zombie.row]
        if not mower.used:
            mower.activate(self)  # wipes every zombie in this row, including this one
        else:
            self.state = GameState.LOSE
            play_sound(self.sounds.get("brainz"), volume=0.7)

    def _check_end_conditions(self):
        if self.state != GameState.PLAYING:
            return
        if self.wave_manager.all_zombies_spawned and not self.zombies:
            self.state = GameState.WIN

    # -- draw -----------------------------------------------------------------------
    def _hover_cell(self):
        if self.hud.card_bar.selected_card is None:
            return None
        return self.board.pixel_to_cell(*pygame.mouse.get_pos())

    def _draw(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.state == GameState.MENU:
            self.start_menu.draw(self.screen, mouse_pos)
            return

        self.board.draw(self.screen, hover_cell=self._hover_cell())
        for plant in self.plants:
            plant.draw(self.screen)
        for zombie in self.zombies:
            zombie.draw(self.screen)
        for pea in self.projectiles:
            pea.draw(self.screen)
        for mower in self.lawnmowers:
            if mower.visible:
                mower.draw(self.screen)
        for sun in self.suns:
            sun.draw(self.screen)

        self.hud.draw(self.screen, self.sun_count)

        if self.state == GameState.PAUSED:
            self.pause_menu.draw(self.screen, mouse_pos)
        elif self.state in (GameState.WIN, GameState.LOSE):
            self.end_screen.draw(self.screen, mouse_pos, won=(self.state == GameState.WIN))
