# Project timeline

The timeline below transcribes the task board. Weeks are relative project
weeks, not calendar dates.

## Overview

| Week | Focus |
|---:|---|
| 0 | Foundation, investigation, interfaces, workspace |
| 1 | Configuration, maze integration, initial game shell |
| 2 | Core gameplay, AI, rendering, menus |
| 3 | Progression, highscores, end states, cheat mode, integration |
| 4 | Robustness, packaging, quality, documentation |
| 5 | Buffer and polish |

## Week 0 — foundation

| Task | Owner |
|---|---|
| Repository and Makefile (`install`, `run`, `debug`, `clean`, `lint`), flake8/mypy setup, and `.gitignore` | Both |
| Read the assigned A-Maze-ing subject, test its output, and choose a graphics library | Both |
| Define interfaces and write the decisions log | Both |
| Create the Notion workspace and README skeleton | Both |

**Outcome:** a shared technical baseline and a documented direction for the
implementation.

## Week 1 — configuration and game shell

| Task | Owner |
|---|---|
| Configuration parser: comments, validation, clamping, defaults, and clear messages | mezahir |
| A-Maze-ing adapter with `PERFECT=False`, internal maze model, and error handling | aymouate |
| Place the player in the middle, four ghosts, four corner super-pac-gums, and pac-gums | mezahir |
| Build the window and render loop; draw a stub maze, then the real maze | aymouate |

**Outcome:** validated data can reach a visible game window and the generated
maze can be used by the game shell.

## Week 2 — gameplay slice

| Task | Owner |
|---|---|
| Add arrows/WASD input and the menu/playing state-machine skeleton | aymouate |
| Player movement, wall collision, eating, and scoring | mezahir |
| Ghost AI: chase with BFS, flee, eaten state, and respawn timer | mezahir |
| Draw Pac-Man, normal/edible ghosts, pellets, and HUD for score, lives, level, and time | mezahir |
| Build the main menu and instructions screen | mezahir |
| Build and integrate the pause menu | mezahir |

**Outcome:** the principal play cycle exists: move, collect, avoid or eat
ghosts, score, and see the game state.

## Week 3 — progression and integration

| Task | Owner |
|---|---|
| Lives, respawn, game over, and progression through 10+ levels | aymouate |
| Top-10 highscore with names limited to 10 alphanumeric characters/spaces and robust bad-file handling | aymouate |
| Game-over/victory screens, name-entry UI, and highscores in the menu | aymouate |
| Cheat-mode logic, key bindings, and on-screen indicator | mezahir |
| Integrate everything into one playable loop | Both |

**Outcome:** the individual features are connected into a complete game flow,
including normal completion and failure paths.

## Week 4 — robustness and delivery

| Task | Owner |
|---|---|
| Error-handling pass for broken configs, missing files, and generator failure | Both |
| Package with PyInstaller or a similar tool, upload privately/unlisted to itch.io, and include in-package instructions | Both |
| Make mypy/flake8 clean and complete docstrings and type hints | aymouate |
| Complete the README required sections and project-management documentation | Both |

**Outcome:** code quality, delivery packaging, and documentation are complete.

## Week 5 — buffer and polish

| Task | Owner |
|---|---|
| Buffer for bugs, balance, and polish such as sounds and animations if time allows | aymouate |

**Outcome:** reserve time absorbs late defects and supports final polish.
