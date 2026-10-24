from typing import Any


class Pacgums():

    def __init__(self, maze: Any, player: Any) -> None:
        self.maze = maze
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
        for y in range(self.height):
            for x in range(self.width):
                pos = (x, y)
                if self.maze.maze[y][x] == 15:
                    continue
                if pos == self.player.start_position:
                    continue
                if pos in self.super_pacgums:
                    continue

                self.pacgums.add(pos)
        return self.pacgums
