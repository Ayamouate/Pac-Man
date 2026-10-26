from typing import Any

from maze.maze_loader import Loader


class Player:
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

    def lose_life(self) -> int:
        if self.lives > 0:
            self.lives -= 1
            self.current_pos = self.start_position
        return self.lives
