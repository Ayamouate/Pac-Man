"""Create mazes from the levels returned by the configuration parser."""

from __future__ import annotations
from collections.abc import Mapping, Sequence
from pathlib import Path
import sys
from typing import Any


try:
    from mazegenerator import MazeGenerator
except ModuleNotFoundError as error:
    if error.name != "mazegenerator":
        raise
    generator_package = (
        Path(__file__).resolve().parent.parent
        / "mazegenerator-00001-py3-none-any"
    )
    sys.path.insert(0, str(generator_package))
    from mazegenerator import MazeGenerator


Level = Mapping[str, Any]


class MazeGenerationError(RuntimeError):
    """Raised when the assigned maze generator cannot create a maze."""


def _level_size(level: Level) -> tuple[int, int]:
    """Return a safe generator size for one parsed level."""

    width = level.get("width")
    height = level.get("height")
    if type(width) is not int or type(height) is not int:
        raise ValueError("A maze level must contain integer width and height")
    if width < 3 or height < 3:
        raise ValueError("A maze level must be at least 3x3")
    return width, height


def generate_maze(level: Level, seed: int = 0) -> MazeGenerator:
    """Generate one maze from a parsed level definition."""

    width, height = _level_size(level)
    try:
        return MazeGenerator(
            size=(width, height),
            perfect=False,
            seed=seed,
        )
    except Exception as error:
        raise MazeGenerationError(
            f"Could not generate maze {width}x{height}: {error}"
        ) from error


def generate_mazes(
    levels: Sequence[Level], seed: int = 0
) -> list[MazeGenerator]:
    """Generate all configured levels using reproducible per-level seeds."""

    return [
        generate_maze(level, seed=seed + level_number)
        for level_number, level in enumerate(levels)
    ]
