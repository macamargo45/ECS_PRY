from enum import Enum


class EnemyStates(Enum):
    IDLE = 0,

class CEnemyState:
    def __init__(self) -> None:
        self.state:EnemyStates = EnemyStates.IDLE