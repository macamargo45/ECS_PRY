from enum import Enum


class CPlayerState:
    def __init__(self, lives: int):
        self.state:PlayerState = PlayerState.ALIVE
        self.lives = lives
        self.max_deaths = 3
        self.curr_dead_time = 0


class PlayerState(Enum):
    ALIVE = 0
    DEAD = 1
