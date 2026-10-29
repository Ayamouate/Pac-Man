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
    game_over_reason: str | None
    _mazes: Any
    player: Any
    selected: int

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

        size = 700
        image = pygame.transform.scale(
            self.instruction_image, (size, size)
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
        surface.fill((0, 0, 0, 175))
        screen.blit(surface, (0, 0))

        panel = pygame.Surface((900, 330), pygame.SRCALPHA)
        panel.fill((25, 55, 48, 245))
        panel_rect = panel.get_rect(
            center=(self.WINDOW_SIZE[0] // 2, self.WINDOW_SIZE[1] // 2)
        )
        screen.blit(panel, panel_rect)

        title_font = pygame.font.Font(None, 82)
        body_font = pygame.font.Font(None, 36)
        title = title_font.render("VICTORY!", True, self.MENU_SELECTED)
        score = body_font.render(
            f"All {len(self._mazes)} levels cleared  -  Score: "
            f"{self.player.score}",
            True,
            self.MENU_TEXT,
        )
        hint = body_font.render(
            "Press ENTER to play again or ESC for the menu",
            True,
            self.MUTED_TEXT,
        )
        center_x = self.WINDOW_SIZE[0] // 2
        screen.blit(title, title.get_rect(center=(center_x, 365)))
        screen.blit(score, score.get_rect(center=(center_x, 455)))
        screen.blit(hint, hint.get_rect(center=(center_x, 525)))

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
        credit_font = pygame.font.SysFont("dejavusans", 20)
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
        
        screen.blit(self.background, (0, 0))
        panel = pygame.Surface((700, 500), pygame.SRCALPHA)
        panel.fill((8, 10, 24, 225))
        screen.blit(panel, panel.get_rect(center=(550, 450)))
        title_font = pygame.font.Font(None, 56)
        body_font = pygame.font.Font(None, 32)
        title = title_font.render("Highscores", True, self.MENU_SELECTED)
        screen.blit(title, title.get_rect(center=(550, 250)))
        score = body_font.render(
            f"Current score: {self.player.score}", True, self.MENU_TEXT
        )
        screen.blit(score, score.get_rect(center=(550, 370)))
        hint = body_font.render(
            "Press Enter or Esc to return", True, self.MUTED_TEXT
        )
        screen.blit(hint, hint.get_rect(center=(550, 520)))
