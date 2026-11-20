from typing import Any
from collections.abc import Sequence
import time
import pygame

from engine.player import Player
from engine.ghost import Ghost


class InteractionManager:
    """Manage interactions between the player, pacgums, and ghosts."""

    def __init__(
        self,
        player: Player,
        pacgums: set,
        super_pacgums: list,
        sound_manager: Any = None,
    ) -> None:
        self.player = player
        self.pacgums = pacgums
        self.super_pacgums = super_pacgums
        self.sound_manager = sound_manager

    def _play(self, name: str) -> None:
        if self.sound_manager is not None:
            self.sound_manager.play(name)

    def check_pacgum(self, ghosts: Sequence[Ghost]) -> None:
        """Check and handle pacgum and super pacgum collection."""

        if self.player.current_pos in self.pacgums:
            self.pacgums.discard(self.player.current_pos)
            self.player.add_score()
            self._play("pacgum")
        elif self.player.current_pos in self.super_pacgums:
            self.super_pacgums.remove(self.player.current_pos)
            for ghost in ghosts:
                if ghost.is_eaten:
                    continue
                ghost.state = "scared"
                ghost.frightened_time = pygame.time.get_ticks()
            self.player.add_super_score()
            self._play("power_pellet")

    def check_ghost_collision(
        self,
        ghosts: Sequence[Ghost],
        invincibility: bool
    ) -> bool:
        """Handle collisions between the player and ghosts."""

        current_time = time.monotonic()
        if self.player.is_respawn_protected(current_time):
            return False

        for ghost in ghosts:
            if invincibility and ghost.state == "chase":
                return False
            if ghost.is_eaten:
                continue
            if self.player.current_pos != ghost.current_pos:
                continue
            if ghost.state == "chase":
                if self.player.current_pos == ghost.current_pos:
                    self.player.lose_life(current_time)
                    for ghost in ghosts:
                        ghost.current_pos = ghost.spawn_pos
                    self._play("death")
                    return True
            ghost.is_eaten = True
            ghost.eaten_time = pygame.time.get_ticks()
            ghost.current_pos = ghost.spawn_pos
            self.player.add_ghost_score()
            self._play("ghost_eaten")
        return False
