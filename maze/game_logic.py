"""Input handling and game-state helpers of the maze viewer."""

from __future__ import annotations
from collections.abc import Sequence
from engine.pacgums import Pacgums
from typing import Any


class GameMixin:
    """Key handling, level changes, timer and reset logic."""

    _mazes: Sequence[Any]
    _level_index: int
    maze: Any
    player: Any
    pacgums: Any
    super_pacgums: Any
    starting_lives: int
    level_max_time: int
    start_time: int
    state: str
    selected: int
    game_state: str
    pause_start: int
    pause_total_time: int
    last_direction: str | None
    game_over_reason: str | None

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

        if self.state == "menu":
            if key == pygame.K_UP:
                self.selected = (self.selected - 1) % 4
            elif key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % 4
            elif key == pygame.K_RETURN:
                if self.selected == 0:
                    self._reset_game(pygame)
                    self.state = "playing"
                elif self.selected == 1:
                    self.state = "highscores"
                elif self.selected == 2:
                    self.state = "instructions"
                else:
                    return False
            elif key in (pygame.K_ESCAPE, pygame.K_q):
                return False
            return True

        if self.state == "over":
            if key in (pygame.K_RETURN, pygame.K_ESCAPE):
                self._reset_game(pygame)
                self.state = "menu"
            elif key == pygame.K_q:
                return False
            return True

        if self.state == "victory":
            if key == pygame.K_RETURN:
                self._reset_game(pygame)
                self.state = "playing"
            elif key == pygame.K_ESCAPE:
                self._reset_game(pygame)
                self.state = "menu"
            elif key == pygame.K_q:
                return False
            return True

        if self.state in ("instructions", "highscores"):
            if key in (
                pygame.K_ESCAPE,
                pygame.K_q,
                pygame.K_RETURN,
                pygame.K_BACKSPACE,
            ):
                self.state = "menu"
            return True

        if key == pygame.K_ESCAPE:
            self.state = "menu"
            return True
        if key == pygame.K_q:
            return False
        if key == pygame.K_n:
            index = (self._level_index + 1) % len(self._mazes)
            self._change_level(index)
            return True
        elif key == pygame.K_b:
            index = (self._level_index - 1) % len(self._mazes)
            self._change_level(index)
            return True
        elif key == pygame.K_p and self.state == "playing":
            self.last_direction = self.player.direction
            self.player.direction = None
            self.pause_start = pygame.time.get_ticks()
            self.game_state = "pause"
            return True
        elif key == pygame.K_1 and self.game_state == "pause":
            self.pause_total_time += pygame.time.get_ticks() - self.pause_start
            self.game_state = "playing"
            self.player.direction = self.last_direction
            return True
        elif key == pygame.K_2 and self.game_state == "pause":
            self._change_level(0)
            self.player.score = 0
            self.game_state = "playing"
            self.state = "menu"
            return True
        if key in moves and self.game_state == "playing":
            self.player.direction = moves[key]
        return True

    def _reset_game(self, pygame: Any) -> None:
        self._change_level(0)
        self.player.lives = self.starting_lives
        self.player.score = 0
        self.player.direction = None
        self.game_state = "playing"
        self.pause_start = 0
        self.pause_total_time = 0
        self.last_direction = None
        self.game_over_reason = None
        self.player.clear_respawn_protection()
        self.start_time = pygame.time.get_ticks()

    def _elapsed_seconds(self, now: int) -> int:
        active_milliseconds = max(
            0, now - self.start_time - self.pause_total_time
        )
        return active_milliseconds // 1000

    def _timer_expired(self, now: int) -> bool:
        return bool(
            now - self.start_time - self.pause_total_time
            >= self.level_max_time * 1000
        )

    def _change_level(self, index: int, now: int | None = None) -> None:
        self._level_index = index
        self.maze = self._mazes[index]
        self.player.start_position = (
            len(self.maze.maze[0]) // 2, len(self.maze.maze) // 2)
        self.player.current_pos = self.player.start_position
        self.player.direction = None
        self.player.clear_respawn_protection()

        self.pacgums = Pacgums(self.maze, self.player)
        self.super_pacgums = self.pacgums.super_pacgums
        pause_start = (
            now if now is not None and self.game_state == "pause" else 0
        )
        self.pause_start = pause_start
        self.pause_total_time = 0
        self.last_direction = None
        if now is not None:
            self.start_time = now
