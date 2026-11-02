"""Full-screen views: menu, instructions, pause, game over, victory."""

from __future__ import annotations
from typing import Any


class ScreensMixin:
    """Draw the non-gameplay screens and overlays."""

    WINDOW_SIZE: tuple[int, int]
    MAIN_MENU: list[str]
    MENU_SELECTED: tuple[int, int, int]
    MENU_TEXT: tuple[int, int, int]
    MUTED_TEXT: tuple[int, int, int]
    background: Any
    video_background: Any
    instruction_image: Any
    pause_menu: Any
    game_over_image: Any
    menu_image: Any
    highscore_title: Any
    highscore_panel: Any
    game_over_reason: str | None
    _mazes: Any
    player: Any
    highscore_manager: Any
    selected: int
    name_entry: str

    def _inside(self, maze: Any, x: int, y: int) -> bool:
        return 0 <= y < len(maze.maze) and 0 <= x < len(maze.maze[0])

    def _draw_background(self, pygame: Any, screen: Any) -> None:
        if (
            self.video_background is None
            or not self.video_background.draw(screen)
        ):
            screen.blit(self.background, (0, 0))

    def _instructions(self, pygame: Any, screen: Any) -> None:
        self._draw_background(pygame, screen)
        center_x = self.WINDOW_SIZE[0] // 2
        center_y = self.WINDOW_SIZE[1] // 2

        image = pygame.transform.scale(
            self.instruction_image, (700, 600)
        )
        rect = image.get_rect(
            center=(round(center_x), round(center_y))
        )
        screen.blit(image, rect)

    def _draw_pause_menu(self, pygame: Any, screen: Any) -> None:

        surface = pygame.Surface(
                screen.get_size(), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 130))
        screen.blit(surface, (0, 0))
        image = pygame.transform.scale(self.pause_menu, (900, 200))
        rect = image.get_rect(
            center=(round(self.WINDOW_SIZE[0] // 2),
                    round(self.WINDOW_SIZE[1] // 2))
        )
        screen.blit(image, rect)

    def _draw_game_over(self, pygame: Any, screen: Any) -> None:
        surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 160))
        screen.blit(surface, (0, 0))

        if self.game_over_reason == "time":
            image = pygame.transform.smoothscale(
                self.game_over_image, (900, 200)
            )
            rect = image.get_rect(
                center=(self.WINDOW_SIZE[0] // 2, self.WINDOW_SIZE[1] // 2)
            )
            screen.blit(image, rect)

            artwork_fill = (47, 24, 23)
            title_area = pygame.Rect(rect.left + 292, rect.top + 5, 316, 43)
            message_area = pygame.Rect(rect.left + 155, rect.top + 65, 590, 88)
            pygame.draw.rect(screen, artwork_fill, title_area)
            pygame.draw.rect(screen, artwork_fill, message_area)

            title_font = pygame.font.SysFont("dejavusans", 38, bold=True)
            body_font = pygame.font.SysFont("dejavusans", 25, bold=True)
            hint_font = pygame.font.SysFont("dejavusans", 19)
            title = title_font.render("GAME OVER", True, (255, 226, 228))

            message = body_font.render(
                "TIME'S UP!",
                True,
                (255, 248, 245),
            )
            hint = hint_font.render(
                "Press ENTER to return to the main menu",
                True,
                (231, 190, 193),
            )
            center_x = self.WINDOW_SIZE[0] // 2

            screen.blit(
                title,
                title.get_rect(center=(center_x, rect.top + 26)),
            )
            screen.blit(
                message,
                message.get_rect(center=(center_x, rect.top + 101)),
            )
            screen.blit(
                hint,
                hint.get_rect(center=(center_x, rect.top + 131)),
            )
            return

        image = pygame.transform.smoothscale(self.game_over_image, (900, 200))
        rect = image.get_rect(
            center=(self.WINDOW_SIZE[0] // 2, self.WINDOW_SIZE[1] // 2)
        )
        screen.blit(image, rect)

    def _draw_victory(self, pygame: Any, screen: Any) -> None:
        """Draw the final completion screen after every level is cleared."""

        surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        surface.fill((25, 14, 20, 150))
        screen.blit(surface, (0, 0))

        # Keep the victory screen in the same Sakura-styled visual language as
        # the highscores and name-entry screens instead of introducing a
        # one-off flat panel.
        panel = pygame.transform.smoothscale(
            self.highscore_panel, (820, 680)
        )
        panel_rect = panel.get_rect(
            center=(self.WINDOW_SIZE[0] // 2, self.WINDOW_SIZE[1] // 2)
        )
        screen.blit(panel, panel_rect)

        center_x = self.WINDOW_SIZE[0] // 2

        def outlined_text(
            text: str,
            font: Any,
            center: tuple[int, int],
            fill: tuple[int, int, int],
        ) -> None:
            """Render the outlined lettering used by the other themed views."""

            rendered = font.render(text, True, fill)
            shadow = font.render(text, True, (57, 28, 31))
            rect = rendered.get_rect(center=center)
            for offset in ((4, 5), (3, 3), (-2, 2), (2, -2)):
                screen.blit(shadow, rect.move(*offset))
            screen.blit(rendered, rect)

        title_font = pygame.font.SysFont("dejavusans", 58, bold=True)
        heading_font = pygame.font.SysFont("dejavusans", 27, bold=True)
        score_font = pygame.font.SysFont("dejavusans", 34, bold=True)
        hint_font = pygame.font.SysFont("lora", 22)

        outlined_text(
            "VICTORY!",
            title_font,
            (center_x, panel_rect.top + 84),
            (249, 191, 198),
        )
        outlined_text(
            f"ALL {len(self._mazes)} LEVELS CLEARED",
            heading_font,
            (center_x, panel_rect.top + 252),
            (255, 224, 220),
        )
        outlined_text(
            f"SCORE  {self.player.score:06d}",
            score_font,
            (center_x, panel_rect.top + 330),
            self.MENU_TEXT,
        )

        hint = hint_font.render(
            "ENTER to play again  ·  ESC to return to menu",
            True,
            (231, 190, 193),
        )
        screen.blit(
            hint,
            hint.get_rect(center=(center_x, panel_rect.bottom - 43)),
        )

    def _draw_main_menu(self, pygame: Any, screen: Any) -> None:
        cord = [(547, 189), (558, 360), (543, 528), (555, 700)]
        self._draw_background(pygame, screen)
        center_x = self.WINDOW_SIZE[0] // 2
        center_y = self.WINDOW_SIZE[1] // 2

        size = 800
        image = pygame.transform.scale(
            self.menu_image, (size, size)
        )
        rect = image.get_rect(
            center=(round(center_x), round(center_y))
        )
        screen.blit(image, rect)
        for i in range(4):
            font = pygame.font.Font(None, 50)
            if i == self.selected:
                text = font.render(self.MAIN_MENU[i], True, (255, 215, 0))
            else:
                text = font.render(self.MAIN_MENU[i], True, (255, 250, 205))
            text_rect = text.get_rect(
                center=cord[i]

            )
            screen.blit(text, text_rect)

        # signature message
        credit_font = pygame.font.SysFont("lora", 20)
        credit = credit_font.render(
            "Created by mezahir and aymouate",
            True,
            (255, 250, 205),
        )
        credit_rect = credit.get_rect(
            center=(center_x, self.WINDOW_SIZE[1] - 22)
        )
        screen.blit(credit, credit_rect)

    def _draw_highscores(self, pygame: Any, screen: Any) -> None:
        """Draw the shared leaderboard loaded from the high-score file."""

        screen.blit(self.background, (0, 0))
        title = pygame.transform.smoothscale(
            self.highscore_title, (820, 159)
        )
        title_rect = title.get_rect(center=(550, 138))
        screen.blit(title, title_rect)

        panel = pygame.transform.smoothscale(
            self.highscore_panel, (780, 640)
        )
        panel_rect = panel.get_rect(center=(550, 540))
        screen.blit(panel, panel_rect)

        title_font = pygame.font.SysFont("dejavusans", 28, bold=True)
        body_font = pygame.font.SysFont("dejavusans", 25, bold=True)
        hint_font = pygame.font.SysFont("lora", 24)

        # Reload when the page is opened so scores written by another process
        # are visible without restarting the game.
        entries = self.highscore_manager.load()

        heading_y = panel_rect.top + 75
        heading_player = title_font.render(
            "RANK  PLAYER", True, (255, 224, 220)
        )
        heading_score = title_font.render(
            "SCORE", True, (255, 224, 220)
        )
        screen.blit(
            heading_player,
            heading_player.get_rect(
                left=panel_rect.left + 150,
                centery=heading_y,
            ),
        )
        screen.blit(
            heading_score,
            heading_score.get_rect(
                right=panel_rect.right - 150,
                centery=heading_y,
            ),
        )

        if entries:
            first_row_y = panel_rect.top + 165
            row_height = 39
            for rank, entry in enumerate(entries, start=1):
                rank_text = body_font.render(
                    f"{rank:>2}.", True, self.MENU_TEXT
                )
                name_text = body_font.render(
                    entry.name, True, self.MENU_TEXT
                )
                score_text = body_font.render(
                    f"{entry.score:>6}", True, self.MENU_TEXT
                )
                rank_rect = rank_text.get_rect(
                    left=panel_rect.left + 150,
                    centery=first_row_y,
                )
                score_rect = score_text.get_rect(
                    right=panel_rect.right - 150,
                    centery=first_row_y,
                )
                screen.blit(rank_text, rank_rect)
                screen.blit(
                    name_text,
                    name_text.get_rect(
                        left=rank_rect.right + 14,
                        centery=first_row_y,
                    ),
                )
                screen.blit(score_text, score_rect)
                first_row_y += row_height
        else:
            empty = body_font.render(
                "NO SCORES YET", True, self.MENU_TEXT
            )
            screen.blit(
                empty,
                empty.get_rect(center=(550, panel_rect.top + 245)),
            )

        hint = hint_font.render(
            "Press Enter or Esc to return", True, (231, 190, 193)
        )
        screen.blit(
            hint,
            hint.get_rect(center=(550, panel_rect.bottom - 43)),
        )

    def _draw_name_entry(self, pygame: Any, screen: Any) -> None:
        """Draw the Sakura-styled name entry screen for a new high score."""

        screen.blit(self.background, (0, 0))

        title_font = pygame.font.SysFont("dejavusans", 56, bold=True)
        heading_font = pygame.font.SysFont("dejavusans", 27, bold=True)
        body_font = pygame.font.SysFont("Pacifico", 22)
        score_font = pygame.font.SysFont("dejavusans", 32, bold=True)
        hint_font = pygame.font.SysFont("lora", 22)

        def outlined_text(
            text: str,
            font: Any,
            center: tuple[int, int],
            fill: tuple[int, int, int],
        ) -> None:
            rendered = font.render(text, True, fill)
            shadow = font.render(text, True, (57, 28, 31))
            rect = rendered.get_rect(center=center)
            for offset in ((4, 5), (3, 3), (-2, 2), (2, -2)):
                screen.blit(shadow, rect.move(*offset))
            screen.blit(rendered, rect)

        outlined_text(
            "NEW HIGH SCORE!",
            title_font,
            (550, 122),
            (249, 191, 198),
        )

        panel = pygame.transform.smoothscale(
            self.highscore_panel, (780, 561)
        )
        panel_rect = panel.get_rect(center=(550, 492))
        screen.blit(panel, panel_rect)

        outlined_text(
            "ENTER YOUR NAME",
            heading_font,
            (550, panel_rect.top + 72),
            (255, 224, 220),
        )

        instruction = body_font.render(
            "Letters, numbers, and spaces · 10 characters max",
            True,
            (231, 190, 193),
        )
        screen.blit(
            instruction,
            instruction.get_rect(center=(550, panel_rect.top + 143)),
        )

        input_rect = pygame.Rect(
            panel_rect.left + 160,
            panel_rect.top + 178,
            panel_rect.width - 320,
            86,
        )
        pygame.draw.rect(
            screen,
            (38, 19, 23),
            input_rect,
            border_radius=18,
        )
        pygame.draw.rect(
            screen,
            (245, 174, 181),
            input_rect,
            width=3,
            border_radius=18,
        )
        display_name = self.name_entry or "TYPE YOUR NAME"
        name_color = (
            self.MENU_TEXT if self.name_entry else (155, 111, 117)
        )
        name_font = pygame.font.SysFont("dejavusans", 31, bold=True)
        name_text = name_font.render(display_name, True, name_color)
        screen.blit(name_text, name_text.get_rect(center=input_rect.center))

        score = score_font.render(
            f"SCORE  {self.player.score:06d}",
            True,
            self.MENU_TEXT,
        )
        screen.blit(
            score,
            score.get_rect(center=(550, panel_rect.top + 337)),
        )

        hint = hint_font.render(
            "ENTER to save  ·  BACKSPACE to edit  ·  ESC to cancel",
            True,
            (231, 190, 193),
        )
        screen.blit(
            hint,
            hint.get_rect(center=(550, panel_rect.bottom - 43)),
        )
