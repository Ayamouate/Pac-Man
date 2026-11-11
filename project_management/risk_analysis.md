# Risk analysis

This register focuses on risks that can affect a playable, reproducible
release. Priority is qualitative: `High`, `Medium`, or `Low`.

| ID | Risk | Likelihood | Impact | Priority | Mitigation / response | Owner | Status |
|---|---|---|---|---|---|---|---|
| R1 | A malformed, missing, or unexpectedly typed configuration prevents the game from starting. | Medium | High | High | Keep parser defaults and type validation; test missing files, invalid JSON, wrong types, comments, and invalid level sizes. | mezahir / Both | Addressed in code; verify regression cases |
| R2 | The assigned maze generator is unavailable, incompatible, or fails for a level. | Medium | High | High | Keep the bundled package fallback, validate level dimensions, use reproducible seeds, and convert generator failures into a clear `MazeGenerationError`. | aymouate | Addressed in code; verify clean package |
| R3 | Packaging omits assets, audio, the generator package, or writable data paths. | High | High | High | Build from a clean location, launch the packaged game, inspect collected files, and verify highscore behavior. | mezahir / Both | Controlled and completed |
| R4 | A change to one subsystem breaks the integrated game loop or state machine. | Medium | High | High | Integrate frequently and run a full menu-to-game-to-end-state scenario. | Both | Addressed and completed |
| R5 | Ghost movement or state transitions make the game unwinnable or inconsistent. | Medium | Medium | Medium | Test chase/BFS, frightened/flee, eaten, respawn, collision, and level reset behavior; use cheat mode to reach cases quickly. | mezahir | Addressed in code; balance check remains useful |
| R6 | Maze dimensions or spawn locations create unreachable entities or collectibles. | Medium | High | High | Validate dimensions at generation time, test all configured levels, and check the player, four ghosts, four corner super-pac-gums, and pac-gums after each reset. | aymouate / mezahir | Addressed in code; verify all levels |
| R7 | Malformed highscore data crashes the game or allows invalid names/scores. | Medium | Medium | Medium | Ignore invalid records safely, validate names and non-negative scores, cap the table at ten entries, and test read/write failures. | aymouate | Addressed in code; verify filesystem cases |
| R8 | Timing, pause, respawn, or level progression behaves differently across machines. | Medium | Medium | Medium | Run pause/resume, timer expiry, respawn protection, level changes, and victory/game-over checks at normal frame rate and in the packaged build. | Both | Verify during acceptance testing |
| R9 | Missing or corrupt visual/audio assets degrade startup or gameplay. | Medium | Medium | Medium | Confirm every required asset is included, test the documented fallback for the player image, and launch from the package rather than the repository root only. | mezahir / Both | Verify during packaging |
| R10 | Linting, type checking, or documentation drift reduces maintainability or delivery readiness. | Low | Medium | Medium | Run the Makefile `lint` target, keep type hints/docstrings current, and link project-management documents from the root README. | aymouate / Both | Addressed and completed |
| R11 | Late polish expands scope and displaces release-critical work. | Medium | Medium | Medium | Treat sounds, animations, and balance as buffer work after the core release requirements. | Both | Controlled and completed |

## Risk response order

1. **Release blockers:** packaging, missing dependencies/assets, and generator
   failures.
2. **Playable-loop blockers:** state transitions, level progression, lives,
   collision, and timer behavior.
3. **Data-safety issues:** configuration and highscore corruption.
4. **Maintainability and delivery:** reproducibility, lint/type checks, and
   documentation.
5. **Optional polish:** sounds, animations, and balance improvements that do
   not threaten delivery.

