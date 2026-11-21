# Project timeline

The timeline below transcribes the task board. Weeks are relative project
weeks, not calendar dates.

## Overview

| Week | Focus | Estimated work | Board status |
|---:|---|---:|---|
| 0 | Foundation, investigation, interfaces, workspace | 12h | Done |
| 1 | Configuration, maze integration, initial game shell | 35h | Done |
| 2 | Core gameplay, AI, rendering, menus | 38h | Done |
| 3 | Progression, highscores, end states, cheat mode, integration | 33h | Done |
| 4 | Robustness, packaging, quality, documentation | 30h | Done |
| 5 | Buffer and polish | 12h | Done |
| **Total** |  | **160h** | **Done** |

## Week 0 — foundation

| Task | Owner | Estimate | Status |
|---|---|---:|---|
| Repository and Makefile (`install`, `run`, `debug`, `clean`, `lint`), flake8/mypy setup, and `.gitignore` | Both | 3h | Done |
| Read the assigned A-Maze-ing subject, test its output, and choose a graphics library | Both | 4h | Done |
| Define interfaces and write the decisions log | Both | 3h | Done |
| Create the Notion workspace and README skeleton | Both | 2h | Done |

**Outcome:** a shared technical baseline and a documented direction for the
implementation.

## Week 1 — configuration and game shell

| Task | Owner | Estimate | Status |
|---|---|---:|---|
| Configuration parser: comments, validation, clamping, defaults, and clear messages | mezahir | 8h | Done |
| A-Maze-ing adapter with `PERFECT=False`, internal maze model, and error handling | aymouate | 8h | Done |
| Place the player in the middle, four ghosts, four corner super-pac-gums, and pac-gums | mezahir | 5h | Done |
| Build the window and render loop; draw a stub maze, then the real maze | aymouate | 8h | Done |
| Add arrows/WASD input and the menu/playing/pause/over/victory state-machine skeleton | aymouate | 6h | Done |

**Outcome:** validated data can reach a visible game window and the generated
maze can be used by the game shell.

## Week 2 — gameplay slice

| Task | Owner | Estimate | Status |
|---|---|---:|---|
| Player movement, wall collision, eating, and scoring | mezahir | 8h | Done |
| Ghost AI: chase with BFS, flee, eaten state, and respawn timer | mezahir | 12h | Done |
| Draw Pac-Man, normal/edible ghosts, pellets, and HUD for score, lives, level, and time | mezahir | 10h | Done |
| Build the main menu and instructions screen | mezahir | 6h | Done |
| Build and integrate the pause menu | aymouate | 2h | Done |

**Outcome:** the principal play cycle exists: move, collect, avoid or eat
ghosts, score, and see the game state.

## Week 3 — progression and integration

| Task | Owner | Estimate | Status |
|---|---|---:|---|
| Lives, respawn, game over, and progression through 10+ levels | aymouate | 8h | Done |
| Top-10 highscore with names limited to 10 alphanumeric characters/spaces and robust bad-file handling | aymouate | 6h | Done |
| Game-over/victory screens, name-entry UI, and highscores in the menu | aymouate | 8h | Done |
| Cheat-mode logic, key bindings, and on-screen indicator | mezahir | 5h | Done |
| Integrate everything into one playable loop | Both | 6h | Done |

**Outcome:** the individual features are connected into a complete game flow,
including normal completion and failure paths.

## Week 4 — robustness and delivery

| Task | Owner | Estimate | Status |
|---|---|---:|---|
| Error-handling pass for broken configs, missing files, and generator failure | Both | 6h | Done |
| Package with PyInstaller or a similar tool, upload privately/unlisted to itch.io, and include in-package instructions | aymouate | 10h | Done |
| Make mypy/flake8 clean and complete docstrings and type hints | aymouate | 6h | Done |
| Complete the README required sections and project-management documentation | Both | 8h | Done |

**Outcome:** code quality, delivery packaging, and documentation are complete.

## Week 5 — buffer and polish

| Task | Owner | Estimate | Status |
|---|---|---:|---|
| Buffer for bugs, balance, and polish such as sounds and animations if time allows | aymouate | 12h | Done |

**Outcome:** reserve time absorbs late defects and supports final polish.

## Planned effort by person

| Person | Individual task hours | Share of shared tasks | Total |
|---|---:|---:|---:|
| `aymouate` | 74h | 16h | **90h** |
| `mezahir` | 54h | 16h | **70h** |
| **Project effort** | **128h** | **32h** | **160h** |



