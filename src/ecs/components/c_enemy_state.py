from enum import Enum
import pygame

class EnemyStates(Enum):
    IDLE = 0,

class CEnemyState:
    def __init__(self) -> None:
        self.state:EnemyStates = EnemyStates.IDLE
        self.fold_pos:pygame.Vector2 = pygame.Vector2(0,0)