import sys
from config.parsing import config_file
from maze.maze import generate_mazes
from maze.visualizer import MazeViewer
from pathlib import Path
import os

if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)
else:
    os.chdir(Path(__file__).resolve().parent)

def main() -> None:

    if len(sys.argv) != 2:
        raise ValueError("Expected exactly one configuration file.")
    if not sys.argv[1].endswith(".json"):
        raise ValueError("configuration file must be in json format")
    config_path = Path(sys.argv[1])

    if not config_path.exists() and getattr(sys, "frozen", False):
        config_path = Path(sys._MEIPASS) / sys.argv[1]

    data = config_file(str(config_path)).read_file()
    # data = config_file(sys.argv[1]).read_file()
    mazes = generate_mazes(data["levels"], seed=data["seed"])
    print(
        f"\033[1;38;5;218m{len(mazes)} LEVELS LOADED. "
        "GET READY TO PLAY!\033[0m"
    )
    MazeViewer(data, mazes).run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting Pac-Man.")
