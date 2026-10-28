from maze.screens import ScreensMixin
from typing import Any


class Ghost:
    def __init__(
        self,
        color: str,
        direction: str | None,
        spawn_pos: tuple[int, int],
        current_pos: tuple[int, int],
        state: str,
    ) -> None:
        self.color = color
        self.direction = direction
        self.spawn_pos = spawn_pos
        self.current_pos = current_pos
        self.state = state
        self.inside = ScreensMixin()

    def get_neighbors(
        self, maze: Any, ghost: "Ghost"
    ) -> list[tuple[int, int]]:
        neighbors = []
        x, y = ghost.current_pos[0], ghost.current_pos[1]
        cell = int(maze.maze[y][x])

        if not cell & 1 and self.inside._inside(maze, x, y - 1):
            neighbors.append((x, y - 1))
        if not cell & 2 and self.inside._inside(maze, x + 1, y):
            neighbors.append((x + 1, y))
        if not cell & 4 and self.inside._inside(maze, x, y + 1):
            neighbors.append((x, y + 1))

        if not cell & 8 and self.inside._inside(maze, x - 1, y):
            neighbors.append((x - 1, y))
        return neighbors
