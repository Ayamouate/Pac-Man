from pathlib import Path
from typing import Any, Final

import pygame


class SoundManager:

    MUSIC_FILE: Final[str] = "music.wav"

    SOUND_FILES: Final[dict[str, str]] = {
        "menu_move": "menu_move.wav",
        "menu_select": "menu_select.wav",
        "menu_jingle": "menu_select.wav",
        "pacgum": "pacgum_collect.wav",
        "power_pellet": "power_pellet.wav",
        "ghost_eaten": "ghost_eaten.wav",
        "death": "player_death.wav",
        "level_clear": "level_clear.wav",
        "game_over": "game_over.wav",
    }

    SOUND_VOLUMES: Final[dict[str, float]] = {
        "pacgum": 0.15,
        "power_pellet": 0.30,
        "game_over": 0.35,
        "menu_select": 0.35,
        "menu_jingle": 0.35,
        "menu_move": 0.35,
        "level_clear": 0.35,
        "death": 0.30,
        "ghost_eaten": 0.35,
    }

    def __init__(self, sound_dir: Path | None = None) -> None:
        self.enabled = True
        self.available = False
        self.sounds: dict[str, Any] = {}
        self.sound_dir = sound_dir or Path(__file__).with_name("sounds")
        self.music_dir = self.sound_dir.parent / "music"
        self.music_available = False
        self.music_started = False
        self.music_paused = False

    def load(self) -> None:
        """Initialize the mixer and load the bundled effects if possible."""

        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init()
            self.available = True
        except (pygame.error, OSError):
            self.available = False
            return

        for name, filename in self.SOUND_FILES.items():
            try:
                sound = pygame.mixer.Sound(
                    str(self.sound_dir / filename)
                )
                sound.set_volume(self.SOUND_VOLUMES.get(name, 1.0))
                self.sounds[name] = sound
            except (pygame.error, OSError, FileNotFoundError):
                # A missing or unsupported asset should not stop the game.
                continue

        try:
            pygame.mixer.music.load(str(self.music_dir / self.MUSIC_FILE))
            self.music_available = True
        except (pygame.error, OSError, FileNotFoundError):
            self.music_available = False

    def play_music(self) -> None:
        """Start the gameplay loop, or resume it after a pause."""

        if not self.enabled or not self.music_available:
            return
        try:
            if self.music_paused:
                pygame.mixer.music.unpause()
                self.music_paused = False
            elif not self.music_started:
                pygame.mixer.music.play(-1)
                self.music_started = True
        except pygame.error:
            pass

    def pause_music(self) -> None:
        if not self.enabled or not self.music_available:
            return
        try:
            if self.music_started and not self.music_paused:
                pygame.mixer.music.pause()
                self.music_paused = True
        except pygame.error:
            pass

    def stop_music(self) -> None:
        if not self.music_available:
            return
        try:
            if self.music_started or self.music_paused:
                pygame.mixer.music.stop()
            self.music_started = False
            self.music_paused = False
        except pygame.error:
            pass

    def play(self, name: str) -> None:

        if not self.enabled or not self.available:
            return
        sound = self.sounds.get(name)
        if sound is None:
            return

        try:
            sound.play()
        except pygame.error:
            pass
