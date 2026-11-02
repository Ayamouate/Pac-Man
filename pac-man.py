import sys
from config.parsing import config_file
from maze.maze import generate_mazes
from maze.visualizer import MazeViewer


def main() -> None:

    if len(sys.argv) != 2:
        raise ValueError("Expected exactly one configuration file.")
    if not sys.argv[1].endswith(".json"):
        raise ValueError("configuration file must be in json format")
    data = config_file(sys.argv[1]).read_file()
    mazes = generate_mazes(data["levels"], seed=data["seed"])
    print(f"\033[1;38;5;218m{len(mazes)} LEVELS LOADED. GET READY TO PLAY!\033[0m")
    MazeViewer(data, mazes).run()


if __name__ == "__main__":
    # try:
    main()
    # except Exception as error:
    #     print(f"Error: {error}", file=sys.stderr)
    #     raise SystemExit(1)
