class CheatMode:
    def __init__(self) -> None:
        self.invincibility = False
        self.ghost_freeze = False
        self.infini_lives = False
        self.speed_boost = False
        self.freeze_timer = False

    def infinite_lives(self) -> None:
        self.infini_lives = not self.infini_lives

    def freeze(self) -> None:
        self.ghost_freeze = not self.ghost_freeze
