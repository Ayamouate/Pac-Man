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
    print(f"Loaded {len(mazes)} maze levels.")
    for level_number, level in enumerate(data["levels"], 1):
        print(f"Level {level_number}: {level['width']}x{level['height']}")
    MazeViewer(data["levels"], mazes).run()


if __name__ == "__main__":
    main()
