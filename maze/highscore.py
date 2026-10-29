"""Persistent, validated high-score storage."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import tempfile
from typing import Any


MAX_HIGHSCORES = 10
MAX_PLAYER_NAME_LENGTH = 10
_PLAYER_NAME_PATTERN = re.compile(r"^[A-Za-z0-9 ]+$")


class HighscoreEntry:
    """Store one player's validated high-score entry."""

    def __init__(self, name: str, score: int) -> None:
        self.name = name
        self.score = score

    def to_dict(self) -> dict[str, Any]:
        """Return the entry in the format used by the JSON file."""

        return {"name": self.name, "score": self.score}


def validate_player_name(name: Any) -> str:
    """Validate and normalize a player name."""

    if not isinstance(name, str):
        raise ValueError("Player name must be text")
    normalized = name.strip()
    if not normalized:
        raise ValueError("Player name cannot be empty")
    if len(normalized) > MAX_PLAYER_NAME_LENGTH:
        raise ValueError(
            f"Player name must be at most {MAX_PLAYER_NAME_LENGTH} characters"
        )
    if _PLAYER_NAME_PATTERN.fullmatch(normalized) is None:
        raise ValueError(
            "Player name may contain only letters, numbers, and spaces"
        )
    return normalized


def validate_score(score: Any) -> int:
    """Validate a non-negative integer score."""

    if type(score) is not int or score < 0:
        raise ValueError("Score must be a non-negative integer")
    return score


def sort_entries(
    entries: list[HighscoreEntry],
) -> list[HighscoreEntry]:
    """Sort scores from highest to lowest and keep the top ten."""

    return sorted(
        entries,
        key=lambda entry: entry.score,
        reverse=True,
    )[:MAX_HIGHSCORES]


class HighscoreManager:
    """Load, update, and safely persist the top ten high scores."""

    def __init__(self, filename: str) -> None:
        self.path = Path(filename)
        self._entries: list[HighscoreEntry] = []
        self.load()

    def get_entries(self) -> list[HighscoreEntry]:
        """Return a copy of the current sorted leaderboard."""

        return list(self._entries)

    def load(self) -> list[HighscoreEntry]:
        """Load valid entries; missing or malformed files become empty."""

        try:
            with self.path.open("r", encoding="utf-8") as highscore_file:
                content = json.load(highscore_file)
        except (OSError, UnicodeError, json.JSONDecodeError, TypeError):
            self._entries = []
            return self.get_entries()

        if isinstance(content, dict):
            content = content.get("highscores", [])
        if not isinstance(content, list):
            self._entries = []
            return self.get_entries()

        valid_entries: list[HighscoreEntry] = []
        for item in content:
            if not isinstance(item, dict):
                continue
            try:
                name = validate_player_name(item.get("name"))
                score = validate_score(item.get("score"))
            except ValueError:
                continue
            valid_entries.append(HighscoreEntry(name, score))

        self._entries = sort_entries(valid_entries)
        return self.get_entries()

    def qualifies(self, score: Any) -> bool:
        """Return whether a valid score belongs in the top ten."""

        try:
            score = validate_score(score)
        except ValueError:
            return False
        return (
            len(self._entries) < MAX_HIGHSCORES
            or score >= self._entries[-1].score
        )

    def record(self, name: Any, score: Any) -> bool:
        """Add a score and save it, returning whether saving succeeded."""

        entry = HighscoreEntry(
            validate_player_name(name), validate_score(score)
        )
        previous_entries = self._entries
        self._entries = sort_entries([*self._entries, entry])
        if self.save():
            return True
        self._entries = previous_entries
        return False

    def save(self) -> bool:
        """Atomically save the leaderboard without crashing on file errors."""

        temporary_path: Path | None = None
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.path.parent,
                prefix=f".{self.path.name}.",
                suffix=".tmp",
                delete=False,
            ) as temporary_file:
                temporary_path = Path(temporary_file.name)
                json.dump(
                    [entry.to_dict() for entry in self._entries],
                    temporary_file,
                    indent=2,
                )
                temporary_file.write("\n")
            os.replace(temporary_path, self.path)
            return True
        except (OSError, TypeError, ValueError):
            if temporary_path is not None:
                try:
                    temporary_path.unlink(missing_ok=True)
                except OSError:
                    pass
            return False
