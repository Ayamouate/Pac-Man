from typing import Any
import random


class Pacgums():
    """Handle pacgum positions and placement in the maze."""
    pacgum = 42

    def __init__(self, maze: Any, player: Any, number: int) -> None:
        self.maze = maze
        self.number = number
        self.pacgums: set[tuple[int, int]] = set()
        self.height = len(self.maze.maze)
        self.width = len(self.maze.maze[0])
        self.super_pacgums = [
            (0, 0),
            (self.width - 1, 0),
            (self.width - 1, self.height - 1),
            (0, self.height - 1),
        ]
        self.player = player
        self.set_pacgums()

    def set_pacgums(self) -> set[tuple[int, int]]:
        """Place regular pacgums in valid maze cells."""

        available_cells = []
        for y in range(self.height):
            for x in range(self.width):
                pos = (x, y)
                if self.maze.maze[y][x] == 15:
                    continue
                if pos == self.player.start_position:
                    continue
                if pos in self.super_pacgums:
                    continue
                available_cells.append(pos)
        if len(available_cells) >= self.number:
            number = self.number
        else:
            number = min(self.pacgum, len(available_cells))
        self.pacgums = set(random.sample(available_cells, number))
        return self.pacgums
