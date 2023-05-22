from enum import Enum


class CPlayerState:
    def __init__(self, lives:int, respawn_time: int):
        self.state = PlayerState.MOVE
        self.lives = lives
        self.respawn_time = respawn_time
        self.actual_respawn_time = respawn_time


class PlayerState(Enum):
    IDLE = 0
    MOVE = 1
    DEAD = 2
