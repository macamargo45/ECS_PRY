from enum import Enum


class CPlayerState:
    def __init__(self, lives:int):
        self.state = PlayerState.IDLE
        self.lives = lives


class PlayerState(Enum):
    IDLE = 0
    MOVE = 1
