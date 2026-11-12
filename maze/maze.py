"""Create mazes from the levels returned by the configuration parser."""

from __future__ import annotations
from collections.abc import Mapping, Sequence
from pathlib import Path
import sys
from typing import Any


try:
    from mazegenerator import MazeGenerator
except ImportError as error:
    if error.name != "mazegenerator":
        raise
    generator_package = (
        Path(__file__).resolve().parent.parent
        / "mazegenerator-00001-py3-none-any"
    )
    sys.path.insert(0, str(generator_package))
    # An installed, older package can remain cached after the import above.
    # Remove it so the bundled package is actually loaded from the path added
    # above.
    sys.modules.pop("mazegenerator", None)
    from mazegenerator import MazeGenerator


Level = Mapping[str, Any]


class MazeGenerationError(RuntimeError):
    """Raised when the assigned maze generator cannot create a maze."""

def generate_maze(level: Level, seed: int = 0) -> MazeGenerator:
    """Generate one maze from a parsed level definition."""

    width = level.get("width")
    height = level.get("height")
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
