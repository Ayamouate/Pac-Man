"""Pygame display for the generated maze levels."""

from __future__ import annotations
from collections.abc import Mapping, Sequence
from typing import Any


Level = Mapping[str, Any]


class MazeViewer:
    """Display configured mazes one level at a time."""

    WINDOW_SIZE = (1100, 800)
    HEADER_HEIGHT = 92
    PADDING = 24

    BACKGROUND = (8, 10, 24)
    FLOOR = (15, 20, 42)
    WALL = (52, 145, 255)
    PATH = (80, 220, 220)
    ENTRY = (255, 220, 40)
    EXIT = (255, 85, 100)
    TEXT = (235, 240, 255)
    MUTED_TEXT = (155, 165, 195)

    def __init__(self, levels: Sequence[Level], mazes: Sequence[Any]) -> None:
        if len(levels) != len(mazes):
            raise ValueError(
                "Each configured level must have a generated maze"
            )
        if not levels:
            raise ValueError("At least one maze level is required")
        self._levels = levels
        self._mazes = mazes
        self._level_index = 0
        self._show_path = False

    def run(self) -> None:
        """Open the window and process input until the user closes it."""

        try:
            import pygame
        except ModuleNotFoundError as error:
            if error.name == "pygame":
                raise RuntimeError(
                    "Pygame is required for the maze viewer; "
                    "run 'make install'."
                ) from error
            raise

        pygame.init()
        screen = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption("Pac-Man Maze Viewer")
        title_font = pygame.font.Font(None, 32)
        info_font = pygame.font.Font(None, 24)
        clock = pygame.time.Clock()

        running = True
        try:
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        running = self._handle_key(pygame, event.key)

                self._draw(pygame, screen, title_font, info_font)
                pygame.display.flip()
                clock.tick(60)
        finally:
            pygame.quit()

    def _handle_key(self, pygame: Any, key: int) -> bool:
        if key in (pygame.K_ESCAPE, pygame.K_q):
            return False
        if key in (pygame.K_RIGHT, pygame.K_d, pygame.K_DOWN, pygame.K_s):
            self._level_index = (self._level_index + 1) % len(self._mazes)
        elif key in (pygame.K_LEFT, pygame.K_a, pygame.K_UP, pygame.K_w):
            self._level_index = (self._level_index - 1) % len(self._mazes)
        elif key == pygame.K_p:
            self._show_path = not self._show_path
        return True

    def _draw(
        self, pygame: Any, screen: Any, title_font: Any, info_font: Any
    ) -> None:
        screen.fill(self.BACKGROUND)
        maze = self._mazes[self._level_index]
        level = self._levels[self._level_index]
        width = level["width"]
        height = level["height"]
        cell_size, origin_x, origin_y = self._layout(width, height)

        title = (
            f"Level {self._level_index + 1}/{len(self._mazes)}  "
            f"{width}x{height}"
        )
        self._draw_text(pygame, screen, title_font, title, self.TEXT, 24, 16)
        path_length = len(maze.shortest_path or "")
        path_state = "on" if self._show_path else "off"
        details = (
            f"Shortest path: {path_length} steps   |   Path: {path_state}   "
            "|   Left/Right: level   P: path   Esc/Q: quit"
        )
        self._draw_text(
            pygame, screen, info_font, details, self.MUTED_TEXT, 24, 52
        )

        self._draw_cells(
            pygame, screen, maze, cell_size, origin_x, origin_y, width, height
        )
        if self._show_path:
            self._draw_path(
                pygame, screen, maze, cell_size, origin_x, origin_y
            )
        self._draw_endpoints(
            pygame, screen, maze, cell_size, origin_x, origin_y
        )

    def _layout(self, width: int, height: int) -> tuple[int, int, int]:
        window_width, window_height = self.WINDOW_SIZE
        available_width = window_width - 2 * self.PADDING
        available_height = (
            window_height - self.HEADER_HEIGHT - 2 * self.PADDING
        )
        cell_size = max(
            1, min(available_width // width, available_height // height)
        )
        maze_width = width * cell_size
        maze_height = height * cell_size
        origin_x = (window_width - maze_width) // 2
        origin_y = self.HEADER_HEIGHT + (
            window_height - self.HEADER_HEIGHT - maze_height
        ) // 2
        return cell_size, origin_x, origin_y

    def _draw_cells(
        self,
        pygame: Any,
        screen: Any,
        maze: Any,
        cell_size: int,
        origin_x: int,
        origin_y: int,
        width: int,
        height: int,
    ) -> None:
        for y in range(height):
            for x in range(width):
                left = origin_x + x * cell_size
                top = origin_y + y * cell_size
                cell = pygame.Rect(left, top, cell_size, cell_size)
                pygame.draw.rect(screen, self.FLOOR, cell)
                walls = maze.maze[y][x]
                if walls & 1:
                    self._draw_wall(
                        pygame, screen, left, top, left + cell_size, top
                    )
                if walls & 2:
                    self._draw_wall(
                        pygame,
                        screen,
                        left + cell_size,
                        top,
                        left + cell_size,
                        top + cell_size,
                    )
                if walls & 4:
                    self._draw_wall(
                        pygame,
                        screen,
                        left,
                        top + cell_size,
                        left + cell_size,
                        top + cell_size,
                    )
                if walls & 8:
                    self._draw_wall(
                        pygame, screen, left, top, left, top + cell_size
                    )

    def _draw_wall(
        self,
        pygame: Any,
        screen: Any,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
    ) -> None:
        pygame.draw.line(
            screen, self.WALL, (start_x, start_y), (end_x, end_y), 2
        )

    def _draw_path(
        self,
        pygame: Any,
        screen: Any,
        maze: Any,
        cell_size: int,
        origin_x: int,
        origin_y: int,
    ) -> None:
        x, y = maze.maze_entry
        cells = [(x, y)]
        moves = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
        for move in maze.shortest_path or "":
            dx, dy = moves[move]
            x += dx
            y += dy
            cells.append((x, y))

        points = [
            (
                origin_x + cell_x * cell_size + cell_size // 2,
                origin_y + cell_y * cell_size + cell_size // 2,
            )
            for cell_x, cell_y in cells
        ]
        if len(points) > 1:
            pygame.draw.lines(
                screen, self.PATH, False, points, max(2, cell_size // 5)
            )
        for point in points:
            pygame.draw.circle(
                screen, self.PATH, point, max(2, cell_size // 7)
            )

    def _draw_endpoints(
        self,
        pygame: Any,
        screen: Any,
        maze: Any,
        cell_size: int,
        origin_x: int,
        origin_y: int,
    ) -> None:
        radius = max(4, cell_size // 3)
        for point, colour in (
            (maze.maze_entry, self.ENTRY),
            (maze.maze_exit, self.EXIT),
        ):
            x, y = point
            center = (
                origin_x + x * cell_size + cell_size // 2,
                origin_y + y * cell_size + cell_size // 2,
            )
            pygame.draw.circle(screen, colour, center, radius)

    def _draw_text(
        self,
        pygame: Any,
        screen: Any,
        font: Any,
        message: str,
        colour: tuple[int, int, int],
        x: int,
        y: int,
    ) -> None:
        screen.blit(font.render(message, True, colour), (x, y))
