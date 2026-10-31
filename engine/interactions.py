from typing import Any
from collections.abc import Sequence
import time
import pygame

from engine.player import Player
from engine.ghost import Ghost


class InteractionManager:

    def __init__(
        self, player: Player, pacgums: Any, super_pacgums: Any
    ) -> None:
        self.player = player
        self.pacgums = pacgums
        self.super_pacgums = super_pacgums

    def check_pacgum(self, ghosts) -> None:
        if self.player.current_pos in self.pacgums:
            self.pacgums.discard(self.player.current_pos)
            self.player.add_score()
        elif self.player.current_pos in self.super_pacgums:
            self.super_pacgums.remove(self.player.current_pos)
            for ghost in ghosts:
                if ghost.is_eaten:
                    continue
                ghost.state = "Frightened"
                ghost.frightened_time = pygame.time.get_ticks()
            self.player.add_super_score()

    def check_ghost_collision(
        self,
        ghosts: Sequence[Ghost],
        current_time: float | None = None,
    ) -> bool:
        if current_time is None:
            current_time = time.monotonic()
        if self.player.is_respawn_protected(current_time):
            return False

        for ghost in ghosts:
            if ghost.is_eaten:
                continue
            if self.player.current_pos != ghost.current_pos:
                continue
            if ghost.state == "chase":
                if self.player.current_pos == ghost.current_pos:
                    self.player.lose_life(current_time)
                    for ghost in ghosts:
                        ghost.current_pos = ghost.spawn_pos
                    return True
            ghost.is_eaten = True
            ghost.eaten_time = pygame.time.get_ticks()
            ghost.current_pos = ghost.spawn_pos
            self.player.add_ghost_score()
        return False
