from typing import Any

from engine.player import Player


class InteractionManager:

    def __init__(
        self, player: Player, pacgums: Any, super_pacgums: Any
    ) -> None:
        self.player = player
        self.pacgums = pacgums
        self.super_pacgums = super_pacgums

    def check_pacgum(self) -> None:
        if self.player.current_pos in self.pacgums:
            self.pacgums.discard(self.player.current_pos)
            self.player.add_score()
        elif self.player.current_pos in self.super_pacgums:
            self.super_pacgums.remove(self.player.current_pos)
            self.player.add_super_score()
