import json
from json import JSONDecodeError
from typing import Any
import sys
from pathlib import Path

DEFAULTS = {

    "highscore_filename": "highscore.json",
    "lives": 3,
    "pacgum": 42,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90,
    "levels": [
        {"width": 15, "height": 15}
        for _ in range(10)]
}

TYPES = {

    "highscore_filename": str,
    "lives": int,
    "pacgum": int,
    "points_per_pacgum": int,
    "points_per_super_pacgum": int,
    "points_per_ghost": int,
    "seed": int,
    "level_max_time": int,
    "levels": list
}


def validate_levels(levels: list) -> list:
    """Validate level dimensions and fill missing levels with defaults."""

    default_level = {"width": 15, "height": 15}
    valide_levels = []
    for level in levels:
        if type(level) is not dict:
            valide_levels.append(default_level.copy())
            continue
        width = level.get("width", 15)
        height = level.get("height", 15)

        if type(width) is not int or width < 10 or width > 30:
            print("Warning: Invalid maze width. Using default width (15).")
            width = 15
        if type(height) is not int or height < 10 or height > 30:
            print("Warning: Invalid maze height . Using default width (15).")
            height = 15
        valide_levels.append({"width": width, "height": height})
        if len(valide_levels) == 10:
            return valide_levels
    while len(valide_levels) < 10:
        valide_levels.append(default_level.copy())
    return valide_levels


def keep_first_key(data: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in data:
        if key not in result:
            result[key] = value
    return result


class config_file:
    """Read and validate the game's configuration file."""
    def __init__(self, file_name: str) -> None:
        requested_path = Path(file_name)
        if requested_path.is_file():
            self.file = requested_path
        elif getattr(sys, "frozen", False):
            self.file = Path(sys._MEIPASS) / requested_path.name
        else:
            self.file = requested_path

    def read_file(self) -> dict:
        """Read the JSON file and return validated configuration settings."""
        try:
            with open(self.file) as f:
                valid_content = []
                lines = []
                for i in f:
                    lines.append(i.strip())
                if not lines:
                    print("empty config file")
                    print("Using default configuration.")
                    return DEFAULTS
                for line in lines:
                    line = line.split("#")[0]
                    line = line.split("//")[0].strip()
                    if not line:
                        continue
                    valid_content.append(line)
                data = json.loads(
                    "\n".join(valid_content),
                    object_pairs_hook=keep_first_key,
                )
                if type(data) is not dict:
                    print("Config must contain a JSON object")
                    print("Using default configuration.")
                    return DEFAULTS
                data = {i.lower(): j for i, j in data.items()}
                for key, default in DEFAULTS.items():
                    if key not in data:
                        print(f"Warning: missing {key}, using default.")
                        data[key] = default
                    elif type(data[key]) is not TYPES[key]:
                        print(f"Warning: invalid {key}, using default.")
                        data[key] = default
                    if key == "levels":
                        data[key] = validate_levels(data[key])

                if data["lives"] < 1 or data["lives"] > 3:
                    print("Invalid lives, using default.")
                    data["lives"] = DEFAULTS["lives"]
                if data["pacgum"] < 1:
                    print("Invalid pacgum, using default.")
                    data["pacgum"] = DEFAULTS["pacgum"]

                if data["points_per_pacgum"] < 0:
                    print("Invalid points_per_pacgum, using default.")
                    data["points_per_pacgum"] = DEFAULTS["points_per_pacgum"]

                if data["points_per_super_pacgum"] < 0:
                    print("Invalid points_per_super_pacgum, using default.")
                    data["points_per_super_pacgum"] = DEFAULTS[
                        "points_per_super_pacgum"
                    ]

                if data["points_per_ghost"] < 0:
                    print("Invalid points_per_ghost, using default.")
                    data["points_per_ghost"] = DEFAULTS["points_per_ghost"]

                if data["seed"] <= 0:
                    print("Invalid seed, using default.")
                    data["seed"] = DEFAULTS["seed"]

                if data["level_max_time"] <= 0:
                    print("Invalid level_max_time, using default.")
                    data["level_max_time"] = DEFAULTS["level_max_time"]

                valide_data = {}
                for key in data:
                    if key not in TYPES:
                        continue
                    valide_data[key] = data[key]
        except FileNotFoundError:
            print("config file missing.")
            print("Using default configuration.")
            return DEFAULTS
        except JSONDecodeError:
            print("Invalid json format")
            print("Using default configuration.")
            return DEFAULTS
        except OSError as error:
            print(f"Could not read config file : {error}")
            print("Using default configuration.")
            return DEFAULTS
        return valide_data
