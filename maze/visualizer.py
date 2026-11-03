"""Pygame display for the generated maze levels."""

from __future__ import annotations
from engine.pacgums import Pacgums
from engine.interactions import InteractionManager
from collections.abc import Mapping, Sequence
from typing import Any
from engine.player import Player
from maze.highscore import HighscoreManager
from maze.game_logic import GameMixin
from maze.screens import ScreensMixin
from engine.ghost import Ghost
from engine.cheat_mode import CheatMode
from audio.sound_manager import SoundManager


Level = Mapping[str, Any]


class MazeViewer(GameMixin, ScreensMixin):
    """Display configured mazes one level at a time."""

    WINDOW_SIZE = (1100, 900)
    FRIGHTENED_DURATION = 10000
    EATEN_TIME = 4000

    HEADER_HEIGHT = 92
    PADDING = 24
    PLAYER_SPEED = 6.0
    # Ghost decisions happen every 450 ms, so this carries each ghost across
    # one cell without stopping between targets.
    GHOST_SPEED = 2.2

    BACKGROUND = (8, 10, 24)
    WALL = (107, 66, 38)
    FORTY_TWO_COLOR = (188, 173, 88)
    TEXT = (55, 32, 20)
    MENU_TEXT = (255, 250, 205)
    MENU_SELECTED = (255, 215, 0)
    MUTED_TEXT = (155, 165, 195)
    MAIN_MENU = ["Start Game", "View Highscores", "Instructions", "Exit"]

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
        self.highscore_manager = HighscoreManager(data["highscore_filename"])
        self.name_entry = ""
        self.name_entry_return_state = "over"
        self.name_entry_pending = False
        self._level_index = 0
        self.maze = self._mazes[self._level_index]
        self.player = Player(
            (
                len(self.maze.maze[0]) // 2,
                len(self.maze.maze) // 2,
            ),
            self.starting_lives,
            data["points_per_super_pacgum"],
            data["points_per_pacgum"], data["points_per_ghost"]
        )
        self.pacgums = Pacgums(self.maze, self.player)
        self.super_pacgums = self.pacgums.super_pacgums
        self.pacgums_image: Any = None
        self.player_image: Any = None
        self.frightened_ghost: Any = None
        self.super_pacgums_image: Any = None
        self.background: Any = None
        self.video_background: Any = None
        self.wall_h: Any = None
        self.wall_v: Any = None
        self.hud: Any = None
        self.life_icon: Any = None
        self.menu_image: Any = None
        self.pause_menu: Any = None
        self.game_over_image: Any = None
        self.highscore_title: Any = None
        self.highscore_panel: Any = None
        self.instruction_image: Any = None
        self.start_time = 0
        self.state = "menu"
        self.selected = 0
        self.game_state = "playing"
        self.pause_start = 0
        self.pause_total_time = 0
        self.game_over_time: int | None = None
        self.last_direction: str | None = None
        self.game_over_reason: str | None = None
        self.title: Any = None
        self.start_ghosts_positions = self._get_ghost_spawn_positions(
            self.maze
        )
        self.ghosts = [
            Ghost(
                "red", None, self.start_ghosts_positions[0]
            ),
            Ghost(
                "pink", None, self.start_ghosts_positions[1]
            ),
            Ghost(
                "blue", None, self.start_ghosts_positions[2]
            ),
            Ghost(
                "orange", None, self.start_ghosts_positions[3]
            ),
        ]
        self.player_render_pos: Any = None
        self.ghost_render_positions: list[Any] = []
        self.cheat_mode = CheatMode()
        self.sound_manager = SoundManager()
        self._last_sound_state: str | None = None

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
        self.sound_manager.load()
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
        self.highscore_title = pygame.image.load(
                "assets/highscore_title.png"
            ).convert_alpha()
        self.highscore_panel = pygame.image.load(
                "assets/highscore_panel.png"
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
        self.frightened_ghost = pygame.image.load(
                "assets/edible.png"
            ).convert_alpha()
        self.title = pygame.image.load(
                "assets/cheat_mode.png"
            ).convert_alpha()
        pygame.display.set_caption("Pac-Man Maze Viewer")
        title_font = pygame.font.Font(None, 32)
        info_font = pygame.font.Font(None, 24)
        clock = pygame.time.Clock()
        last_move = pygame.time.get_ticks()
        self.start_time = last_move
        last_ghost_move = 0
        ghost_move_delay = 450
        move_delay = 160
        running = True

        try:
            while running:
                delta_time = clock.tick(60) / 1000.0
                now = pygame.time.get_ticks()
                if (
                    self.state == "playing"
                    and self.game_state == "playing"
                    and self._timer_expired(now)
                ):
                    self.game_over_reason = "time"
                    self.game_over_time = now // 1000
                    self._start_end_state("over")

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        running = self._handle_key(
                            pygame, event.key, event.unicode
                        )

                if self.state != self._last_sound_state:
                    if self.state == "menu":
                        self.sound_manager.play("menu_jingle")
                    elif self.state == "over":
                        self.sound_manager.play("game_over")
                    self._last_sound_state = self.state

                player_moved = False
                ghost_moved = False
                level_changed = False
                maze = self._mazes[self._level_index]

                if (
                    self.state == "playing"
                    and self.game_state == "playing"
                    and now - last_ghost_move >= ghost_move_delay
                ):
                    for index, ghost in enumerate(self.ghosts):
                        if ghost.is_eaten:
                            if now - ghost.eaten_time >= self.EATEN_TIME:
                                ghost.state = "chase"
                                ghost.current_pos = ghost.spawn_pos
                                self.ghost_render_positions[index] = (
                                    pygame.Vector2(ghost.spawn_pos)
                                )
                                ghost.is_eaten = False
                            continue
                        if (
                            ghost.state == "Frightened"
                            and now - ghost.frightened_time
                            >= self.FRIGHTENED_DURATION
                        ):
                            ghost.state = "chase"
                        if ghost.state == "Frightened":
                            target = ghost.get_escape_move(
                                maze, self.player.current_pos
                            )
                        else:
                            target = ghost.get_target_position(
                                self.player, self.ghosts[0], maze
                            )
                        next_pos = ghost.move(maze, target)
                        if next_pos is not None:
                            ghost.current_pos = next_pos
                    last_ghost_move = now
                    ghost_moved = True

                if (
                    self.state == "playing"
                    and self.game_state == "playing"
                    and now - last_move >= move_delay
                ):
                    self.player.move(maze)
                    interaction = InteractionManager(
                        self.player,
                        self.pacgums.pacgums,
                        self.super_pacgums,
                        self.sound_manager,
                    )
                    interaction.check_pacgum(self.ghosts)
                    if not self.pacgums.pacgums:
                        self.sound_manager.play("level_clear")
                        if self._level_index == len(self._mazes) - 1:
                            self._start_end_state("victory")
                        else:
                            self._change_level(
                                self._level_index + 1, now=now
                            )
                            level_changed = True
                    last_move = now

                    player_moved = True

                if (player_moved or ghost_moved) and not level_changed:
                    interaction = InteractionManager(
                        self.player,
                        self.pacgums.pacgums,
                        self.super_pacgums,
                        self.sound_manager,
                    )
                    if interaction.check_ghost_collision(self.ghosts):
                        if not self.player.is_alive():
                            self.game_over_reason = "lives"

                            self.game_over_time = now // 1000
                            self._start_end_state("over")

                if self.state in (
                    "menu", "highscores", "instructions", "playing"
                ):
                    self.sound_manager.play_music()
                else:
                    self.sound_manager.stop_music()

                self._update_render_positions(pygame, delta_time)

                if self.state == "menu":
                    self._draw_main_menu(pygame, screen)
                elif self.state == "playing" and self.game_state == "pause":
                    self._draw(pygame, screen, title_font, info_font)
                    self._draw_pause_menu(pygame, screen)
                elif self.state == "playing":
                    if self.cheat_mode.infini_lives:
                        self.player.lives = 3

                    self._draw(pygame, screen, title_font, info_font)
                elif self.state == "over":
                    self._draw(pygame, screen, title_font, info_font)
                    self._draw_game_over(pygame, screen)
                elif self.state == "victory":
                    self._draw(pygame, screen, title_font, info_font)
                    self._draw_victory(pygame, screen)
                elif self.state == "instructions":
                    self._instructions(pygame, screen)
                elif self.state == "highscores":
                    self._draw_highscores(pygame, screen)
                elif self.state == "name_entry":
                    self._draw_name_entry(pygame, screen)
                pygame.display.flip()
        finally:
            if self.video_background is not None:
                self.video_background.stop()
            self.sound_manager.stop_music()
            pygame.quit()

    def _update_render_positions(
        self, pygame: Any, delta_time: float
    ) -> None:
        player_target = pygame.Vector2(self.player.current_pos)
        if self.player_render_pos is None:
            self.player_render_pos = player_target
        elif self.player_render_pos.distance_to(player_target) > 1.5:
            self.player_render_pos = player_target
        else:
            self.player_render_pos = self.player_render_pos.move_towards(
                player_target, self.PLAYER_SPEED * delta_time
            )

        while len(self.ghost_render_positions) < len(self.ghosts):
            index = len(self.ghost_render_positions)
            self.ghost_render_positions.append(
                pygame.Vector2(self.ghosts[index].current_pos)
            )

        for index, ghost in enumerate(self.ghosts):
            ghost_target = pygame.Vector2(ghost.current_pos)
            render_pos = self.ghost_render_positions[index]
            if render_pos.distance_to(ghost_target) > 1.5:
                self.ghost_render_positions[index] = ghost_target
            else:
                self.ghost_render_positions[index] = render_pos.move_towards(
                    ghost_target, self.GHOST_SPEED * delta_time
                )

    def _draw(
        self, pygame: Any, screen: Any, title_font: Any, info_font: Any
    ) -> None:
        self._draw_background(pygame, screen)
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
            pygame, screen, cell_size, origin_x, origin_y
        )
        self._draw_player(pygame, screen, cell_size, origin_x, origin_y)
        self._draw_menu(pygame, screen)
        if self.cheat_mode.infini_lives:
            title = pygame.transform.scale(self.title, (500, 400))
            center = (self.WINDOW_SIZE[0] // 2, self.WINDOW_SIZE[1] - 20)
            title_rect = title.get_rect(center=center)
            screen.blit(title, title_rect)

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
        if self.state == "over":
            elapsed = self.game_over_time
        elif self.game_state == "pause":
            elapsed = (
                self.pause_start - self.start_time - self.pause_total_time
            ) // 1000
        else:
            elapsed = (
                pygame.time.get_ticks()
                - self.pause_total_time
                - self.start_time
            ) // 1000

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
        render_pos = self.player_render_pos
        if render_pos is None:
            render_pos = pygame.Vector2(self.player.current_pos)

        center_x = origin_x + (render_pos.x + 0.5) * cell_size
        center_y = origin_y + (render_pos.y + 0.5) * cell_size

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

    def _draw_ghosts(
        self,
        pygame: Any,
        screen: Any,
        cell_size: int,
        origin_x: int,
        origin_y: int,

    ) -> None:
        size = int(cell_size * 0.8)
        for index, ghost in enumerate(self.ghosts):
            if ghost.is_eaten:
                continue
            color = ghost.color
            if index < len(self.ghost_render_positions):
                render_pos = self.ghost_render_positions[index]
            else:
                render_pos = pygame.Vector2(ghost.current_pos)
            center_x = origin_x + (render_pos.x + 0.5) * cell_size
            center_y = origin_y + (render_pos.y + 0.5) * cell_size

            if ghost.state == "Frightened":
                sprite = self.frightened_ghost
            elif color == "red":
                sprite = self.red_ghost
            elif color == "pink":
                sprite = self.pink_ghost
            elif color == "orange":
                sprite = self.orange_ghost
            elif color == "blue":
                sprite = self.blue_ghost

            image = pygame.transform.scale(sprite, (size, size))
            screen.blit(image, (center_x - size // 2, center_y - size // 2))

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
