from collections import deque
from typing import Any

from engine.player import Player


class Ghost:
    """Manage ghost movement, targeting, and behavior."""

    directions = {"right": (1, 0), "up": (0, -1),
                  "down": (0, 1), "left": (-1, 0)}

    def __init__(
        self,
        color: str,
        direction: str | None,
        spawn_pos: tuple[int, int]
    ) -> None:
        self.color = color
        self.direction = direction
        self.spawn_pos = spawn_pos
        self.current_pos = spawn_pos
        self.state = "chase"
        self.frightened_time = 0
        self.is_eaten = False
        self.eaten_time = 0
        self.previous_pos: tuple[int, int] | None = None

    def _inside(self, maze: Any, x: int, y: int) -> bool:
        """Check if a position is inside the maze."""
        return 0 <= y < len(maze.maze) and 0 <= x < len(maze.maze[0])

    def get_neighbors(
        self, maze: Any, cell: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """Get all accessible neighboring cells."""
        neighbors = []
        x, y = cell[0], cell[1]
        cell_value = int(maze.maze[y][x])

        if not cell_value & 1 and self._inside(maze, x, y - 1):
            neighbors.append((x, y - 1))
        if not cell_value & 2 and self._inside(maze, x + 1, y):
            neighbors.append((x + 1, y))
        if not cell_value & 4 and self._inside(maze, x, y + 1):
            neighbors.append((x, y + 1))

        if not cell_value & 8 and self._inside(maze, x - 1, y):
            neighbors.append((x - 1, y))
        return neighbors

    def shortest_path(
        self, maze: Any, target_pos: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """Find the shortest path to a target using BFS."""
        queue = deque([self.current_pos])
        visited = {self.current_pos}
        parent: dict[tuple[int, int], tuple[int, int] | None] = {
            self.current_pos: None
        }
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
                parent[neighbor] = current

        if target_pos not in parent:
            return []

        path = []
        current_cell: tuple[int, int] | None = target_pos

        while current_cell is not None:
            path.append(current_cell)
            current_cell = parent[current_cell]

        path.reverse()
        return path

    def move(
        self, maze: Any, target_pos: tuple[int, int]
    ) -> tuple[int, int] | None:
        """Get the next position along the shortest path."""
        path = self.shortest_path(maze, target_pos)
        if len(path) >= 2:
            next_direction = path[1]
            return next_direction
        return None

    def get_target_position(
        self, player: Player, red_ghost: "Ghost", maze: Any
    ) -> tuple[int, int]:
        """Calculate the target position based on the ghost's color."""
        if self.color == "red":
            return player.current_pos
        elif self.color == "pink":
            direction = player.direction or "right"
            target_x = (
                player.current_pos[0]
                + self.directions[direction][0] * 4
            )
            target_y = (
                player.current_pos[1]
                + self.directions[direction][1] * 4
            )
        elif self.color == "blue":
            direction = player.direction or "right"
            intermediate_target_x = (
                player.current_pos[0]
                + self.directions[direction][0] * 2
            )
            intermediate_target_y = (
                player.current_pos[1]
                + self.directions[direction][1] * 2
            )
            target_x = (
                (intermediate_target_x - red_ghost.current_pos[0]) * 2
                + red_ghost.current_pos[0]
            )
            target_y = (
                (intermediate_target_y - red_ghost.current_pos[1]) * 2
                + red_ghost.current_pos[1]
            )
        elif self.color == "orange":
            distance = (
                abs(self.current_pos[0] - player.current_pos[0])
                + abs(self.current_pos[1] - player.current_pos[1])
            )
            if distance > 8:
                return player.current_pos
            else:
                return self.spawn_pos
        target_x = max(0, min(len(maze.maze[0]) - 1, target_x))
        target_y = max(0, min(len(maze.maze) - 1, target_y))
        target = (target_x, target_y)
        return target

    def get_escape_move(
        self, maze: Any, target_pos: tuple[int, int]
    ) -> tuple[int, int]:
        """Choose the neighboring cell farthest from the target."""
        neighbors = self.get_neighbors(maze, self.current_pos)

        if not neighbors:
            return self.current_pos

        if (
            len(neighbors) > 1
            and self.previous_pos is not None
            and self.previous_pos in neighbors
        ):
            neighbors.remove(self.previous_pos)

        distances = {}

        for neighbor in neighbors:
            distance = (
                abs(neighbor[0] - target_pos[0])
                + abs(neighbor[1] - target_pos[1])
            )
            distances[neighbor] = distance

        return max(distances, key=lambda pos: distances[pos])
