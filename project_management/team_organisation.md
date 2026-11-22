# Team organisation

## Team

The project is developed by `aymouate` and `mezahir`. Ownership is assigned
at task level so that each feature has a responsible person while shared
decisions remain visible to both teammates.

| Member | Main responsibilities from the task board |
|---|---|
| `aymouate` | A-Maze-ing adapter and internal maze integration; window and render loop; lives, respawn, game-over, and level progression; highscores; end screens and name entry; mypy/flake8, docstrings, and type hints |
| `mezahir` | Configuration parser; player, ghosts, pac-gums, and scoring; ghost AI; gameplay rendering and HUD; menus and instructions; cheat mode |
| `Both` | Repository/tooling setup; A-Maze-ing investigation and graphics-library choice; interfaces and decisions; project workspace and README; integration; error-handling pass; final project-management documentation |

## Responsibility matrix

| Area | Primary owner | Shared responsibility |
|---|---|---|
| Repository, Makefile, linting, and type-checking | aymouate | Agree on commands and keep the main branch runnable |
| Configuration and defaults | mezahir | Validate behavior against the game entry point |
| Maze generation and adapter | aymouate | Confirm the adapter contract with gameplay code |
| Player, collectibles, and scoring | Both | Confirm collision and scoring behavior in the playable loop |
| Ghost AI | mezahir | Validate pathfinding and state transitions during integration |
| Rendering, menus, and state transitions | Both | Keep visual states and gameplay states consistent |
| Highscores and name validation | aymouate | Test persistence with malformed files |
| Cheat mode | mezahir | Verify that it remains useful for testing without breaking normal play |
| Packaging and upload | Both | Both perform a clean-install or regenerated-package check |
| Documentation and reproducibility | Both | Each teammate must be able to explain and reproduce the project |

## Collaboration rules

### Ownership and hand-off

- The task owner implements the feature, keeps its interfaces documented, and
  demonstrates the behavior during integration.
- A `Both` task requires agreement on the interface or acceptance condition
  before it is considered complete.
- Shared code is integrated into the same playable loop regularly so that
  incompatible assumptions are found before the final week.
- A task should not be marked done merely because its code exists; its
  acceptance behavior and failure cases must also be checked.

### Interface-first development

The initial shared work defined the project interfaces and recorded design
decisions before feature implementation. Important boundaries are:

- `pac-man.py` loads configuration, generates mazes, and starts `MazeViewer`.
- `config.parsing` returns validated values and safe defaults.
- `maze.maze` adapts the assigned `MazeGenerator` package and reports
  generation failures through `MazeGenerationError`.
- `MazeViewer` coordinates the loop, state transitions, rendering, and game
  components.
- `Player`, `Ghost`, `Pacgums`, and `InteractionManager` own gameplay rules.
- `HighscoreManager` owns validated, persistent top-10 scores.

This separation lets either of us work on a subsystem without moving all
game logic into the render loop.

