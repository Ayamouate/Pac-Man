from typing import Any

from maze.maze_loader import Loader


class Player:
    directions = {"right": (1, 0), "up": (0, -1),
                  "down": (0, 1), "left": (-1, 0)}

    def __init__(
        self, start_position: tuple[int, int], lives: int = 3
    ) -> None:
        self.start_position = start_position
        self.lives = lives
        self.score = 0
        self.direction = ""
        self.current_pos = self.start_position

    def can_move(self, direction: str, maze: Any) -> bool:
        if direction not in self.directions:
            return False
        move = Loader(maze).open_wall(
            self.current_pos[0], self.current_pos[1], direction)
        if move:
            self.current_pos = (
                self.current_pos[0] + self.directions[direction][0],
                self.current_pos[1] + self.directions[direction][1]
            )
            self.direction = direction
            return True
        return False

    def move(self, maze: Any) -> None:
        self.can_move(self.direction, maze)

    def add_score(self, points: int) -> None:
        self.score += points

    def is_alive(self) -> bool:
        return self.lives > 0

    def lose_life(self) -> int:
        if self.lives > 0:
            self.lives -= 1
            self.current_pos = self.start_position
        return self.lives
