from maze.screens import ScreensMixin
from collections import deque
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
        self.parent: dict[
            tuple[int, int], tuple[int, int] | None
        ] = {}

    def get_neighbors(
        self, maze: Any, cell: tuple[int, int]
    ) -> list[tuple[int, int]]:
        neighbors = []
        x, y = cell[0], cell[1]
        cell_value = int(maze.maze[y][x])

        if not cell_value & 1 and self.inside._inside(maze, x, y - 1):
            neighbors.append((x, y - 1))
        if not cell_value & 2 and self.inside._inside(maze, x + 1, y):
            neighbors.append((x + 1, y))
        if not cell_value & 4 and self.inside._inside(maze, x, y + 1):
            neighbors.append((x, y + 1))

        if not cell_value & 8 and self.inside._inside(maze, x - 1, y):
            neighbors.append((x - 1, y))
        return neighbors

    def shortest_path(
        self, maze: Any, target_pos: tuple[int, int]
    ) -> list[tuple[int, int]]:
        queue = deque([self.current_pos])
        visited = {self.current_pos}
        self.parent = {self.current_pos: None}
        while queue:
            current = queue.popleft()
            if current == target_pos:
                break
            neighbors = self.get_neighbors(maze, current)
            for neighbor in neighbors:
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                queue.append(neighbor)
                self.parent[neighbor] = current

        if target_pos not in self.parent:
            return []

        path = []
        current_cell: tuple[int, int] | None = target_pos

        while current_cell is not None:
            path.append(current_cell)
            current_cell = self.parent[current_cell]

        path.reverse()
        return path

    def move(
        self, maze: Any, target_pos: tuple[int, int]
    ) -> tuple[int, int] | None:
        path = self.shortest_path(maze, target_pos)
        if len(path) >= 2:
            next_direction = path[1]
            return next_direction
        return None
