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
    instruction_image: Any
    pause_menu: Any
    game_over_image: Any
    menu_image: Any
    game_over_reason: str | None
    _mazes: Any
    player: Any
    selected: int

    def _instructions(self, pygame: Any, screen: Any) -> None:
        screen.blit(self.background, (0, 0))
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
            panel = pygame.Surface((900, 260), pygame.SRCALPHA)
            panel.fill((57, 29, 29, 240))
            panel_rect = panel.get_rect(
                center=(self.WINDOW_SIZE[0] // 2, self.WINDOW_SIZE[1] // 2)
            )
            screen.blit(panel, panel_rect)
            title_font = pygame.font.Font(None, 72)
            body_font = pygame.font.Font(None, 34)
            title = title_font.render("TIME'S UP", True, self.MENU_SELECTED)
            body = body_font.render(
                "Press ENTER to return to the main menu",
                True,
                self.MENU_TEXT,
            )
            screen.blit(title, title.get_rect(center=(550, 410)))
            screen.blit(body, body.get_rect(center=(550, 500)))
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
        screen.blit(self.background, (0, 0))
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

    # def _draw_highscores(self, pygame: Any, screen: Any) -> None:
    #     screen.blit(self.background, (0, 0))
    #     panel = pygame.Surface((700, 500), pygame.SRCALPHA)
    #     panel.fill((8, 10, 24, 225))
    #     screen.blit(panel, panel.get_rect(center=(550, 450)))
    #     title_font = pygame.font.Font(None, 56)
    #     body_font = pygame.font.Font(None, 32)
    #     title = title_font.render("Highscores", True, self.MENU_SELECTED)
    #     screen.blit(title, title.get_rect(center=(550, 250)))
    #     score = body_font.render(
    #         f"Current score: {self.player.score}", True, self.MENU_TEXT
    #     )
    #     screen.blit(score, score.get_rect(center=(550, 370)))
    #     hint = body_font.render(
    #         "Press Enter or Esc to return", True, self.MUTED_TEXT
    #     )
    #     screen.blit(hint, hint.get_rect(center=(550, 520)))
