"""Pygame display for the generated maze levels."""

from __future__ import annotations
from collections.abc import Mapping, Sequence
from typing import Any
from engine.player import Player


Level = Mapping[str, Any]


class MazeViewer:
    """Display configured mazes one level at a time."""

    WINDOW_SIZE = (1100, 800)
    HEADER_HEIGHT = 92
    PADDING = 24

    BACKGROUND = (8, 10, 24)
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
        maze = self._mazes[self._level_index]
        self.player = Player((
            len(maze.maze[0]) // 2,
            len(maze.maze) // 2
        ))
        self.player_image: Any = None
        self.background: Any = None
        self.wall_h: Any = None
        self.wall_v: Any = None

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

        self.background = pygame.image.load(
            "assets/Bg.jpeg"
        ).convert()

        self.background = pygame.transform.scale(
            self.background, self.WINDOW_SIZE
        )
        self.wall_h = pygame.image.load(
            "assets/wall_h.png"
        ).convert_alpha()
        self.wall_v = pygame.image.load(
            "assets/wall_v.png"
        ).convert_alpha()

        try:
            self.player_image = pygame.image.load(
                "assets/player.png"
            ).convert_alpha()
        except (pygame.error, FileNotFoundError):
            print("Player image not found. Using yellow circle.")
        pygame.display.set_caption("Pac-Man Maze Viewer")
        title_font = pygame.font.Font(None, 32)
        info_font = pygame.font.Font(None, 24)
        clock = pygame.time.Clock()
        last_move = pygame.time.get_ticks()
        move_delay = 180
        running = True
        try:
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        running = self._handle_key(pygame, event.key)
                now = pygame.time.get_ticks()

                if now - last_move >= move_delay:
                    maze = self._mazes[self._level_index]
                    self.player.move(maze)
                    last_move = now

                self._draw(pygame, screen, title_font, info_font)
                pygame.display.flip()
                clock.tick(60)
        finally:
            pygame.quit()

    def _handle_key(self, pygame: Any, key: int) -> bool:

        moves = {
            pygame.K_UP: "up",
            pygame.K_w: "up",
            pygame.K_DOWN: "down",
            pygame.K_s: "down",
            pygame.K_LEFT: "left",
            pygame.K_a: "left",
            pygame.K_RIGHT: "right",
            pygame.K_d: "right",
        }
        if key in (pygame.K_ESCAPE, pygame.K_q):
            return False
        elif key == pygame.K_n:
            self._level_index = (self._level_index + 1) % len(self._mazes)
            self._reset_player()
            return True
        elif key == pygame.K_b:
            self._level_index = (self._level_index - 1) % len(self._mazes)
            self._reset_player()
            return True
        if key not in moves:
            return True

        self.player.direction = moves[key]
        return True

    def _reset_player(self) -> None:
        """Reset the player to the center of the selected maze."""

        maze = self._mazes[self._level_index]
        self.player.start_position = (
            len(maze.maze[0]) // 2,
            len(maze.maze) // 2,
        )
        self.player.current_pos = self.player.start_position
        self.player.direction = ""

    def _draw(
        self, pygame: Any, screen: Any, title_font: Any, info_font: Any
    ) -> None:
        screen.blit(self.background, (0, 0))
        header = pygame.Surface(
            (self.WINDOW_SIZE[0], self.HEADER_HEIGHT), pygame.SRCALPHA
        )
        header.fill((*self.BACKGROUND, 180))
        screen.blit(header, (0, 0))
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
        details = (
            "Arrows/WASD: move   N/B: level   Esc/Q: quit"
        )
        self._draw_text(
            pygame, screen, info_font, details, self.MUTED_TEXT, 24, 52
        )

        self._draw_cells(
            pygame, screen, maze, cell_size, origin_x, origin_y, width, height
        )
        self._draw_player(pygame,
                          screen, cell_size, origin_x, origin_y
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

                floor_surface = pygame.Surface(
                    (cell_size, cell_size), pygame.SRCALPHA)
                floor_surface.fill((230, 210, 180, 180))
                screen.blit(floor_surface, (left, top))
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

        if start_y == end_y:
            wall = pygame.transform.scale(
                self.wall_h, (end_x - start_x, 7)
            )
            screen.blit(wall, (min(start_x, end_x), start_y))
        else:
            wall = pygame.transform.scale(
                self.wall_v, (7, end_y - start_y)
            )
            screen.blit(wall, (start_x, min(start_y, end_y)))

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

    def _draw_player(
        self,
        pygame: Any,
        screen: Any,
        cell_size: int,
        origin_x: int,
        origin_y: int,
    ) -> None:
        x, y = self.player.current_pos

        center_x = origin_x + x * cell_size + cell_size // 2
        center_y = origin_y + y * cell_size + cell_size // 2

        radius = max(3, cell_size // 3)

        if self.player_image is not None:
            size = int(cell_size * 0.8)
            image = pygame.transform.scale(
                self.player_image, (size, size)
            )
            rect = image.get_rect(
                center=(round(center_x), round(center_y))
            )
            screen.blit(image, rect)
        else:
            pygame.draw.circle(
                screen,
                (255, 220, 0),
                (round(center_x), round(center_y)),
                radius,
            )
