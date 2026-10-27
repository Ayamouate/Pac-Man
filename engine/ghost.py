

class Ghost:
    def __init__(
        self,
        color: str,
        direction: str,
        spawn_pos: tuple[int, int],
        current_pos: tuple[int, int],
        state: str,
    ) -> None:
        self.color = color
        self.direction = direction
        self.spawn_pos = spawn_pos
        self.current_pos = current_pos
        self.state = state
