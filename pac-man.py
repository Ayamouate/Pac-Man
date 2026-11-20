import sys
from pathlib import Path


def main() -> None:

    if len(sys.argv) != 2:
        raise ValueError(
            "Usage: python3 pac-man.py <configuration.json> "
            "(exactly one file is required)."
        )
    if not sys.argv[1].endswith(".json"):
        raise ValueError("configuration file must be in json format")
    from config.parsing import config_file
    from maze.maze import generate_mazes
    from maze.visualizer import MazeViewer

    config_path = Path(sys.argv[1]).resolve()
    data = config_file(str(config_path)).read_file()
    mazes = generate_mazes(data["levels"], seed=data["seed"])
    print(
        f"\033[1;38;5;218m{len(mazes)} LEVELS LOADED. "
        "GET READY TO PLAY!\033[0m"
    )
    MazeViewer(data, mazes, config_filename=config_path).run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting Pac-Man.")
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
