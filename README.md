*This project has been created as part of the 42 curriculum by `aymouate`, `mezahir`.*

## 1. Description:

`Pacman` is a recreation of the classic arcade game, developed in **Python 3.13** using **Pygame** for graphics, rendering, animations, and player interaction, following an object-oriented and modular software architecture.

The objective is to navigate through procedurally generated mazes, collect pac-gums and super-pac-gums, avoid or defeat four autonomous ghosts, and complete **10** levels while achieving the highest possible score.

Each level features a new maze, with increasing challenges. Collecting a super-pac-gum temporarily makes ghosts vulnerable, allowing the player to eat them and earn extra points.

The game includes a graphical interface with a main menu, instructions, pause menu, in-game HUD, game-over and victory screens, as well as a persistent top 10 highscore system. Additional features include JSON-based configuration and a cheat mode for testing and evaluation.

## 2. Instructions:
### Installation

Clone the repository:

```bash
git clone git@github.com:Ayamouate/Pac-Man.git
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

### Packaging

The Makefile also provides PyInstaller packaging commands:

```bash
make package  # creates dist/PacMan/
make zip      # creates PacMan-linux.zip
```

The package includes the game assets, audio, configuration package, and
configuration file required by the application.

## 3.How to Play :

### Objective

Navigate Pac-Man(Maomao) through the maze, collect all the Pacgums, and avoid being caught by the ghosts. Complete each level before the timer runs out and try to achieve the highest score!

### Controls

| Key | Action |
|---|---|
| Arrow Keys / WASD | Move Pac-Man |
| P / ESC | Open the pause menu |
| 1 (pause menu) | Resume the current game |
| 2 (pause menu) | Return to the main menu |
| M | Toggle music |
| Q | Return to the main menu / exit from the menu |

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
- **Super Pacgums:** Activate scared mode, allowing Pac-Man to eat ghosts for extra points.
- **Avoid Ghosts:** Normal ghost collisions cost Pac-Man a life.
- **Complete Levels:** Collect all Pacgums before the time limit expires to progress to the next level.
- **Earn High Scores:** Your score is recorded in the Highscore table, where you can compete for a place in the Top 10.

The game ends when all lives are lost, the level timer expires, or the player
successfully completes the configured level progression.

### Ghost Algorithm

The ghost system is implemented in `engine/ghost.py`. Each ghost uses AI logic
to move through the maze and interact with Pac-Man.

#### `Ghost Personalities`

Each ghost has a distinct personality and targeting strategy in **CHASE** mode:

| Color | Ghost | Target in CHASE mode |
|---|---|---|
| Red | Blinky | Pac-Man's current cell. Blinky is the direct chaser. |
| Pink | Pinky | Four cells ahead of Pac-Man's current direction. |
| Cyan | Inky | A target calculated using a pivot two cells ahead of Pac-Man and Blinky's current position. |
| Orange | Clyde | Pac-Man when far away; its starting corner when close. |

#### `Ghost Movement`

Ghosts use **Breadth-First Search (BFS)** to find paths through the maze. Their movement behavior depends on their current state and the game situation.

#### `Ghost States and Transitions`

The implementation uses `chase` and `scared` states, plus an `is_eaten` flag:

- **Chase:** Ghosts follow paths toward their individual targets.
- **Scared:** When Pac-Man collects a Super Pacgum, ghosts become vulnerable and try to escape.
- **Eaten (`is_eaten`):** When Pac-Man catches a scared ghost, the flag is set and the ghost is temporarily removed from play.
- **Return to play:** After the eaten delay, the ghost returns to its spawn position and its state is set back to `chase`.

### Game Coordination

`MazeViewer` coordinates ghost updates and manages their interactions with the
player through `InteractionManager`. It handles state transitions, collisions,
and the timing of ghost respawning.

## 4.Configuration :

The game uses a `config.json` file to customize its settings, including the number of lives, scoring system, Pacgums, level time limits, and maze generation parameters.


### Configuration Structure

The `config.json` file follows this structure:

```json
{
    "highscore_filename": "highscore.json",
    "lives": 3,
    "pacgum": 200,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 100,
    "levels": [
        { "width": 15, "height": 15 },
        { "width": 15, "height": 16 },
        { "width": 17, "height": 17 },
        { "width": 19, "height": 19 },
        { "width": 21, "height": 19 },
        { "width": 21, "height": 21 },
        { "width": 23, "height": 21 },
        { "width": 25, "height": 21 },
        { "width": 27, "height": 23 },
        { "width": 29, "height": 23 }
    ]
}
```

### Configuration Parameters

| Parameter | Description | Configured value (`config.json`) |
|---|---|---|
| `highscore_filename` | File used to store high scores. | `highscore.json` |
| `lives` | Initial number of player lives. | `3` |
| `pacgum` | Number of regular Pacgums. | `200` |
| `points_per_pacgum` | Points earned for collecting a regular Pacgum. | `10` |
| `points_per_super_pacgum` | Points earned for collecting a Super Pacgum. | `50` |
| `points_per_ghost` | Points earned for eating a frightened ghost. | `200` |
| `seed` | Main seed used to generate reproducible levels. | `42` |
| `level_max_time` | Maximum time allowed per level, in seconds. | `100` |
| `levels` | List of maze configurations. | 10 levels in `config.json` |

### Configuration Validation

The configuration is validated when the game starts.

- Missing configuration values are replaced with their default values.
- Invalid values are rejected and replaced with safe defaults.
- Missing or malformed configuration files are handled without crashing the game.
- Unknown configuration keys are ignored.
- Comments beginning with `#` or `//` are supported.
- Configuration keys are case-insensitive.

This validation ensures that the game can start safely even when the configuration file contains errors.

## 5. Highscore System :

The game includes a persistent Top 10 highscore system that stores players'
names and scores in `highscore.json` by default. A custom path can be supplied
through `highscore_filename` in the configuration.

After a game ends, players can enter their names to save their scores. The leaderboard ranks entries from highest to lowest and keeps only the ten best scores.

Player names are limited to 10 characters and accept only alphanumeric characters and spaces. Invalid or corrupted highscore data is handled safely.

## 6. Maze Generation :

The project uses the assigned **A-Maze-ing** package (`MazeGenerator`) to generate mazes dynamically. The game does not implement its own maze-generation algorithm; instead, it relies on the external package and integrates its output into the game.

The maze-generation process is:

1. `main()` reads the configuration file using `config_file()` and retrieves the configured levels and seed.
2. `generate_mazes()` iterates through the level definitions and generates one maze for each level.
3. The configuration parser validates each level dimension, requiring integer
   widths and heights between 10 and 30.
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

The project follows a modular, object-oriented architecture that separates the application's entry point, configuration handling, maze generation, gameplay logic, and visual presentation. Each module and class has a specific responsibility, making the code easier to maintain and extend.

### A. Application Entry Point

The `pac-man.py` file is the entry point of the application. It validates the command-line arguments and checks that the provided configuration file has a JSON extension.

It then uses `config_file()` from the configuration parsing module to read the game configuration. The parsed data is passed to `generate_mazes()` from the maze module, which generates the levels using the configured seed. Finally, `pac-man.py` creates a `MazeViewer` instance with data and generated mazes, then calls its `run()` method to launch the game.

### B. Main Game Controller

The `MazeViewer` class, located in `maze.visualizer`, acts as the central controller. It initializes the main game components, manages the game loop, processes events, updates gameplay, and coordinates rendering.

It uses multiple inheritance from two mixins:

- **GameMixin:** Handles keyboard input, game-state transitions, level management, timers, game resets, and cheat-mode controls.
- **ScreensMixin:** Handles the visual presentation of the main menu, instructions, pause menu, game-over screen, victory screen, highscores, and name-entry screen.

### C. Gameplay Components

The gameplay is organized into several classes:

- **Player:** Manages the player's position, movement, direction, lives, and score. It uses the `Loader` class to check whether a movement is possible according to the maze walls.
- **Ghost:** Represents the four ghosts and manages their movement and behavior. It uses Breadth-First Search (BFS) to find shortest paths and determine movement towards target positions. It also supports different targeting strategies and escape movement.
- **Loader:** Checks the maze structure and determines whether a wall allows movement in a given direction.
- **Pacgums:** Manages the collectible items in the maze.
- **InteractionManager:** Handles interactions between the player, ghosts, and collectibles. It checks pacgum collection, super_pacgum effects, ghost collisions, and related score and sound effects.
- **CheatMode:** Stores and manages the states of the available cheat modes, such as invincibility, freeze, and infinite lives.

### D. Supporting Components

Other classes provide additional game functionality:

- **HighscoreManager:** Loads, validates, sorts, and saves the top ten scores. It uses `HighscoreEntry` to represent individual player records and stores the data in JSON format.
- **HighscoreEntry:** Represents a single high-score entry containing a player's name and score.
- **SoundManager:** Manages the game's music and sound effects.

## 9. Project Structure

The repository is organized by responsibility: the root contains the entry
point and runtime data, `engine/` contains gameplay entities, and `maze/`
contains maze generation, the game controller, screens, and persistence.

```text
.
├── pac-man.py                         # Application entry point
├── config.json                        # Runtime configuration
├── highscore.json                     # Persistent high scores
├── Makefile                            # Install, run, package, lint, and clean commands
├── requirements.txt                    # Python dependencies
├── README.md                          # Project documentation
├── assets/                            # Images used by the Pygame interface
│   ├── Bg.jpeg
│   ├── player.png, red.png, pink.png, bleu.png, orange.png
│   ├── pacgum.png, super_pacgum.png, edible.png, life_icon.png
│   ├── wall_h.png, wall_v.png
│   └── menu and screen images
├── audio/
│   ├── sound_manager.py               # Music and sound-effect management
│   ├── music/music.wav                # Background music
│   └── sounds/                        # Gameplay and menu sound effects
├── config/
│   └── parsing.py                      # Configuration loading and validation
├── engine/
│   ├── player.py                       # Player movement, lives, and score
│   ├── ghost.py                        # Ghost AI and pathfinding
│   ├── pacgums.py                      # Collectible placement
│   ├── interactions.py                 # Collision and collection rules
│   └── cheat_mode.py                   # Testing and cheat switches
├── maze/
│   ├── maze.py                         # MazeGenerator integration
│   ├── maze_loader.py                  # Wall and movement validation
│   ├── visualizer.py                   # Main Pygame controller and game loop
│   ├── game_logic.py                   # Input, states, timer, and level changes
│   ├── screens.py                      # Menu and screen rendering
│   └── highscore.py                    # Validated top-10 score storage
├── mazegenerator-2.1.0-py3-none-any.whl # MazeGenerator dependency
└── project_management/                # Planning and delivery documents
```

## 10. File-by-File Explanation

### Root files

| File | Responsibility |
|---|---|
| `pac-man.py` | Validates the command-line argument, loads the configuration, generates all mazes, creates `MazeViewer`, and starts the application. |
| `config.json` | Defines the default run settings: lives, scoring, seed, time limit, high-score file, and level dimensions. |
| `highscore.json` | Stores the persistent high-score entries written by `HighscoreManager`. |
| `Makefile` | Provides `install`, `run`, `debug`, `package`, `zip`, `clean`, and `lint` commands. |
| `requirements.txt` | Lists Pygame, linting/type-checking tools, PyInstaller, and the local maze-generator wheel. |
| `PacMan.spec` | Describes the PyInstaller data files and executable settings. |
| `README.md` | Describes installation, gameplay, architecture, and project organization. |

### `config/`

| File | Responsibility |
|---|---|
| `config/__init__.py` | Marks `config` as a Python package. |
| `config/parsing.py` | Reads JSON configuration files, removes supported comment lines, applies defaults, validates types, and sanitizes level dimensions. |

### `engine/`

| File | Responsibility |
|---|---|
| `engine/__init__.py` | Marks `engine` as a Python package. |
| `engine/player.py` | Stores Pac-Man's position, direction, lives, score, movement rules, and temporary respawn protection. |
| `engine/ghost.py` | Implements ghost states, target selection, BFS shortest-path movement, and frightened escape movement. |
| `engine/pacgums.py` | Places regular Pacgums and four Super Pacgums on the current maze. |
| `engine/interactions.py` | Processes Pacgum collection, score updates, Super Pacgum scared mode, ghost eating, and player collisions. |
| `engine/cheat_mode.py` | Stores the enabled/disabled states for freeze, infinite lives, invincibility, and level skipping. |

### `maze/`

| File | Responsibility |
|---|---|
| `maze/__init__.py` | Exposes the maze-generation helpers as package functions. |
| `maze/maze.py` | Creates one reproducible maze per configured level using `MazeGenerator` and reports generation errors. |
| `maze/maze_loader.py` | Interprets the generator's wall bit flags and prevents movement through walls or outside the maze. |
| `maze/visualizer.py` | Defines `MazeViewer`, the central controller responsible for Pygame setup, the 60 FPS loop, entity updates, rendering, audio, and screen selection. |
| `maze/game_logic.py` | Defines `GameMixin`, which handles keyboard input, menu actions, pause/resume, timers, game resets, level changes, name entry, and cheat controls. |
| `maze/screens.py` | Defines `ScreensMixin`, which draws the menu, instructions, pause, gameplay HUD, highscores, name-entry, game-over, and victory screens. |
| `maze/highscore.py` | Validates player names and scores, keeps the highest ten entries, and saves them safely as JSON. |

### `audio/`, assets, and bundled dependencies

| Path | Responsibility |
|---|---|
| `audio/__init__.py` | Marks `audio` as a Python package. |
| `audio/sound_manager.py` | Loads music and sound effects, handles playback, pause/resume, muting, and missing-audio fallbacks. |
| `audio/music/` and `audio/sounds/` | Contain the bundled WAV files used by menus and gameplay events. |
| `assets/` | Contains the background, maze walls, player, ghosts, collectibles, HUD, and screen artwork loaded by `MazeViewer`. |
| `mazegenerator-2.0.2-py3-none-any.whl` | Local wheel installed by `make install`; it provides the assigned `MazeGenerator` implementation. |
| `project_management/` | Contains team organization, timeline, progress, risk analysis, and acceptance-test documents. |

## 11. Main Game State Flow

The game uses two related state values:

- `state` selects the active screen: `menu`, `playing`, `instructions`,
  `highscores`, `over`, `victory`, or `name_entry`.
- `game_state` controls gameplay while `state == "playing"`: it is either
  `playing` or `pause`.

### Application and screen flow

```text
Start
  │
  ├─ Read and validate config.json
  ├─ Generate one maze for each configured level
  └─ Create MazeViewer ──> state = menu
                              │
          ┌───────────────────┼────────────────────┐
          │                   │                    │
     Start Game         View Highscores        Instructions
          │                   │                    │
          v                   v                    v
   state = playing       state = highscores    state = instructions
   game_state = playing        │                    │
          │                    └──── Return ───────┘
          │                              │
          └────────────── Return to menu ┘

   Exit / Q / window close ──> application stops
```

### Gameplay loop and transitions

```text
state = playing, game_state = playing
  │
  ├─ Read keyboard and window events
  ├─ Check the level timer
  ├─ Move ghosts and calculate their targets
  ├─ Move Pac-Man when the movement interval elapses
  ├─ Collect Pacgums / Super Pacgums and update the score
  ├─ Check ghost collisions and lives
  ├─ Render the maze, entities, HUD, and effects
  └─ Repeat at up to 60 frames per second
```

## 12. Project Management :

Project planning and delivery documentation is available in the
[`project_management`](project_management/) folder:

- [Team organisation](project_management/team_organisation.md)
- [Timeline](project_management/timeline.md)
- [Project progress](project_management/project_progress.md)
- [Risk analysis](project_management/risk_analysis.md)
- [Acceptance tests](project_management/acceptance_tests.md)

## 13. Resources :

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
