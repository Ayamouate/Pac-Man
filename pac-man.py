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
    for level_number, (level, maze) in enumerate(
        zip(data["levels"], mazes), 1
    ):
        path_length = (
            len(maze.shortest_path)
            if isinstance(maze.shortest_path, str)
            else 0
        )
        print(
            f"Level {level_number}: {level['width']}x{level['height']} "
            f"(shortest path: {path_length} steps)"
        )
    MazeViewer(data["levels"], mazes).run()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1)
