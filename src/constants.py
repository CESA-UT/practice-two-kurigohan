"""
Global constants for the Plants vs Zombies clone.

All numeric gameplay values (HP, cooldowns, damage, speeds, wave timings)
come directly from docs/characters/*.md in the assignment repository.
Keeping them in one place makes the game easy to balance/tune and keeps
every other module free of "magic numbers".
"""

import os

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "Assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
ICONS_DIR = os.path.join(ASSETS_DIR, "icon")

IMG = {
    "frontyard": os.path.join(IMAGES_DIR, "items", "Frontyard.png"),
    "card_peashooter": os.path.join(IMAGES_DIR, "Cards", "PeaShooter.png"),
    "card_sunflower": os.path.join(IMAGES_DIR, "Cards", "SunFlower.png"),
    "card_wallnut": os.path.join(IMAGES_DIR, "Cards", "WallNut.png"),
    "plant_peashooter": os.path.join(IMAGES_DIR, "Plants", "Peashooter.gif"),
    "plant_sunflower": os.path.join(IMAGES_DIR, "Plants", "SunFlower.gif"),
    "plant_wallnut": os.path.join(IMAGES_DIR, "Plants", "Wallnut.gif"),
    "plant_wallnut_dying": os.path.join(IMAGES_DIR, "Plants", "Wallnut_Dying.gif"),
    "zombie_normal_walk": os.path.join(IMAGES_DIR, "Zombies", "NormalZombie.gif"),
    "zombie_normal_eat": os.path.join(IMAGES_DIR, "Zombies", "NormalZombieEat.gif"),
    "pea": os.path.join(IMAGES_DIR, "items", "Pea.png"),
    "sun": os.path.join(IMAGES_DIR, "items", "Sun.png"),
    "shovel": os.path.join(IMAGES_DIR, "items", "Shovel.png"),
    "lawnmower_idle": os.path.join(IMAGES_DIR, "items", "lawnMower_Idle.png"),
    "lawnmower_active": os.path.join(IMAGES_DIR, "items", "lawnMower_Active.gif"),
    "icon_win": os.path.join(ICONS_DIR, "face-smile-beam.png"),
    "icon_lose": os.path.join(ICONS_DIR, "face-sad-cry.png"),
    "icon_party": os.path.join(ICONS_DIR, "party-horn.png"),
    "icon_menu": os.path.join(ICONS_DIR, "bars-solid.png"),
    "icon_house": os.path.join(ICONS_DIR, "house-solid.png"),
}

SND = {
    "plant": os.path.join(SOUNDS_DIR, "plant.wav"),
    "chomp": os.path.join(SOUNDS_DIR, "chomp.wav"),
    "splat": os.path.join(SOUNDS_DIR, "splat3.wav"),
    "groan": os.path.join(SOUNDS_DIR, "groan.wav"),
    "wave_incoming": os.path.join(SOUNDS_DIR, "zombies_are_coming.wav"),
    "lawnmower": os.path.join(SOUNDS_DIR, "lawnmower.wav"),
    "brainz": os.path.join(SOUNDS_DIR, "brainz.wav"),
}

# ---------------------------------------------------------------------------
# Board / screen geometry  (GameRules.md: 5 rows x 9 columns)
# ---------------------------------------------------------------------------
BOARD_ROWS = 5
BOARD_COLS = 9

LAWN_IMAGE_SIZE = (1024, 626)  # native size of Frontyard.png

HUD_HEIGHT = 110  # top strip reserved for sun counter + plant cards
BOARD_ORIGIN_X = 0
BOARD_ORIGIN_Y = HUD_HEIGHT

CELL_WIDTH = LAWN_IMAGE_SIZE[0] / BOARD_COLS
CELL_HEIGHT = LAWN_IMAGE_SIZE[1] / BOARD_ROWS

SCREEN_WIDTH = LAWN_IMAGE_SIZE[0]
SCREEN_HEIGHT = HUD_HEIGHT + LAWN_IMAGE_SIZE[1]

FPS = 60
GAME_TITLE = "Plants vs Zombies - AP Practice 2"

# ---------------------------------------------------------------------------
# Sun economy (GameRules.md)
# ---------------------------------------------------------------------------
INITIAL_SUN = 150
SUN_VALUE = 25
SKY_SUN_INTERVAL = 10.0      # a sun falls from the sky every 10s
SUN_FALL_SPEED = 90.0        # px/sec while falling from the sky
SUN_LIFETIME = 9.0           # seconds a sun stays collectible before vanishing
SUN_DISPLAY_SIZE = (64, 64)

# ---------------------------------------------------------------------------
# Combat (GameRules.md)
# ---------------------------------------------------------------------------
PEA_DAMAGE = 20
PEA_SPEED_CELLS_PER_SEC = 3.5
PEA_DISPLAY_SIZE = (28, 28)
ZOMBIE_EAT_DAMAGE_PER_SEC = 100

# ---------------------------------------------------------------------------
# Plants (PeaShooter.md, SunFlower.md, WallNut.md)
# ---------------------------------------------------------------------------
PLANT_CONFIG = {
    "PeaShooter": {
        "cost": 100,
        "hp": 300,
        "card_cooldown": 7.5,
        "shoot_interval": 1.5,
        "damage": PEA_DAMAGE,
        "display_size": (100, 100),
    },
    "SunFlower": {
        "cost": 50,
        "hp": 300,
        "card_cooldown": 7.5,
        "sun_interval": 24.0,
        "first_sun_delay": 7.0,   # simplification allowed by SunFlower.md
        "sun_value": 25,
        "display_size": (100, 100),
    },
    "WallNut": {
        "cost": 50,
        "hp": 4000,
        "card_cooldown": 30.0,
        "display_size": (85, 96),
    },
}

PLANT_ORDER = ["PeaShooter", "SunFlower", "WallNut"]

# ---------------------------------------------------------------------------
# Zombies (NormalZombie.md)
# ---------------------------------------------------------------------------
ZOMBIE_CONFIG = {
    "NormalZombie": {
        "hp": 200,
        "speed": 0.25,  # cells per second
        "eat_damage": ZOMBIE_EAT_DAMAGE_PER_SEC,
        "display_size": (90, 130),
    },
}

# ---------------------------------------------------------------------------
# Waves (Waves.md - minimum acceptable table, total 15 zombies)
# ---------------------------------------------------------------------------
WAVES = [
    {"start_time": 20.0, "count": 3, "type": "NormalZombie"},
    {"start_time": 50.0, "count": 5, "type": "NormalZombie"},
    {"start_time": 90.0, "count": 7, "type": "NormalZombie"},
]
WAVE_SPAWN_STAGGER = 1.4  # seconds between individual zombie spawns within a wave

# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------
COLOR_HUD_BG = (61, 40, 23)
COLOR_HUD_BORDER = (35, 22, 12)
COLOR_TEXT = (255, 255, 255)
COLOR_TEXT_DARK = (30, 30, 30)
COLOR_SUN_COUNTER_BG = (0, 0, 0, 120)
COLOR_CARD_LOCKED = (0, 0, 0, 150)
COLOR_CARD_SELECTED = (255, 255, 0)
COLOR_OVERLAY_BG = (0, 0, 0, 170)
COLOR_GRID_HOVER = (255, 255, 255, 60)
COLOR_SHOVEL_SELECTED = (255, 200, 0)
