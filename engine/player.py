import time
from typing import Any

from maze.maze_loader import Loader


class Player:
    RESPAWN_PROTECTION_SECONDS = 3.0
    directions = {"right": (1, 0), "up": (0, -1),
                  "down": (0, 1), "left": (-1, 0)}

    def __init__(
        self,
        start_position: tuple[int, int],
        lives: int,
        super_pacgums_points: int,
        pacgums_points: int,
    ) -> None:
        self.start_position = start_position
        self.super_pacgums_points = super_pacgums_points
        self.pacgums_points = pacgums_points
        self.lives = lives
        self.score = 0
        self.direction: str | None = None
        self.current_pos = self.start_position
        self.respawn_protection_until = 0.0

    def can_move(self, direction: str, maze: Any) -> bool:
        if direction not in self.directions:
            return False
        move = Loader(maze).open_wall(
            self.current_pos[0], self.current_pos[1], direction)
        if move:
            self.current_pos = (
                self.current_pos[0] + self.directions[direction][0],
                self.current_pos[1] + self.directions[direction][1],
            )
            self.direction = direction
            return True
        return False

    def move(self, maze: Any) -> None:
        if self.direction is not None:
            self.can_move(self.direction, maze)

    def add_score(self) -> None:
        self.score += self.pacgums_points

    def add_super_score(self) -> None:
        self.score += self.super_pacgums_points

    def is_alive(self) -> bool:
        if self.lives == 0:
            return False
        else:
            return True

    def is_respawn_protected(self, current_time: float | None = None) -> bool:
        """Return whether the player is temporarily safe after respawning."""

        if current_time is None:
            current_time = time.monotonic()
        return current_time < self.respawn_protection_until

    def clear_respawn_protection(self) -> None:
        """Clear protection when starting or changing to a new game level."""

        self.respawn_protection_until = 0.0

    def lose_life(self, current_time: float | None = None) -> int:
        if self.lives > 0:
            self.lives -= 1
            self.current_pos = self.start_position
            self.direction = None
            if current_time is None:
                current_time = time.monotonic()
            self.respawn_protection_until = (
                current_time + self.RESPAWN_PROTECTION_SECONDS
            )
        return self.lives
