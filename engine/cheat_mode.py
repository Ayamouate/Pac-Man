class CheatMode:
    def __init__(self) -> None:
        self.invincibility = False
        self.freeze = False
        self.infinite_lives = False
        self.speed_boost = False
        self.level_skip = False
        self.active = False

    def cheate_mode_active(self) -> None:
        self.active = not self.active
    def toggle_infinite_lives(self) -> None:
        self.infinite_lives = not self.infinite_lives

    def toggle_freeze(self) -> None:
        self.freeze = not self.freeze

    def toggle_invincibility(self) -> None:
        self.invincibility = not self.invincibility

    def toggle_level_skip(self) -> None:
        self.level_skip = not self.level_skip