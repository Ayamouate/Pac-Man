## Pac-Man maze generation

The project uses the assigned `mazegenerator` package without modifying it.
The adapter in `maze/maze.py` passes each configured level size, the configured
seed, and `perfect=False` so the generated maze has Pac-Man-compatible
corridors.

Run the parser and Pygame viewer with:

```bash
python3 pac-man.py config.json
```

The viewer shows one level at a time. Use the arrow keys or WASD to move, N/B
to change levels, and Esc or Q to quit.

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

`levels` is normalized to ten entries. Each entry contains an integer
`width` and `height`; invalid width or height values use `15`. Unknown keys
are ignored.

