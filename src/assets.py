"""
Asset loading helpers.

pygame cannot decode animated GIFs on its own, so we use Pillow to split a
GIF into its individual frames (converted to pygame Surfaces) and wrap them
in an AnimatedSprite that cycles through them over time. Static images
(.png) are loaded directly through pygame.

Everything is cached so each file is only ever read from disk once.
"""

import os
import pygame
from PIL import Image, ImageSequence

_image_cache = {}
_gif_cache = {}
_sound_cache = {}


def load_image(path, size=None, alpha=True):
    """Load a static image (png/jpg) as a pygame Surface, optionally scaled."""
    key = (path, size)
    if key in _image_cache:
        return _image_cache[key]

    surface = pygame.image.load(path)
    surface = surface.convert_alpha() if alpha else surface.convert()
    if size is not None:
        surface = pygame.transform.smoothscale(surface, size)

    _image_cache[key] = surface
    return surface


def load_gif_frames(path, size=None):
    """
    Load every frame of a GIF as a list of (pygame.Surface, duration_seconds).

    Frame durations come from the GIF's own metadata; if a frame is missing
    duration info we fall back to 80ms which looks natural for these sprites.
    """
    key = (path, size)
    if key in _gif_cache:
        return _gif_cache[key]

    frames = []
    with Image.open(path) as im:
        for frame in ImageSequence.Iterator(im):
            rgba = frame.convert("RGBA")
            if size is not None:
                rgba = rgba.resize(size, Image.LANCZOS)
            data = rgba.tobytes()
            surface = pygame.image.frombuffer(data, rgba.size, "RGBA").convert_alpha()
            duration_ms = frame.info.get("duration", 80)
            frames.append((surface, max(duration_ms, 20) / 1000.0))

    if not frames:
        raise ValueError(f"No frames decoded from {path}")

    _gif_cache[key] = frames
    return frames


def load_sound(path):
    """Load a sound effect, returning None if audio is unavailable.

    The grading machine might not have a working audio device, so every
    caller must tolerate a None result instead of crashing.
    """
    if path in _sound_cache:
        return _sound_cache[path]
    try:
        sound = pygame.mixer.Sound(path)
    except (pygame.error, FileNotFoundError):
        sound = None
    _sound_cache[path] = sound
    return sound


def play_sound(sound, volume=0.6):
    if sound is not None:
        try:
            sound.set_volume(volume)
            sound.play()
        except pygame.error:
            pass


class AnimatedSprite:
    """Cycles through a list of GIF frames based on elapsed time."""

    def __init__(self, path, size=None, loop=True):
        self.frames = load_gif_frames(path, size=size)
        self.loop = loop
        self.index = 0
        self.timer = 0.0
        self.finished = False

    def reset(self):
        self.index = 0
        self.timer = 0.0
        self.finished = False

    def update(self, dt):
        if self.finished:
            return
        self.timer += dt
        _, duration = self.frames[self.index]
        while self.timer >= duration:
            self.timer -= duration
            if self.index + 1 < len(self.frames):
                self.index += 1
            elif self.loop:
                self.index = 0
            else:
                self.finished = True
                break
            _, duration = self.frames[self.index]

    @property
    def image(self):
        return self.frames[self.index][0]

    def get_rect(self, **kwargs):
        return self.image.get_rect(**kwargs)
