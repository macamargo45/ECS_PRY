from enum import Enum
import pygame
import random

class EnemyStates(Enum):
    IDLE = 0,
    ATTACK = 1,

class CEnemyState:
    def __init__(self) -> None:
        self.state:EnemyStates = EnemyStates.IDLE
        self.move_pos:pygame.Vector2 = pygame.Vector2(0,0)
        
        self.rng:random.Random = random.Random()
        self.prob_fire:int = 1999
        self.prob_fire_attack:int = 1950