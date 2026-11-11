"""Input handling and game-state helpers of the maze viewer."""

from __future__ import annotations
from collections.abc import Sequence
from engine.pacgums import Pacgums
from maze.highscore import MAX_PLAYER_NAME_LENGTH
from typing import Any
from engine.ghost import Ghost
import pygame
from engine.cheat_mode import CheatMode


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
    ghosts: list[Ghost]
    highscore_manager: Any
    name_entry: str
    name_entry_return_state: str
    name_entry_pending: bool
    cheat_mode: CheatMode
    sound_manager: Any


    def _handle_key(
        self, pygame: Any, key: int, text: str = ""
    ) -> bool:
        if self.state == "name_entry":
            if key == pygame.K_ESCAPE:
                self.state = self.name_entry_return_state
            elif key == pygame.K_RETURN:
                self._save_name_entry()
            elif key == pygame.K_BACKSPACE:
                self.name_entry = self.name_entry[:-1]
            elif (
                text.isascii()
                and (text.isalnum() or text == " ")
                and len(self.name_entry) < MAX_PLAYER_NAME_LENGTH
            ):
                self.name_entry += text.upper()
            return True

        if key == pygame.K_m:
            self.sound_manager.toggle_music()
            return True

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
                self.sound_manager.play("menu_move")
            elif key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % 4
                self.sound_manager.play("menu_move")
            elif key == pygame.K_RETURN:
                self.sound_manager.play("menu_select")
                if self.selected == 0:
                    self._reset_game()
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
            if key == pygame.K_RETURN and self.name_entry_pending:
                self.name_entry = ""
                self.state = "name_entry"
            elif key in (pygame.K_RETURN, pygame.K_ESCAPE):
                self._reset_game()
                self.state = "menu"
            elif key == pygame.K_q:
                return False
            return True

        if self.state == "victory":
            if key == pygame.K_RETURN and self.name_entry_pending:
                self.name_entry = ""
                self.state = "name_entry"
            elif key == pygame.K_RETURN:
                self._reset_game()
                self.state = "playing"
            elif key == pygame.K_ESCAPE:
                self._reset_game()
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

        if self.state == "playing" and key == pygame.K_ESCAPE:
            if self.game_state == "playing":
                self.last_direction = self.player.direction
                self.player.direction = None
                self.pause_start = pygame.time.get_ticks()
                self.game_state = "pause"
                self.sound_manager.pause_music()
            return True
        if self.state == "playing" and key == pygame.K_q:
            self.state = "menu"
            if self.cheat_mode.active:
                self.cheat_mode.cheate_mode_active()
                self._reset_cheat_modes()
            return True
        if key == pygame.K_ESCAPE:
            self.state = "menu"
            return True
        if key == pygame.K_q:
            return False
        if key == pygame.K_c:
            if self.cheat_mode.active:
                self._reset_cheat_modes()
            self.cheat_mode.cheate_mode_active()
        if self.cheat_mode.active:
            if key == pygame.K_f:
                self.cheat_mode.toggle_freeze()
                return True
            elif key == pygame.K_i:
                self.cheat_mode.toggle_infinite_lives()
                return True
            elif key == pygame.K_v:
                self.cheat_mode.toggle_invincibility()
                return True
            elif key == pygame.K_n:
                self.cheat_mode.level_skip = True
                index = self._level_index + 1
                if self._level_index == len(self._mazes) - 1:
                    self._start_end_state("victory")
                else:
                    self._change_level(index)
                return True
        elif (
            key == pygame.K_p
            and self.state == "playing"
            and self.game_state == "playing"
        ):
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

    def _start_end_state(self, state: str) -> None:
        """Show the end screen before asking for the player's name."""

        self.name_entry_return_state = state
        self.name_entry_pending = True
        self.name_entry = ""
        self.state = state

    def _save_name_entry(self) -> None:
        """Persist the entered name and open the highscores screen."""

        name = self.name_entry.strip() or "PLAYER"
        self.highscore_manager.record(name, self.player.score)
        self.name_entry_pending = False
        self.state = "highscores"

    def _reset_cheat_modes(self) -> None:
        if self.cheat_mode.infinite_lives:
            self.cheat_mode.toggle_infinite_lives()
        if self.cheat_mode.freeze:
            self.cheat_mode.toggle_freeze()
        if self.cheat_mode.invincibility:
            self.cheat_mode.toggle_invincibility()
        if self.cheat_mode.level_skip:
            self.cheat_mode.level_skip = False

    def _reset_game(self) -> None:
        self._change_level(0)
        self.player.lives = self.starting_lives
        self.player.score = 0
        self.player.direction = None
        self.game_state = "playing"
        self.pause_start = 0
        self.pause_total_time = 0
        self.last_direction = None
        self.game_over_reason = None
        self.name_entry_pending = False
        self.start_time = pygame.time.get_ticks()

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
        self.start_ghosts_positions = self._get_ghost_spawn_positions(
            self.maze
        )
        for ghost, position in zip(self.ghosts, self.start_ghosts_positions):
            ghost.current_pos = position
            ghost.spawn_pos = position

        self.player.direction = None
        self.pacgums = Pacgums(self.maze, self.player)
        self.super_pacgums = self.pacgums.super_pacgums
        pause_start = (
            now if now is not None and self.game_state == "pause" else 0
        )
        self.pause_start = pause_start
        self.pause_total_time = 0
        self.last_direction = None
        # if now is not None:
        #     self.start_time = now
        self.start_time = pygame.time.get_ticks()
