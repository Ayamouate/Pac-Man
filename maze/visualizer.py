"""Pygame display for the generated maze levels."""

from __future__ import annotations
from engine.pacgums import Pacgums
from engine.interactions import InteractionManager
from collections.abc import Mapping, Sequence
from typing import Any
from engine.player import Player
from maze.maze_loader import Loader
from maze.game_logic import GameMixin
from maze.screens import ScreensMixin


Level = Mapping[str, Any]


class MazeViewer(GameMixin, ScreensMixin):
    """Display configured mazes one level at a time."""

    WINDOW_SIZE = (1100, 900)
    HEADER_HEIGHT = 92
    PADDING = 24

    BACKGROUND = (8, 10, 24)
    WALL = (107, 66, 38)
    FORTY_TWO_COLOR = (188, 173, 88)
    TEXT = (55, 32, 20)
    MENU_TEXT = (255, 250, 205)
    MENU_SELECTED = (255, 215, 0)
    MUTED_TEXT = (155, 165, 195)
    MAIN_MENU = ["Start Game", "View Highscores", "Instructions", "Exit"]
    MENU_ARTWORK_SIZE = (921, 1152)
    MENU_CARD_CENTERS = ((466, 210), (466, 451), (466, 698), (466, 945))

    def __init__(self, data: Any, mazes: Sequence[Any]) -> None:
        levels = data["levels"]
        if len(levels) != len(mazes):
            raise ValueError(
                "Each configured level must have a generated maze"
            )
        if not levels:
            raise ValueError("At least one maze level is required")
        self.starting_lives: int = data["lives"]
        self.level_max_time: int = max(0, data["level_max_time"])
        self.blue_ghost: Any = None
        self.pink_ghost: Any = None
        self.red_ghost: Any = None
        self.orange_ghost: Any = None
        self._levels = levels
        self._mazes = mazes
        self._level_index = 0
        self.maze = self._mazes[self._level_index]
        self.player = Player(
            (
                len(self.maze.maze[0]) // 2,
                len(self.maze.maze) // 2,
            ),
            self.starting_lives,
            data["points_per_super_pacgum"],
            data["points_per_pacgum"],
        )
        self.pacgums = Pacgums(self.maze, self.player)
        self.super_pacgums = self.pacgums.super_pacgums
        self.loader = Loader(self._mazes[0])
        self.pacgums_image: Any = None
        self.player_image: Any = None
        self.super_pacgums_image: Any = None
        self.background: Any = None
        self.wall_h: Any = None
        self.wall_v: Any = None
        self.hud: Any = None
        self.life_icon: Any = None
        self.menu_image: Any = None
        self.pause_menu: Any = None
        self.game_over_image: Any = None
        self.instruction_image: Any = None
        self.start_time = 0
        self.state = "menu"
        self.selected = 0
        self.game_state = "playing"
        self.pause_start = 0
        self.pause_total_time = 0
        self.last_direction: str | None = None
        self.game_over_reason: str | None = None
        self.ghosts: list[Any] = []

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
            "assets/Bg.jpeg").convert()

        self.background = pygame.transform.scale(
            self.background, self.WINDOW_SIZE
        )
        self.wall_h = pygame.image.load(
                "assets/wall_h.png"
            ).convert_alpha()
        self.wall_v = pygame.image.load(
                "assets/wall_v.png"
            ).convert_alpha()
        self.red_ghost = pygame.image.load(
                "assets/red.png"
            ).convert_alpha()
        self.blue_ghost = pygame.image.load(
                "assets/bleu.png"
            ).convert_alpha()
        self.pink_ghost = pygame.image.load(
                "assets/pink.png"
            ).convert_alpha()
        self.orange_ghost = pygame.image.load(
                "assets/orange.png"
            ).convert_alpha()
        self.hud = pygame.image.load(
                "assets/hud.png"
            ).convert_alpha()
        self.menu_image = pygame.image.load(
                "assets/menu.png"
            ).convert_alpha()
        self.instruction_image = pygame.image.load(
                "assets/instructions.png"
            ).convert_alpha()
        self.pause_menu = pygame.image.load(
                "assets/pause_menu.png"
            ).convert_alpha()
        self.game_over_image = pygame.image.load(
                "assets/game_over.png"
            ).convert_alpha()
        try:
            self.player_image = pygame.image.load(
                "assets/player.png"
            ).convert_alpha()
        except (pygame.error, FileNotFoundError):
            print("Player image not found. Using yellow circle.")
        self.pacgums_image = pygame.image.load(
                "assets/pacgum.png"
            ).convert_alpha()
        self.super_pacgums_image = pygame.image.load(
                "assets/super_pacgum.png"
            ).convert_alpha()
        self.life_icon = pygame.image.load(
                "assets/life_icon.png"
            ).convert_alpha()
        pygame.display.set_caption("Pac-Man Maze Viewer")
        title_font = pygame.font.Font(None, 32)
        info_font = pygame.font.Font(None, 24)
        clock = pygame.time.Clock()
        last_move = pygame.time.get_ticks()
        self.start_time = last_move

        move_delay = 180
        running = True
        try:
            while running:
                now = pygame.time.get_ticks()
                if (
                    self.state == "playing"
                    and self.game_state == "playing"
                    and self._timer_expired(now)
                ):
                    self.state = "over"
                    self.game_over_reason = "time"

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        running = self._handle_key(pygame, event.key)
                now = pygame.time.get_ticks()

                if (
                    self.state == "playing"
                    and self.game_state == "playing"
                    and now - last_move >= move_delay
                ):
                    maze = self._mazes[self._level_index]
                    self.player.move(maze)
                    interaction = InteractionManager(
                        self.player,
                        self.pacgums.pacgums,
                        self.super_pacgums,
                    )
                    interaction.check_pacgum()
                    level_changed = False
                    if not self.pacgums.pacgums and not self.super_pacgums:
                        if self._level_index == len(self._mazes) - 1:
                            self.state = "victory"
                        else:
                            self._change_level(
                                self._level_index + 1, now=now
                            )
                            level_changed = True
                    last_move = now

                    # ghost collision
                    ghost_positions = set(
                        self._get_ghost_spawn_positions(maze)
                    )
                    if (
                        not level_changed
                        and interaction.check_ghost_collision(ghost_positions)
                    ):
                        if not self.player.is_alive():
                            self.game_over_reason = "lives"
                            self.state = "over"

                if self.state == "menu":
                    self._draw_main_menu(pygame, screen)
                elif self.state == "playing" and self.game_state == "pause":
                    self._draw(pygame, screen, title_font, info_font)
                    self._draw_pause_menu(pygame, screen)
                elif self.state == "playing":
                    self._draw(pygame, screen, title_font, info_font)
                elif self.state == "over":
                    self._draw(pygame, screen, title_font, info_font)
                    self._draw_game_over(pygame, screen)
                elif self.state == "victory":
                    self._draw(pygame, screen, title_font, info_font)
                    self._draw_victory(pygame, screen)
                elif self.state == "instructions":
                    self._instructions(pygame, screen)
                # elif self.state == "highscores":
                #     self._draw_highscores(pygame, screen)
                pygame.display.flip()
                clock.tick(60)
        finally:
            pygame.quit()

    def _draw(
        self, pygame: Any, screen: Any, title_font: Any, info_font: Any
    ) -> None:
        screen.blit(self.background, (0, 0))
        maze = self._mazes[self._level_index]
        level = self._levels[self._level_index]
        width = level["width"]
        height = level["height"]
        cell_size, origin_x, origin_y = self._layout(width, height)

        self._draw_cells(
            pygame, screen, maze, cell_size, origin_x, origin_y, width, height
        )
        size = int(cell_size * 0.3)
        size_super = int(cell_size * 0.7)
        image = pygame.transform.scale(self.pacgums_image, (size, size))
        image_super = pygame.transform.scale(
            self.super_pacgums_image, (size_super, size_super))
        for k, p in self.super_pacgums:
            center_x = origin_x + k * cell_size + cell_size // 2
            center_y = origin_y + p * cell_size + cell_size // 2
            screen.blit(image_super, (center_x - size_super //
                        2, center_y - size_super // 2))

        for x, y in self.pacgums.pacgums:
            center_x = origin_x + x * cell_size + cell_size // 2
            center_y = origin_y + y * cell_size + cell_size // 2
            screen.blit(image, (center_x - size // 2, center_y - size // 2))
        self._draw_ghosts(
            pygame, screen, cell_size, origin_x, origin_y, maze
        )
        self._draw_player(pygame, screen, cell_size, origin_x, origin_y)
        self._draw_menu(pygame, screen)

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
        origin_y = 30 + (
            window_height - maze_height
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
                walls = maze.maze[y][x]
                floor_color = (
                    self.FORTY_TWO_COLOR
                    if walls == 15
                    else (230, 210, 180, 180)
                )
                floor_surface.fill(floor_color)
                screen.blit(floor_surface, (left, top))
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

    def _draw_menu(self, pygame: Any, screen: Any) -> None:

        images = [
            self.hud,
            self.hud,
            self.hud,
            self.hud,
        ]
        now = (
            self.pause_start
            if self.game_state == "pause"
            else pygame.time.get_ticks()
        )
        elapsed = min(self._elapsed_seconds(now), self.level_max_time)

        values = [
            "",
            f"Score: {self.player.score}",
            f"Level: {self._level_index + 1}",
            f"Time: {elapsed}/{self.level_max_time}"
        ]

        font = pygame.font.Font(None, 28)

        panel_width = 220
        panel_height = 60
        gap = 20

        start_x = (
            self.WINDOW_SIZE[0]
            - (4 * panel_width + 3 * gap)
        ) // 2

        y = 25

        for i in range(4):
            panel = pygame.transform.scale(
                images[i], (panel_width, panel_height)
            )

            x = start_x + i * (panel_width + gap)

            screen.blit(panel, (x, y))

            # life icon logic
            if i == 0:
                label = font.render("Lives:", True, self.TEXT)
                icon_size = 30
                icon_gap = 4
                life_count = max(0, self.player.lives)
                icons_width = (
                    life_count * icon_size
                    + max(0, life_count - 1) * icon_gap
                )
                content_width = label.get_width() + 8 + icons_width
                content_x = x + (panel_width - content_width) // 2
                label_rect = label.get_rect(
                    midleft=(content_x, y + panel_height // 2)
                )
                screen.blit(label, label_rect)

                for life in range(life_count):
                    icon = pygame.transform.smoothscale(
                        self.life_icon, (icon_size, icon_size)
                    )
                    icon_rect = icon.get_rect(
                        midleft=(
                            label_rect.right + 8
                            + life * (icon_size + icon_gap),
                            y + panel_height // 2,
                        )
                    )
                    screen.blit(icon, icon_rect)
                continue

            text = font.render(values[i], True, self.TEXT)

            text_rect = text.get_rect(
                center=(
                    x + panel_width // 2,
                    y + panel_height // 2,
                )
            )

            screen.blit(text, text_rect)

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
        protected = self.player.is_respawn_protected()

        if self.player_image is not None:
            size = int(cell_size * 0.8)
            image = pygame.transform.scale(
                self.player_image, (size, size)
            )
            if protected:
                image.set_alpha(150)
            rect = image.get_rect(
                center=(round(center_x), round(center_y))
            )
            screen.blit(image, rect)
        else:
            pygame.draw.circle(
                screen,
                (255, 255, 255) if protected else (255, 220, 0),
                (round(center_x), round(center_y)),
                radius,
            )

    def _inside(self, maze: Any, x: int, y: int) -> bool:
        return 0 <= y < len(maze.maze) and 0 <= x < len(maze.maze[0])

    def _draw_ghosts(
        self,
        pygame: Any,
        screen: Any,
        cell_size: int,
        origin_x: int,
        origin_y: int,
        maze: Any,
    ) -> None:
        size = int(cell_size * 0.8)
        sprites = (
            self.red_ghost,
            self.pink_ghost,
            self.blue_ghost,
            self.orange_ghost,
        )
        for (x, y), sprite in zip(
            self._get_ghost_spawn_positions(maze), sprites
        ):
            center_x = origin_x + x * cell_size + cell_size // 2
            center_y = origin_y + y * cell_size + cell_size // 2
            image = pygame.transform.scale(sprite, (size, size))
            screen.blit(
                image, (center_x - size // 2, center_y - size // 2)
            )

    def _get_ghost_spawn_positions(
        self, maze: Any
    ) -> list[tuple[int, int]]:
        N, E, S, W = 1, 2, 4, 8
        ghosts_positions: list[tuple[int, int]] = []

        def cell(x: int, y: int) -> Any:
            return maze.maze[y][x]
        width = len(maze.maze[0])
        height = len(maze.maze)

        x1, y1 = (0, 0)
        if self._inside(maze, x1 + 1, y1) and not cell(x1, y1) & E:
            x_red, y_red = x1 + 1, y1
        elif self._inside(maze, x1, y1 + 1) and not cell(x1, y1) & S:
            x_red, y_red = x1, y1 + 1
        else:
            x_red, y_red = x1 + 1, y1 + 1
        ghosts_positions.append((x_red, y_red))

        x2, y2 = (width - 1, 0)
        if self._inside(maze, x2 - 1, y2) and not cell(x2, y2) & W:
            x_pink, y_pink = x2 - 1, y2
        elif self._inside(maze, x2, y2 + 1) and not cell(x2, y2) & S:
            x_pink, y_pink = x2, y2 + 1
        else:
            x_pink, y_pink = x2 - 1, y2 + 1
        ghosts_positions.append((x_pink, y_pink))

        x3, y3 = (width-1, height - 1)
        if self._inside(maze, x3 - 1, y3) and not cell(x3, y3) & W:
            x_blue, y_blue = x3 - 1, y3
        elif self._inside(maze, x3, y3 - 1) and not cell(x3, y3) & N:
            x_blue, y_blue = x3, y3 - 1
        else:
            x_blue, y_blue = x3 - 1, y3 - 1
        ghosts_positions.append((x_blue, y_blue))

        x4, y4 = 0, height-1
        if self._inside(maze, x4 + 1, y4) and not cell(x4, y4) & E:
            x_orange, y_orange = x4 + 1, y4
        elif self._inside(maze, x4, y4 - 1) and not cell(x4, y4) & N:
            x_orange, y_orange = x4, y4 - 1
        else:
            x_orange, y_orange = x4 + 1, y4 - 1
        ghosts_positions.append((x_orange, y_orange))
        return ghosts_positions
