"""Small, dependency-free wind animation for the Sakura background."""

from __future__ import annotations

import math
import random
from typing import Any


class AnimatedBackground:
    """Blow petals off the cherry-blossom canopies of a still background.

    The image is never distorted. At start-up the pink blossom pixels in the
    tree area are located, and petals are spawned only from those points.
    Each petal is pushed by a shared, gusting wind, flutters while it falls,
    then fades out and respawns on another blossom.
    """

    # Blossom detection
    SCAN_STEP = 4
    CANOPY_MAX_Y = 0.54
    PETAL_COUNT = 70

    def __init__(
        self, pygame: Any, image: Any, particle_image: Any | None = None
    ) -> None:
        self.pygame = pygame
        self.image = image
        self.particle_image = particle_image
        self.width, self.height = image.get_size()
        self.overlay = pygame.Surface(image.get_size(), pygame.SRCALPHA)

        self.elapsed = 0.0
        self.last_tick = pygame.time.get_ticks()
        self.random = random.Random(42)

        self.sources = self._find_blossoms()
        self.petals: list[dict[str, Any]] = []
        if self.sources:
            for _ in range(self.PETAL_COUNT):
                petal = self._new_petal()
                # Start at a random point so the petals do not appear together.
                petal["age"] = self.random.uniform(0, petal["life"])
                self.petals.append(petal)

    # setup
    def _find_blossoms(self) -> list[tuple[int, int, tuple[int, int, int]]]:
        """Return (x, y, color) for pink pixels inside the tree canopies."""

        points = []
        step = self.SCAN_STEP
        max_y = int(self.height * self.CANOPY_MAX_Y)
        for y in range(0, max_y, step):
            for x in range(0, self.width, step):
                r, g, b = self.image.get_at((x, y))[:3]
                is_pink = (
                    r > 190
                    and r - g > 60
                    and b - g > 20
                    and g < 200
                    and r - b < 90
                )
                if is_pink:
                    points.append((x, y, (r, g, b)))
        return points

    def _new_petal(self) -> dict[str, Any]:
        x, y, color = self.random.choice(self.sources)
        rnd = self.random
        step = self.SCAN_STEP
        return {
            "x": x + rnd.uniform(-step, step),
            "y": y + rnd.uniform(-step, step),
            "color": (
                min(255, color[0] + 15),
                min(255, color[1] + 25),
                min(255, color[2] + 15),
            ),
            "age": 0.0,
            "life": rnd.uniform(5.0, 10.0),
            "fall": rnd.uniform(10, 28),
            "wind": rnd.uniform(35, 80),
            "size": rnd.uniform(2.5, 5.5),
            "phase": rnd.uniform(0, math.tau),
            "flutter": rnd.uniform(14, 34),
            "spin": rnd.uniform(1.5, 3.5),
        }

    # draw
    def draw(self, screen: Any) -> bool:
        """Draw the current frame and return whether it was available."""

        now = self.pygame.time.get_ticks()
        delta = min(max((now - self.last_tick) / 1000.0, 0.0), 0.1)
        self.last_tick = now
        self.elapsed += delta

        self._update_petals(delta)
        screen.blit(self.image, (0, 0))
        screen.blit(self.overlay, (0, 0))
        return True

    def _gust(self) -> float:
        """Return a slow breeze with occasional stronger gusts."""

        t = self.elapsed
        return 1.0 + 0.45 * math.sin(t * 0.5) + 0.25 * math.sin(t * 1.3 + 1.0)

    def _update_petals(self, delta: float) -> None:
        self.overlay.fill((0, 0, 0, 0))
        if not self.petals:
            return

        gust = max(self._gust(), 0.2)
        for index, petal in enumerate(self.petals):
            petal["age"] += delta
            age = petal["age"]
            if (
                age >= petal["life"]
                or petal["x"] > self.width + 30
                or petal["y"] > self.height + 30
            ):
                petal = self.petals[index] = self._new_petal()
                age = 0.0

            phase = petal["phase"]
            petal["x"] += petal["wind"] * gust * delta
            petal["y"] += (
                petal["fall"]
                + math.sin(age * 2.4 + phase) * petal["flutter"] * 0.5
            ) * delta

            x = petal["x"]
            y = petal["y"] + math.sin(age * 3.1 + phase) * 4

            # Quick fade-in, slow fade-out.
            life = petal["life"]
            fade = min(age / 0.4, 1.0, (life - age) / 1.5)
            alpha = round(235 * max(fade, 0.0))
            if alpha <= 0:
                continue

            angle = age * petal["spin"] + phase
            if self.particle_image is not None:
                size = petal["size"]
                source_size = max(self.particle_image.get_size())
                scale = size * 2.4 / source_size
                sprite = self.pygame.transform.rotozoom(
                    self.particle_image,
                    -math.degrees(angle),
                    scale,
                )
                sprite.set_alpha(alpha)
                self.overlay.blit(
                    sprite,
                    sprite.get_rect(center=(round(x), round(y))),
                )
            else:
                size = petal["size"]
                squash = 0.35 + 0.65 * abs(math.cos(angle * 0.7))
                dx, dy = math.cos(angle) * size, math.sin(angle) * size
                nx, ny = -dy * 0.55 * squash, dx * 0.55 * squash
                points = [
                    (round(x - dx - nx), round(y - dy - ny)),
                    (round(x + nx), round(y + ny)),
                    (round(x + dx - nx), round(y + dy - ny)),
                    (round(x - nx), round(y - ny)),
                ]
                self.pygame.draw.polygon(
                    self.overlay, (*petal["color"], alpha), points
                )

    def stop(self) -> None:
        """Match the interface of a video background; there is no resource."""
