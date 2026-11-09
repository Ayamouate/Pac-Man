*This project has been created as part of the 42 curriculum by `aymouate`,`mezahir`.*

## 1. Description:

`Pacman` is a recreation of the classic arcade game, developed in **Python 3.13** using **Pygame** for graphics, rendering, animations, and player interaction, following an object-oriented and modular software architecture.

The objective is to navigate through procedurally generated mazes, collect pac-gums and super-pac-gums, avoid or defeat four autonomous ghosts, and complete **10** levels while achieving the highest possible score.

Each level features a new maze, with increasing challenges. Collecting a super-pac-gum temporarily makes ghosts vulnerable, allowing the player to eat them and earn extra points.

The game includes a graphical interface with a main menu, instructions, pause menu, in-game HUD, game-over and victory screens, as well as a persistent top 10 highscore system. Additional features include JSON-based configuration and a cheat mode for testing and evaluation.

## 2. Instructions:
### Installation

Clone the repository:

```bash
git clone <repository-url>
cd Pac-Man
```

Install the required dependencies:

```bash
make install
```

### Execution

Run the game with a configuration file:

```bash
make run
```

Or launch it directly:

```bash
python3 pac-man.py config.json
```

## 3.How to Play :

### Objective

Navigate Pac-Man(Maomao) through the maze, collect all the Pacgums, and avoid being caught by the ghosts. Complete each level before the timer runs out and try to achieve the highest score!

### Controls

| Key | Action |
|---|---|
| Arrow Keys / WASD | Move Pac-Man |
| P | Pause / Resume |
| ESC / Q | Return to Main Menu / Exit Game |

### Cheat Mode

Press **C** to open the Cheat Mode menu and access the following features:

| Key | Action |
|---|---|
| F | Freeze / Unfreeze Ghosts |
| I | Toggle Infinite Lives |
| V | Toggle Invincibility |
| N | Skip to the Next Level |

### Gameplay

- **Collect Pacgums:** Earn points by collecting regular Pacgums throughout the maze.
- **Super Pacgums:** Activate frightened mode, allowing Pac-Man to eat ghosts for extra points.
- **Avoid Ghosts:** Normal ghost collisions cost Pac-Man a life.
- **Complete Levels:** Collect all Pacgums before the time limit expires to progress to the next level.
- **Earn High Scores:** Your score is recorded in the Highscore table, where you can compete for a place in the Top 10.

The game ends when all lives are lost or the player successfully completes the configured level progression.

## 4.Configuration :

The game uses a `config.json` file to customize its settings, including the number of lives, scoring system, Pacgums, level time limits, and maze generation parameters.


### Configuration Structure

The `config.json` file follows this structure:

```json
{
    "highscore_filename": "highscores.json",
    "lives": 3,
    "pacgum": 42,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "level_max_time": 90,
    "levels": [
        { "width": 15, "height": 15, "seed": 42 },
        { "width": 19, "height": 21, "seed": 101 }
    ]
}
```

### Configuration Parameters

| Parameter | Description | Default Value |
|---|---|---|
| `highscore_filename` | File used to store high scores. | `highscores.json` |
| `lives` | Initial number of player lives. | `3` |
| `pacgum` | Number of regular Pacgums. | `42` |
| `points_per_pacgum` | Points earned for collecting a regular Pacgum. | `10` |
| `points_per_super_pacgum` | Points earned for collecting a Super Pacgum. | `50` |
| `points_per_ghost` | Points earned for eating a frightened ghost. | `200` |
| `level_max_time` | Maximum time allowed per level, in seconds. | `90` |
| `levels` | List of maze configurations. | Defined in `config.json` |

### Configuration Validation

The configuration is validated when the game starts.

- Missing configuration values are replaced with their default values.
- Invalid values are rejected and replaced with safe defaults.
- Missing or malformed configuration files are handled without crashing the game.
- Unknown configuration keys are ignored.
- Full-line comments beginning with `#` are supported.

This validation ensures that the game can start safely even when the configuration file contains errors.

## 5. Highscore System :

The game includes a persistent Top 10 highscore system that stores players' names and scores in `highscores.json`.

After a game ends, players can enter their names to save their scores. The leaderboard ranks entries from highest to lowest and keeps only the ten best scores.

Player names are limited to 10 characters and accept only alphanumeric characters and spaces. Invalid or corrupted highscore data is handled safely.

## 6. Maze Generation :

The project uses the assigned **A-Maze-ing** package (`MazeGenerator`) to generate mazes dynamically. The game does not implement its own maze-generation algorithm; instead, it relies on the external package and integrates its output into the game.

The maze-generation process is:

1. `main()` reads the configuration file using `config_file()` and retrieves the configured levels and seed.
2. `generate_mazes()` iterates through the level definitions and generates one maze for each level.
3. `generate_maze()` validates the dimensions of each level, ensuring that the width and height are integers and that the maze is at least 3×3.
4. The external `MazeGenerator` is initialized with the level dimensions, the corresponding seed, and `perfect=False`.
5. Each level receives a reproducible seed calculated from the main seed and its level number.
6. The generated maze is returned and passed to `MazeViewer`, which handles its visualization and gameplay integration.

## 7. Implementation :

The main implementation is based on the following mechanisms:

1. **Game Initialization:** The application starts by loading and validating the JSON configuration file. It then generates the configured mazes and initializes the game with the selected settings, including player lives, scoring rules, and level information.

2. **Game Loop:** The main loop continuously processes keyboard events, updates game entities, checks interactions, renders the current game state, and refreshes the display. A controlled frame rate ensures consistent gameplay.

3. **Player Movement:** Pac-Man moves through the maze using keyboard controls. Movement is restricted by the maze structure to prevent the player from passing through walls.

4. **Collectibles and Scoring:** Regular Pacgums and Super Pacgums are placed throughout the maze. When Pac-Man reaches a collectible, the interaction system detects the collision, removes the collectible, and updates the player's score according to its type.

5. **Ghost Behavior:** Ghosts are implemented as independent entities with their own movement and behavior logic. Their interactions with Pac-Man are used to manage collisions, player lives.

6. **Level and Game State Management:** The game handles level progression, remaining lives, and time limits. It also manages the different screens and states, including the main menu, pause, game over, and victory.

7. **Score and High-Score Management:** The scoring system tracks points earned during gameplay, while the high-score system stores and displays the best results.

## 8. Software Architecture :

## 9. Project Management :

## 10. Resources :

* [Breadth-First Search (BFS) – GeeksforGeeks](https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/)
* [Pac-Man – Arcade Game](https://retro-arcade.fr/borne-darcade-pac-man/)
* [Pygame Documentation](https://www.pygame.org/docs/)
* [Python JSON Documentation](https://www.scrapingbee.com/blog/how-to-read-and-parse-json-data-with-python/?utm_source=google&utm_medium=cpc&utm_campaign=HD-ScrapingBee-PMax-Global-Prospecting&gad_source=1&gad_campaignid=23542351429&gbraid=0AAAAACSOZOOktddiFF4VwZKKD0A-0Har5&gclid=Cj0KCQiA-8XXBhDaARIsADnEOrD4BTRBCnlYOKVlU9-Bsd0dehYNlIAzGoYwrxvis53HiTk1FCBD_E4aAgLMEALw_wcB)
* [PyInstaller](https://www.pyinstaller.org/en/stable/usage.html?utm_source=chatgpt.com)

### AI Usage
AI was used to :

- Exploring ghost behaviors and different movement strategies.
- Generating visual assets and images used in the game.
- Exploring ideas and approaches for different game features.
- Supporting us in planning the project, organizing tasks, dividing responsibilities, and coordinating our work throughout development.
- Reviewing the README and improving technical documentation.