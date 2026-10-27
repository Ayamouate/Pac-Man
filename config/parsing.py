from config.class_error import Game_error
import json
from json import JSONDecodeError


DEFAULTS = {

    "highscore_filename": "highscores.json",
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

    default_level = {"width": 15, "height": 15}
    valide_levels = []
    for level in levels:
        if type(level) is not dict:
            valide_levels.append(default_level.copy())
            continue
        width = level.get("width", 15)
        height = level.get("height", 15)

        if type(width) is not int:
            width = 15
        if type(height) is not int:
            height = 15
        valide_levels.append({"width": width, "height": height})
    while len(valide_levels) < 10:
        valide_levels.append(default_level.copy())
    return valide_levels


class config_file:

    def __init__(self, file_name: str) -> None:
        self.file = file_name

    def read_file(self) -> dict:
        try:
            with open(self.file) as f:
                valid_content = []
                lines = []
                for i in f:
                    lines.append(i.strip())
                if not lines:
                    raise Game_error("empty config file")
                for line in lines:
                    if (
                        line.startswith("#")
                        or line.startswith("//")
                        or not line
                    ):
                        continue
                    valid_content.append(line)
                data = json.loads("\n".join(valid_content))
                if type(data) is not dict:
                    raise Game_error("Config must contain a JSON object")
                data = {i.lower(): j for i, j in data.items()}
                for key, default in DEFAULTS.items():
                    if key not in data:
                        print(f"Warning: missing {key}, using default.")
                        data[key] = default
                    elif type(data[key]) is not TYPES[key]:
                        print(f"Warning: invalid {key}, using default.")
                        data[key] = default
                    elif key == "levels":
                        data[key] = validate_levels(data[key])
                valide_data = {}
                for key in data:
                    if key not in TYPES:
                        continue
                    valide_data[key] = data[key]
        except FileNotFoundError:
            raise Game_error("config file missing")
        except PermissionError:
            raise Exception("You don't have permission to access the file")
        except JSONDecodeError:
            raise ValueError("Invalid JSON configuration")
        return valide_data
