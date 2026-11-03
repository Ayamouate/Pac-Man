## Pac-Man maze generation

The project uses the assigned `mazegenerator` package without modifying it.
The adapter in `maze/maze.py` passes each configured level size, the configured
seed, and `perfect=False` so the generated maze has Pac-Man-compatible
corridors.

Run the parser and Pygame viewer with:

```bash
python3 pac-man.py config.json
```

The viewer opens with a main menu. Use Up/Down and Enter to select an option.
During the game, use Arrow keys or WASD to move, N/B to change levels, Esc to
return to the menu, and Q to quit. Press P to pause; the level timer does not
run while paused.

The `assets/tree_wind.mp4` file is played in a loop as the background. Run
`make install` to install the bundled FFmpeg helper used for playback. If
FFmpeg is unavailable, the viewer falls back to `assets/Bg.jpeg`.

Each level must be completed before `level_max_time` seconds elapse. Running
out of time ends the game. Losing a life respawns Pac-Man at the level start
with three seconds of ghost-collision protection. Clearing every regular and
super pac-gum on the final level displays the victory screen. The end screen
appears first; press Enter to enter a name, then press Enter again to
continue to the highscores screen. The leaderboard keeps its top ten scores.

## Sound assets

The game uses short, original-style arcade and UI effects from the CC0
[Various Sound Effects set on OpenGameArt](https://opengameart.org/content/various-sound-effects-0).
The files are renamed locally to describe their game event. The source names,
creator, source page, and license are recorded here for reuse and auditing.

| Game event | Local file | Source sound name | Creator | License |
| --- | --- | --- | --- | --- |
| Menu navigation | `audio/sounds/menu_move.wav` | `snd_menu_move.wav` | Julie Damsgaard / Spring Spring | CC0 |
| Menu entry and selection jingle | `audio/sounds/menu_select.wav` | `snd_menu_select.wav` | Julie Damsgaard / Spring Spring | CC0 |
| Pac-gum collected | `audio/sounds/pacgum_collect.wav` | `get_important_item.wav` | Julie Damsgaard / Spring Spring | CC0 |
| Super pac-gum collected | `audio/sounds/power_pellet.wav` | `snd_getpowerup.wav` | Julie Damsgaard / Spring Spring | CC0 |
| Ghost eaten | `audio/sounds/ghost_eaten.wav` | `pop.wav` | Julie Damsgaard / Spring Spring | CC0 |
| Player loses a life | `audio/sounds/player_death.wav` | `player_hit.wav` | Julie Damsgaard / Spring Spring | CC0 |
| Level cleared | `audio/sounds/level_clear.wav` | `snd_treasure.wav` | Julie Damsgaard / Spring Spring | CC0 |
| Game over | `audio/sounds/game_over.wav` | `snd_death2.wav` | Julie Damsgaard / Spring Spring | CC0 |
| Menu and highscores music | `audio/music/music.wav` | User-provided track | — | — |

These are not the original Namco recordings and no Namco sound files are
included in the project.

The user-provided track plays on the main menu, highscores, instructions, and
gameplay screens, repeats for longer sessions, and stops on the game-over and
victory screens. The game loads it from `audio/music/music.wav`.

## Configuration

`config.json` is a JSON object. Full-line comments beginning with `#` or `//`
are ignored. Missing or incorrectly typed top-level values use these defaults:

```json
{
  "highscore_filename": "highscores.json",
  "lives": 3,
  "pacgum": 42,
  "points_per_pacgum": 10,
  "points_per_super_pacgum": 50,
  "points_per_ghost": 200,
  "seed": 42,
  "level_max_time": 90,
  "levels": [
    {"width": 15, "height": 15}
  ]
}
```

`levels` is normalized to at least ten entries; additional configured levels
are retained. Each entry contains an integer `width` and `height`; invalid
width or height values use `15`. Unknown keys are ignored.

