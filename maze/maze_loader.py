
from typing import Any


class Loader:
    DIRECTIONS = {
        "up": (0, -1, 1, 4),
        "right": (1, 0, 2, 8),
        "down": (0, 1, 4, 1),
        "left": (-1, 0, 8, 2),
    }

    def __init__(self, maze: Any) -> None:
        self.maze = maze.maze
        self.height = len(self.maze)
        self.width = len(self.maze[0]) if self.height else 0

    def open_wall(self, x: int, y: int, direction: str) -> bool:
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        if direction not in self.DIRECTIONS:
            raise ValueError("invalide direction")

        dx, dy, wall, opposite_wall = self.DIRECTIONS[direction]
        next_x = x + dx
        next_y = y + dy

        if not (0 <= next_x < self.width and 0 <= next_y < self.height):
            return False

        current_walls = self.maze[y][x]
        next_walls = self.maze[next_y][next_x]

        if current_walls & wall or next_walls & opposite_wall:
            return False
        return True
