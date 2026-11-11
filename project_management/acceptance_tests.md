# Acceptance tests

This document defines the checks for the Pac-Man release. It is a test plan,
not a claim that every check has already been executed. Record the date,
environment, result, and evidence when running a check.

## Release definition of done

The project is ready for delivery when:

- the documented install and run commands work from a clean location;
- configuration errors fall back safely and produce understandable messages;
- all configured mazes generate and render;
- the player can complete the normal gameplay loop;
- ghost states, collisions, lives, respawn, timers, and progression behave as
  specified;
- menus, pause, game-over, victory, name entry, and highscores are usable;
- cheat mode works for testing and displays its state;
- the source passes the repository's lint/type-check command;
- the packaged build contains everything needed to run;
- the documented build is reproducible, launchable, and explainable by the
  project team.

## Test record

For each test, add a short record in the following format or link to an issue
containing it:

```text
Test ID:
Date:
Environment / package:
Result: PASS | FAIL | BLOCKED
Evidence:
Notes:
```

## Functional acceptance cases

| ID | Area | Check | Expected result | Owner | Status |
|---|---|---|---|---|---|
| AT-01 | Installation | Run `make install` in the documented environment. | Required Python packages install or the documented dependency error is clear. | Both | Ready to verify |
| AT-02 | Launch | Run `make run` with `config.json`. | The game starts, loads the configured levels, and opens the menu/window. | Both | Ready to verify |
| AT-03 | CLI validation | Run the entry point with no argument and with a non-JSON argument. | The program rejects each invalid invocation with a clear error instead of starting with unknown input. | aymouate | Ready to verify |
| AT-04 | Configuration | Use a missing, empty, malformed, or non-object config file. | The game uses safe defaults and does not crash. | mezahir | Ready to verify |
| AT-05 | Configuration | Use comments, mixed-case keys, unknown keys, wrong types, and invalid level dimensions. | Supported comments are ignored, keys are normalized as implemented, unknown keys are ignored, and invalid values are replaced safely. | mezahir | Ready to verify |
| AT-06 | Maze generation | Generate every configured level, including the 10-level progression. | Each maze has valid dimensions, uses the adapter, and renders in the game. | aymouate | Ready to verify |
| AT-07 | Generator failure | Force or simulate a generator failure. | The failure is reported clearly and does not become an unexplained traceback in normal error handling. | aymouate / Both | Ready to verify |
| AT-08 | Movement | Move with arrow keys and WASD in all four directions. | Pac-Man responds to both control schemes and cannot cross a closed wall or leave the maze. | mezahir | Ready to verify |
| AT-09 | Collectibles | Collect regular and super pac-gums. | The item disappears, the correct score is added, and a super pac-gum makes active ghosts frightened. | mezahir | Ready to verify |
| AT-10 | Ghost chase | Play with normal ghosts active. | Ghosts use maze paths and pursue according to their target behavior without moving through closed walls. | mezahir | Ready to verify |
| AT-11 | Ghost frightened/eaten | Collect a super pac-gum and collide with a frightened ghost. | The ghost is treated as eaten, returns/respawns correctly, and the player receives ghost points. | mezahir | Ready to verify |
| AT-12 | Player collision | Collide with a normal ghost. | One life is lost, the player respawns at the start position, ghosts reset as designed, and temporary protection applies. | mezahir / aymouate | Ready to verify |
| AT-13 | Timer and pause | Pause and resume during a level, then allow the timer to expire. | Gameplay stops while paused, resumes correctly, and expiry leads to the documented end/progression behavior. | aymouate | Ready to verify |
| AT-14 | Level progression | Clear a level and continue through the configured levels. | The next level loads with its maze/entities reset; completing the final level shows victory. | aymouate | Ready to verify |
| AT-15 | Game over | Lose all lives. | The game-over screen appears and offers the documented next actions. | aymouate | Ready to verify |
| AT-16 | Menus | Navigate main menu, instructions, pause, highscores, and end screens. | Selection, back/escape, quit, and return actions lead to the correct state without freezing the loop. | mezahir / aymouate | Ready to verify |
| AT-17 | Name entry | Enter empty, overlong, non-alphanumeric, and valid names. | Empty input uses the fallback behavior; invalid characters/length are rejected; valid names are normalized and saved. | aymouate | Ready to verify |
| AT-18 | Highscores | Load valid, malformed, oversized, and missing highscore files, then record a score. | Invalid entries are ignored safely, scores sort high-to-low, and only the top ten remain. | aymouate | Ready to verify |
| AT-19 | Cheat mode | Toggle cheat mode and use freeze, infinite lives, invincibility, and next-level controls. | Each control changes only its intended behavior and the on-screen indicator reflects the active mode. | mezahir | Ready to verify |
| AT-20 | Audio/assets | Launch with all repository assets and audio present. | Required media loads and gameplay/menu sound effects do not prevent startup. | mezahir / Both | Ready to verify |
| AT-21 | Quality | Run `make lint`. | flake8 and mypy complete without errors under the documented environment. | aymouate | Ready to verify |
| AT-22 | Package | Build the PyInstaller-or-similar package and launch it from a clean location. | The package runs without relying on the repository's current working directory or undeclared files. | mezahir / Both | Ready to verify |

## Exploratory checks

These checks are useful after the functional cases pass:

- try the smallest supported maze dimensions and the largest configured level;
- play with no remaining regular pac-gums and with all four super pac-gums;
- pause at the edge of a timer expiry and resume;
- quit and restart after a highscore write;
- run the game from a directory other than the repository root;
- repeat a level reset several times to look for stale entities or score state;
- use cheat mode to reach later levels, then disable it before normal play;
- regenerate levels with the same seed and confirm the intended reproducibility.

## Evidence checklist

For the completed delivery record, collect:

- a successful `make lint` result;
- a clean launch log or screenshot for the source version;
- a clean launch log or screenshot for the packaged version;
- evidence that the package contains the game assets, audio, and maze
  generator;
- an acceptance-test record for configuration failure and highscore
  corruption;
- the final private/unlisted upload location, if the project submission
  requires it.

